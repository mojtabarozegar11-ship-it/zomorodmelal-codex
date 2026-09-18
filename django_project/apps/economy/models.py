from django.db import models


class Asset(models.Model):
    SYMBOL_TYPES = [("stock", "Stock"), ("crypto", "Crypto"), ("fx", "FX"), ("commodity", "Commodity"), ("fund", "Fund")]
    symbol = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=30, choices=SYMBOL_TYPES, default="stock")
    currency = models.CharField(max_length=10, default="USD")
    active = models.BooleanField(default=True)
    def __str__(self): return self.symbol

class MarketDataSnapshot(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="snapshots")
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=24, decimal_places=10)
    volume = models.DecimalField(max_digits=30, decimal_places=10, default=0)
    source = models.CharField(max_length=100, default="manual")
    class Meta: ordering = ["-timestamp"]

class Strategy(models.Model):
    name = models.CharField(max_length=200, unique=True); description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False); paper_only = models.BooleanField(default=True)
    def __str__(self): return self.name

class RiskPolicy(models.Model):
    name = models.CharField(max_length=200, unique=True)
    max_order_value = models.DecimalField(max_digits=24, decimal_places=4, default=0)
    max_daily_loss = models.DecimalField(max_digits=24, decimal_places=4, default=0)
    require_owner_approval = models.BooleanField(default=True); enabled = models.BooleanField(default=True)
    def __str__(self): return self.name

class Portfolio(models.Model):
    name = models.CharField(max_length=200, unique=True); base_currency = models.CharField(max_length=10, default="USD")
    paper_trading = models.BooleanField(default=True); cash_balance = models.DecimalField(max_digits=24, decimal_places=4, default=0); active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="positions")
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT); quantity = models.DecimalField(max_digits=30, decimal_places=10, default=0); average_price = models.DecimalField(max_digits=24, decimal_places=10, default=0)
    class Meta: unique_together = [("portfolio", "asset")]

class OrderIntent(models.Model):
    SIDES = [("buy", "Buy"), ("sell", "Sell")]
    STATUSES = [("pending", "Pending approval"), ("approved", "Approved"), ("rejected", "Rejected"), ("paper_executed", "Paper executed"), ("blocked", "Blocked")]
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT); asset = models.ForeignKey(Asset, on_delete=models.PROTECT); strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=True)
    side = models.CharField(max_length=10, choices=SIDES); quantity = models.DecimalField(max_digits=30, decimal_places=10); limit_price = models.DecimalField(max_digits=24, decimal_places=10, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default="pending"); owner_approved = models.BooleanField(default=False); real_execution_requested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True); approved_at = models.DateTimeField(null=True, blank=True)

class Trade(models.Model):
    order = models.OneToOneField(OrderIntent, on_delete=models.PROTECT, related_name="trade"); executed_price = models.DecimalField(max_digits=24, decimal_places=10); executed_quantity = models.DecimalField(max_digits=30, decimal_places=10); fee = models.DecimalField(max_digits=24, decimal_places=10, default=0); paper = models.BooleanField(default=True); executed_at = models.DateTimeField(auto_now_add=True)

class EconomicReport(models.Model):
    title = models.CharField(max_length=250); report_type = models.CharField(max_length=50, default="market"); summary = models.TextField(); created_at = models.DateTimeField(auto_now_add=True)

class EconomicAuditLog(models.Model):
    action = models.CharField(max_length=100); detail = models.TextField(blank=True); approved = models.BooleanField(default=False); created_at = models.DateTimeField(auto_now_add=True)

class SignalProduct(models.Model):
    name = models.CharField(max_length=200, unique=True); description = models.TextField(); price = models.DecimalField(max_digits=24, decimal_places=4); currency = models.CharField(max_length=10, default="IRR"); active = models.BooleanField(default=True); disclaimer = models.TextField(default="Signals are informational and do not guarantee profit."); created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class SignalPurchase(models.Model):
    STATUSES = [("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed"), ("refunded", "Refunded")]
    product = models.ForeignKey(SignalProduct, on_delete=models.PROTECT, related_name="purchases"); user = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="signal_purchases"); amount = models.DecimalField(max_digits=24, decimal_places=4); currency = models.CharField(max_length=10, default="IRR"); status = models.CharField(max_length=20, choices=STATUSES, default="pending"); gateway = models.CharField(max_length=50, default="sandbox"); authority = models.CharField(max_length=200, blank=True); paid_at = models.DateTimeField(null=True, blank=True); created_at = models.DateTimeField(auto_now_add=True)

class Signal(models.Model):
    SIDES = [("buy", "Buy"), ("sell", "Sell"), ("hold", "Hold")]
    product = models.ForeignKey(SignalProduct, on_delete=models.PROTECT, related_name="signals"); asset = models.ForeignKey(Asset, on_delete=models.PROTECT); side = models.CharField(max_length=10, choices=SIDES); entry_price = models.DecimalField(max_digits=24, decimal_places=10, null=True, blank=True); stop_loss = models.DecimalField(max_digits=24, decimal_places=10, null=True, blank=True); take_profit = models.DecimalField(max_digits=24, decimal_places=10, null=True, blank=True); rationale = models.TextField(blank=True); published = models.BooleanField(default=False); created_at = models.DateTimeField(auto_now_add=True)

class SignalSubscription(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="signal_subscriptions"); product = models.ForeignKey(SignalProduct, on_delete=models.PROTECT, related_name="subscriptions"); starts_at = models.DateTimeField(); expires_at = models.DateTimeField(); active = models.BooleanField(default=True); created_at = models.DateTimeField(auto_now_add=True)
class SignalCoupon(models.Model):
    code = models.CharField(max_length=50, unique=True); percent = models.PositiveIntegerField(default=0); active = models.BooleanField(default=True); max_uses = models.PositiveIntegerField(default=0); used_count = models.PositiveIntegerField(default=0); expires_at = models.DateTimeField(null=True, blank=True)
class SignalPerformance(models.Model):
    signal = models.OneToOneField(Signal, on_delete=models.PROTECT, related_name="performance"); outcome = models.CharField(max_length=30, default="open"); return_percent = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True); verified = models.BooleanField(default=False); closed_at = models.DateTimeField(null=True, blank=True); notes = models.TextField(blank=True)

class VirtualAssetProject(models.Model):
    STATUS = [("idea","Idea"),("research","Research"),("design","Design"),("legal_review","Legal review"),("prototype","Prototype"),("audit","Audit"),("approved","Approved"),("published","Published"),("retired","Retired")]
    ASSET_CLASSES = [("utility","Utility"),("membership","Membership"),("collectible","Collectible"),("digital_certificate","Digital certificate"),("tokenized_right","Tokenized right")]
    name = models.CharField(max_length=200, unique=True); symbol = models.CharField(max_length=30, unique=True); asset_class = models.CharField(max_length=40, choices=ASSET_CLASSES, default="utility")
    status = models.CharField(max_length=30, choices=STATUS, default="idea"); concept = models.TextField(); economic_model = models.TextField(blank=True); behavioral_model = models.TextField(blank=True)
    target_jurisdictions = models.TextField(blank=True, help_text="Jurisdictions considered for legal review."); legal_basis = models.TextField(blank=True); disclosure = models.TextField(blank=True)
    legal_reviewed = models.BooleanField(default=False); owner_approved = models.BooleanField(default=False); issuance_approved = models.BooleanField(default=False); publication_approved = models.BooleanField(default=False); active = models.BooleanField(default=True); created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.name} ({self.symbol})"

class EconomicWorkItem(models.Model):
    DOMAINS = [("macro","Macro economy"),("behavior","Behavioral economics"),("markets","Financial markets"),("innovation","Innovation"),("virtual_assets","Virtual assets"),("compliance","Compliance"),("product","Product"),("publishing","Publishing"),("revenue","Revenue"),("analytics","Analytics")]
    STATUS = [("queued","Queued"),("research","Research"),("review","Review"),("approved","Approved"),("done","Done"),("blocked","Blocked")]
    title = models.CharField(max_length=250); domain = models.CharField(max_length=30, choices=DOMAINS); status = models.CharField(max_length=20, choices=STATUS, default="queued"); brief = models.TextField(); output = models.TextField(blank=True); owner_approval_required = models.BooleanField(default=True); owner_approved = models.BooleanField(default=False); created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)

class EconomicPublication(models.Model):
    CHANNELS = [("site","Website"),("report","Report"),("signal","Signal"),("social","Social"),("marketplace","Marketplace")]
    title = models.CharField(max_length=250); channel = models.CharField(max_length=30, choices=CHANNELS); content = models.TextField(); compliance_checked = models.BooleanField(default=False); owner_approved = models.BooleanField(default=False); published = models.BooleanField(default=False); published_at = models.DateTimeField(null=True, blank=True)
