from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from .models import EconomicAuditLog, Position, Trade
from .policies import guard_real_execution


class TradingGate:
    """Single execution boundary; real execution is explicitly gated."""

    @staticmethod
    def validate(order):
        if order.status not in {"pending", "approved"}:
            return False, "Order is not executable in its current state."
        if order.quantity <= 0:
            return False, "Order quantity must be positive."
        if order.real_execution_requested:
            try:
                guard_real_execution(owner_approved=order.owner_approved)
            except PermissionDenied as exc:
                EconomicAuditLog.objects.create(
                    action="real_execution_blocked",
                    detail=f"Order {order.pk}: {exc}",
                    approved=False,
                )
                order.status = "blocked"
                order.save(update_fields=["status"])
                return False, str(exc)
        return True, "execution allowed"


@transaction.atomic
def paper_execute(order):
    ok, message = TradingGate.validate(order)
    if not ok:
        return False, message
    if not order.portfolio.paper_trading:
        return False, "Portfolio is not configured for paper trading."
    price = order.limit_price
    if price is None or price <= 0:
        return False, "A positive limit price is required for paper execution."

    portfolio = order.portfolio
    value = price * order.quantity
    position, _ = Position.objects.select_for_update().get_or_create(
        portfolio=portfolio, asset=order.asset
    )
    if order.side == "buy":
        if portfolio.cash_balance < value:
            order.status = "blocked"
            order.save(update_fields=["status"])
            return False, "Insufficient paper cash."
        old_qty = position.quantity
        new_qty = old_qty + order.quantity
        position.average_price = ((old_qty * position.average_price) + value) / new_qty
        position.quantity = new_qty
        portfolio.cash_balance -= value
    else:
        if position.quantity < order.quantity:
            return False, "Insufficient paper position."
        position.quantity -= order.quantity
        portfolio.cash_balance += value

    position.save(update_fields=["quantity", "average_price"])
    portfolio.save(update_fields=["cash_balance"])
    Trade.objects.create(
        order=order,
        executed_price=price,
        executed_quantity=order.quantity,
        paper=True,
    )
    order.status = "paper_executed"
    order.save(update_fields=["status"])
    EconomicAuditLog.objects.create(
        action="paper_trade", detail=f"Order {order.pk}", approved=False
    )
    return True, "paper trade executed"


def portfolio_snapshot(portfolio):
    positions = [
        {
            "symbol": p.asset.symbol,
            "quantity": str(p.quantity),
            "average_price": str(p.average_price),
        }
        for p in portfolio.positions.select_related("asset")
    ]
    return {
        "name": portfolio.name,
        "cash": str(portfolio.cash_balance),
        "paper_trading": portfolio.paper_trading,
        "positions": positions,
        "timestamp": timezone.now().isoformat(),
    }
