from .models import EconomicReport, MarketDataSnapshot, OrderIntent, Portfolio, RiskPolicy


class EconomicResearchAgent:
    role = "research"
    def run(self):
        return {"agent": self.role, "status": "ready", "capabilities": ["economic reports", "market research"]}


class MarketDataAgent:
    role = "market_data"
    def latest(self, asset):
        snap = MarketDataSnapshot.objects.filter(asset=asset).first()
        return snap


class AnalysisAgent:
    role = "analysis"
    def analyze(self, asset):
        snap = MarketDataSnapshot.objects.filter(asset=asset).first()
        return {"symbol": asset.symbol, "latest_price": str(snap.price) if snap else None, "status": "data-dependent"}


class StrategyAgent:
    role = "strategy"
    def propose(self, portfolio, asset, side, quantity, price, strategy=None):
        return OrderIntent.objects.create(portfolio=portfolio, asset=asset, side=side, quantity=quantity, limit_price=price, strategy=strategy)


class RiskAgent:
    role = "risk"
    def validate(self, order, policy=None):
        if policy and policy.max_order_value and order.limit_price and order.quantity * order.limit_price > policy.max_order_value:
            return False, "Order exceeds configured maximum value."
        if policy and policy.require_owner_approval:
            return True, "Owner approval required before any real action."
        return True, "Risk checks passed for paper workflow."


class PortfolioAgent:
    role = "portfolio"
    def snapshot(self, portfolio):
        from .services import portfolio_snapshot
        return portfolio_snapshot(portfolio)


class ExecutionAgent:
    role = "execution"
    def execute(self, order):
        from .services import paper_execute
        return paper_execute(order)


class EconomicMasterAgent:
    """Coordinator for economic research, analysis, risk and paper trading."""
    def __init__(self):
        self.research = EconomicResearchAgent()
        self.market_data = MarketDataAgent()
        self.analysis = AnalysisAgent()
        self.strategy = StrategyAgent()
        self.risk = RiskAgent()
        self.portfolio = PortfolioAgent()
        self.execution = ExecutionAgent()

    def capabilities(self):
        return ["research", "market_data", "analysis", "strategy", "risk", "portfolio", "paper_trading", "real_execution_blocked"]
