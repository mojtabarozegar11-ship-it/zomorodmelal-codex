"""Application service boundary for Worker Mojtaba."""
from decimal import Decimal
from typing import Any

from worker_mojtaba.ai.registry import AIProviderRegistry
from worker_mojtaba.core.engine import ExecutionEngine
from worker_mojtaba.core.memory import MemoryStore
from worker_mojtaba.core.master_capability import MasterCapability
from worker_mojtaba.tools.registry import ToolRegistry
from worker_mojtaba.tools.center import ToolCenter
from worker_mojtaba.tools.media_adapter import MediaToolAdapter
from worker_mojtaba.tools.android_adapter import AndroidToolAdapter
from worker_mojtaba.tools.automation_adapter import AutomationToolAdapter
from worker_mojtaba.tools.research_adapter import ResearchToolAdapter
from worker_mojtaba.tools.document_adapter import DocumentToolAdapter
from worker_mojtaba.tools.social_adapter import SocialPublishingToolAdapter
from worker_mojtaba.tools.communications_adapter import CommunicationsToolAdapter
from worker_mojtaba.wallet.wallet import WalletManager
from worker_mojtaba.tools.iranian_bank_adapter import IranianBankAdapter, BankAccountPolicy
from worker_mojtaba.tools.financial_adapter import FinancialToolAdapter
from worker_mojtaba.security.audit import AuditLog
from worker_mojtaba.security.policy import Policy


def _echo_tool(request: str) -> dict[str, Any]:
    return {"status": "completed", "tool": "echo", "request": request}


class WorkerService:
    def __init__(self, ai_registry: AIProviderRegistry | None = None) -> None:
        self.memory = MemoryStore()
        self.tools = ToolRegistry()
        self.wallets = WalletManager()
        self.wallets.configure_default_revenue_wallets()
        self.bank = IranianBankAdapter(
            BankAccountPolicy(
                account_id="owner-configured",
                bank_name="owner-configured",
                revenue_share_wallet_1=Decimal("0.10"),
                revenue_share_wallet_2=Decimal("0.90"),
                wallet_2_outbound_allowed=False,
            )
        )
        self.tool_center = ToolCenter()
        self.tool_center.register(MediaToolAdapter())
        self.tool_center.register(AndroidToolAdapter())
        self.tool_center.register(AutomationToolAdapter())
        self.tool_center.register(ResearchToolAdapter())
        self.tool_center.register(DocumentToolAdapter())
        self.tool_center.register(SocialPublishingToolAdapter())
        self.tool_center.register(CommunicationsToolAdapter())
        self.tools.register("echo", "Safe diagnostic tool that returns the received request.", _echo_tool)
        self.tool_center.register(FinancialToolAdapter(self.bank, self.wallets))
        self.policy = Policy({
            "echo",
            "account_balance",
            "transactions",
            "calendar_event",
            "list_calendar_events",
            "publish_video",
        })
        self.engine = ExecutionEngine(
            self.memory, self.tools, ai_registry, self.tool_center, policy=self.policy
        )
        self.master = MasterCapability()
        self.audit = AuditLog()

    def dispatch(self, request: str, context: dict[str, Any]) -> dict[str, Any]:
        return self.engine.run(request, context=context)

    def handle(
        self,
        request: str,
        context: dict[str, Any] | None = None,
        *,
        approved: bool = False,
    ) -> dict[str, Any]:
        execution_context = dict(context or {})
        if context is None:
            execution_context["require_approval"] = False
        lifecycle = self.master.run(
            request,
            approved=approved,
            dispatch=self.dispatch,
            context=execution_context,
        )
        result = lifecycle.get("result") or {}
        execution = result.get("execution") or {}
        self.audit.record(
            "task",
            execution.get("result_state", lifecycle.get("status", "unknown")),
            {
                "request": request,
                "route": result.get("route"),
                "intent": result.get("intent"),
                "capability": result.get("authorization", {}).get("capability"),
                "authorized": result.get("authorization", {}).get("allowed"),
                "execution_status": execution.get("status"),
            },
        )
        if lifecycle.get("status") != "completed":
            return {
                "status": lifecycle.get("status", "unknown"),
                "request": request,
                "plan": lifecycle.get("plan", []),
                "goal": lifecycle.get("goal", request),
                "intent": None,
                "route": None,
                "ai": {},
                "execution": {},
                "tools": [],
                "authorization": {},
            }
        return result
