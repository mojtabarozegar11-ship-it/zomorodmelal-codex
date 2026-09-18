from decimal import Decimal
from django.utils import timezone
from .models import EconomicAuditLog, OrderIntent, Position, Trade


class TradingGate:
    """Hard safety gate: real execution is never performed by this service."""
    @staticmethod
    def validate(order):
        if order.real_execution_requested:
            EconomicAuditLog.objects.create(action="real_execution_blocked", detail=f"Order {order.pk}", approved=False)
            order.status = "blocked"
            order.save(update_fields=["status"])
            return False, "Real execution is disabled; owner approval and an external execution adapter are required."
        return True, "paper execution allowed"


def paper_execute(order):
    ok, message = TradingGate.validate(order)
    if not ok:
        return False, message
    price = order.limit_price
    if price is None:
        return False, "A limit price is required for paper execution."
    portfolio = order.portfolio
    value = price * order.quantity
    if order.side == "buy" and portfolio.cash_balance < value:
        order.status = "blocked"
        order.save(update_fields=["status"])
        return False, "Insufficient paper cash."
    position, _ = Position.objects.get_or_create(portfolio=portfolio, asset=order.asset)
    if order.side == "buy":
        old_qty = position.quantity
        new_qty = old_qty + order.quantity
        position.average_price = ((old_qty * position.average_price) + value) / new_qty if new_qty else Decimal("0")
        position.quantity = new_qty
        portfolio.cash_balance -= value
    else:
        if position.quantity < order.quantity:
            return False, "Insufficient paper position."
        position.quantity -= order.quantity
        portfolio.cash_balance += value
    position.save()
    portfolio.save(update_fields=["cash_balance"])
    Trade.objects.create(order=order, executed_price=price, executed_quantity=order.quantity, paper=True)
    order.status = "paper_executed"
    order.save(update_fields=["status"])
    EconomicAuditLog.objects.create(action="paper_trade", detail=f"Order {order.pk}", approved=False)
    return True, "paper trade executed"


def portfolio_snapshot(portfolio):
    positions = []
    for p in portfolio.positions.select_related("asset"):
        positions.append({"symbol": p.asset.symbol, "quantity": str(p.quantity), "average_price": str(p.average_price)})
    return {"name": portfolio.name, "cash": str(portfolio.cash_balance), "paper_trading": portfolio.paper_trading, "positions": positions, "timestamp": timezone.now().isoformat()}
