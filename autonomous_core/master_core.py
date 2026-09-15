import os
import json
import ast
from datetime import datetime


class MasterCore:

    VERSION = "1.0.0"

    def __init__(self):
        self.root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        self.data_dir = os.path.join(self.root, "data")
        self.sandbox_dir = os.path.join(
            self.root, "sandbox",
            "autonomous_workspace"
        )

        self.state_file = os.path.join(
            self.data_dir,
            "master_core_state.json"
        )

        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.sandbox_dir, exist_ok=True)

        self.state = self._load_state()

    # -------------------------
    # State
    # -------------------------

    def _load_state(self):
        if not os.path.exists(self.state_file):
            state = {
                "version": self.VERSION,
                "cycles": 0,
                "agents": [],
                "capabilities": [],
                "proposals": [],
                "access_requests": [],
                "last_cycle": None
            }
            self._save_state(state)
            return state

        try:
            with open(
                self.state_file,
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)
        except Exception:
            return {
                "version": self.VERSION,
                "cycles": 0,
                "agents": [],
                "capabilities": [],
                "proposals": [],
                "access_requests": [],
                "last_cycle": None
            }

    def _save_state(self, state=None):
        if state is not None:
            self.state = state

        with open(
            self.state_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                self.state,
                f,
                ensure_ascii=False,
                indent=2
            )

    # -------------------------
    # Project discovery
    # -------------------------

    def discover_project(self):
        files = []

        ignored = {
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "node_modules"
        }

        for current, dirs, names in os.walk(self.root):

            dirs[:] = [
                d for d in dirs
                if d not in ignored
            ]

            for name in names:

                path = os.path.join(
                    current,
                    name
                )

                relative = os.path.relpath(
                    path,
                    self.root
                )

                files.append(relative)

        return files

    # -------------------------
    # Python audit
    # -------------------------

    def audit_python(self):

        results = []

        for relative in self.discover_project():

            if not relative.endswith(".py"):
                continue

            path = os.path.join(
                self.root,
                relative
            )

            result = {
                "file": relative,
                "syntax_ok": False,
                "error": None
            }

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:
                    source = f.read()

                ast.parse(source)

                result["syntax_ok"] = True

            except Exception as e:

                result["error"] = str(e)

            results.append(result)

        return results

    # -------------------------
    # Capability discovery
    # -------------------------

    def discover_capabilities(self):

        capabilities = set()

        mapping = {
            "web_research": "web_research",
            "research": "research",
            "agent_factory": "agent_generation",
            "factory": "agent_generation",
            "sandbox": "sandbox_execution",
            "testing": "automated_testing",
            "evolution": "evolution",
            "versioning": "rollback",
            "approval": "owner_approval",
            "execution": "execution_control",
            "orchestrator": "orchestration",
            "access": "access_management",
            "knowledge": "knowledge_management",
            "memory": "memory",
            "planner": "planning",
            "evaluation": "evaluation"
        }

        for relative in self.discover_project():

            parts = relative.replace(
                "\\",
                "/"
            ).split("/")

            for part in parts:

                if part in mapping:
                    capabilities.add(
                        mapping[part]
                    )

        self.state["capabilities"] = sorted(
            capabilities
        )

        return sorted(capabilities)

    # -------------------------
    # Agent discovery
    # -------------------------

    def discover_agents(self):

        agents = []

        agent_dir = os.path.join(
            self.root,
            "agents"
        )

        if os.path.isdir(agent_dir):

            for name in os.listdir(agent_dir):

                if name.endswith(".py"):

                    agents.append({
                        "name": name[:-3],
                        "source": "agents",
                        "status": "discovered"
                    })

        self.state["agents"] = agents

        return agents

    # -------------------------
    # Gap analysis
    # -------------------------

    def analyze_gaps(self):

        required = {
            "planning",
            "research",
            "memory",
            "knowledge_management",
            "evaluation",
            "sandbox_execution",
            "automated_testing",
            "rollback",
            "owner_approval",
            "execution_control",
            "orchestration",
            "agent_generation",
            "evolution"
        }

        available = set(
            self.state.get(
                "capabilities",
                []
            )
        )

        missing = sorted(
            required - available
        )

        return missing

    # -------------------------
    # Agent generation design
    # -------------------------

    def design_agents(self, missing):

        designs = []

        templates = {
            "planning": (
                "StrategicPlannerAgent",
                "تحلیل اهداف و طراحی برنامه اجرایی"
            ),
            "research": (
                "ResearchAgent",
                "تحقیق و جمع‌آوری دانش"
            ),
            "sandbox_execution": (
                "SandboxAgent",
                "ساخت و اجرای آزمایشی امن"
            ),
            "automated_testing": (
                "TestingAgent",
                "تست خودکار و بررسی نتیجه"
            ),
            "agent_generation": (
                "AgentFactoryAgent",
                "طراحی و تولید زیرایجنت"
            ),
            "evolution": (
                "EvolutionAgent",
                "طراحی نسل‌های جدید سیستم"
            ),
            "orchestration": (
                "OrchestratorAgent",
                "هماهنگی تمام ایجنت‌ها"
            ),
            "access_management": (
                "AccessAgent",
                "شناسایی و مدیریت دسترسی‌های لازم"
            )
        }

        for capability in missing:

            if capability in templates:

                name, purpose = templates[
                    capability
                ]

                designs.append({
                    "name": name,
                    "purpose": purpose,
                    "capability": capability,
                    "status": "design_only",
                    "owner_approval_required": True
                })

        return designs

    # -------------------------
    # Access discovery
    # -------------------------

    def discover_access_requirements(self):

        requirements = []

        capabilities = self.state.get(
            "capabilities",
            []
        )

        if "research" in capabilities:

            requirements.append({
                "resource": "internet_research",
                "level": "read",
                "status": "identified",
                "owner_approval_required": True
            })

        if "execution_control" in capabilities:

            requirements.append({
                "resource": "execution_environment",
                "level": "restricted",
                "status": "identified",
                "owner_approval_required": True
            })

        if "orchestration" in capabilities:

            requirements.append({
                "resource": "agent_runtime",
                "level": "restricted",
                "status": "identified",
                "owner_approval_required": True
            })

        self.state["access_requests"] = requirements

        return requirements

    # -------------------------
    # Proposal creation
    # -------------------------

    def create_proposals(
        self,
        missing,
        agent_designs
    ):

        proposals = []

        for capability in missing:

            proposals.append({
                "type": "capability_upgrade",
                "capability": capability,
                "status": "proposal_only",
                "owner_approval_required": True
            })

        for design in agent_designs:

            proposals.append({
                "type": "agent_generation",
                "agent": design["name"],
                "capability": design["capability"],
                "status": "proposal_only",
                "owner_approval_required": True
            })

        self.state["proposals"] = proposals

        return proposals

    # -------------------------
    # Autonomous cycle
    # -------------------------

    def run_cycle(self):

        self.state["cycles"] += 1

        files = self.discover_project()

        python_audit = self.audit_python()

        capabilities = (
            self.discover_capabilities()
        )

        agents = self.discover_agents()

        missing = self.analyze_gaps()

        agent_designs = self.design_agents(
            missing
        )

        access = (
            self.discover_access_requirements()
        )

        proposals = self.create_proposals(
            missing,
            agent_designs
        )

        self.state["last_cycle"] = (
            datetime.now().isoformat()
        )

        self._save_state()

        syntax_errors = [
            x for x in python_audit
            if not x["syntax_ok"]
        ]

        return {
            "version": self.VERSION,
            "cycle": self.state["cycles"],
            "files": len(files),
            "python_files": len(python_audit),
            "syntax_errors": syntax_errors,
            "capabilities": capabilities,
            "missing_capabilities": missing,
            "agents": agents,
            "new_agent_designs": agent_designs,
            "access_requirements": access,
            "proposals": proposals,
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "sandbox_only": True
        }

    # -------------------------
    # Status
    # -------------------------

    def status(self):

        return {
            "master_core": True,
            "version": self.VERSION,
            "cycles": self.state.get(
                "cycles",
                0
            ),
            "agents": len(
                self.state.get(
                    "agents",
                    []
                )
            ),
            "capabilities": len(
                self.state.get(
                    "capabilities",
                    []
                )
            ),
            "proposals": len(
                self.state.get(
                    "proposals",
                    []
                )
            ),
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "sandbox_only": True
        }


if __name__ == "__main__":

    core = MasterCore()

    result = core.run_cycle()

    print("\n🧠 MASTER CORE")
    print("=" * 50)

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )

    print("\n📊 STATUS")
    print("=" * 50)

    print(
        json.dumps(
            core.status(),
            ensure_ascii=False,
            indent=2
        )
    )
