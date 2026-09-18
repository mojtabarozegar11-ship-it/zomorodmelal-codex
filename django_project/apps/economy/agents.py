from .models import EconomicReport, MarketDataSnapshot, OrderIntent, Portfolio, RiskPolicy

class EconomicResearchAgent:
    role="research"
    def run(self): return {"agent":self.role,"status":"ready","capabilities":["macro economics","economic reports","market research"]}
class MarketDataAgent:
    role="market_data"
    def latest(self,asset): return MarketDataSnapshot.objects.filter(asset=asset).first()
class AnalysisAgent:
    role="analysis"
    def analyze(self,asset):
        snap=MarketDataSnapshot.objects.filter(asset=asset).first()
        return {"symbol":asset.symbol,"latest_price":str(snap.price) if snap else None,"status":"data-dependent"}
class BehavioralEconomicsAgent:
    role="behavioral_economics"
    def analyze(self,context): return {"agent":self.role,"status":"ready","frameworks":["prospect theory","loss aversion","anchoring","herding","confirmation bias"],"note":"Analysis is descriptive; no manipulation design."}
class FinancialMarketsAgent:
    role="financial_markets"
    def analyze(self,asset): return {"agent":self.role,"asset":asset.symbol,"dimensions":["liquidity","volatility","price discovery","market structure","scenario analysis"]}
class InnovationAgent:
    role="innovation"
    def ideate(self,brief): return {"agent":self.role,"status":"ready","method":"economic + behavioral + market + technology synthesis","brief":brief}
class VirtualAssetAgent:
    role="virtual_assets"
    def design(self,project): return {"agent":self.role,"project":project.name,"status":"design","legal_gate":"required before issuance or publication"}
class ComplianceAgent:
    role="compliance"
    def review(self,project):
        ok=project.legal_reviewed and project.owner_approved
        return {"agent":self.role,"ready_for_issuance":ok,"legal_reviewed":project.legal_reviewed,"owner_approved":project.owner_approved,"note":"Jurisdiction-specific professional legal review is required."}
class ProductAgent:
    role="product"
    def lifecycle(self): return ["idea","research","innovation","design","prototype","audit","approval","publication","revenue","analytics","iteration"]
class PublishingAgent:
    role="publishing"
    def can_publish(self,publication): return bool(publication.compliance_checked and publication.owner_approved and not publication.published)
class RevenueAgent:
    role="revenue"
    def plan(self): return ["digital products","subscriptions","signal products","marketplace fees","licensed content","approved virtual-asset products"]
class AnalyticsAgent:
    role="analytics"
    def metrics(self): return ["revenue","conversion","retention","risk","liquidity","engagement","verified performance"]
class StrategyAgent:
    role="strategy"
    def propose(self,portfolio,asset,side,quantity,price,strategy=None): return OrderIntent.objects.create(portfolio=portfolio,asset=asset,side=side,quantity=quantity,limit_price=price,strategy=strategy)
class RiskAgent:
    role="risk"
    def validate(self,order,policy=None):
        if policy and policy.max_order_value and order.limit_price and order.quantity*order.limit_price>policy.max_order_value: return False,"Order exceeds configured maximum value."
        if policy and policy.require_owner_approval: return True,"Owner approval required before any real action."
        return True,"Risk checks passed for paper workflow."
class PortfolioAgent:
    role="portfolio"
    def snapshot(self,portfolio):
        from .services import portfolio_snapshot
        return portfolio_snapshot(portfolio)
class ExecutionAgent:
    role="execution"
    def execute(self,order):
        from .services import paper_execute
        return paper_execute(order)
class EconomicMasterAgent:
    def __init__(self):
        self.research=EconomicResearchAgent(); self.market_data=MarketDataAgent(); self.analysis=AnalysisAgent(); self.behavior=BehavioralEconomicsAgent(); self.markets=FinancialMarketsAgent(); self.innovation=InnovationAgent(); self.virtual_assets=VirtualAssetAgent(); self.compliance=ComplianceAgent(); self.product=ProductAgent(); self.publishing=PublishingAgent(); self.revenue=RevenueAgent(); self.analytics=AnalyticsAgent(); self.strategy=StrategyAgent(); self.risk=RiskAgent(); self.portfolio=PortfolioAgent(); self.execution=ExecutionAgent()
    def capabilities(self): return [a.role for a in (self.research,self.market_data,self.analysis,self.behavior,self.markets,self.innovation,self.virtual_assets,self.compliance,self.product,self.publishing,self.revenue,self.analytics,self.risk,self.portfolio,self.execution)]+["paper_trading","real_execution_blocked","owner_approval_gate"]
