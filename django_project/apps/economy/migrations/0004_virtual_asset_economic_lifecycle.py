from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("economy", "0003_signal_membership")]
    operations = [
        migrations.CreateModel(
            name="VirtualAssetProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)), ("symbol", models.CharField(max_length=30, unique=True)),
                ("asset_class", models.CharField(choices=[("utility","Utility"),("membership","Membership"),("collectible","Collectible"),("digital_certificate","Digital certificate"),("tokenized_right","Tokenized right")], default="utility", max_length=40)),
                ("status", models.CharField(choices=[("idea","Idea"),("research","Research"),("design","Design"),("legal_review","Legal review"),("prototype","Prototype"),("audit","Audit"),("approved","Approved"),("published","Published"),("retired","Retired")], default="idea", max_length=30)),
                ("concept", models.TextField()), ("economic_model", models.TextField(blank=True)), ("behavioral_model", models.TextField(blank=True)),
                ("target_jurisdictions", models.TextField(blank=True, help_text="Jurisdictions considered for legal review.")), ("legal_basis", models.TextField(blank=True)), ("disclosure", models.TextField(blank=True)),
                ("legal_reviewed", models.BooleanField(default=False)), ("owner_approved", models.BooleanField(default=False)), ("issuance_approved", models.BooleanField(default=False)), ("publication_approved", models.BooleanField(default=False)), ("active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="EconomicWorkItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=250)),
                ("domain", models.CharField(choices=[("macro","Macro economy"),("behavior","Behavioral economics"),("markets","Financial markets"),("innovation","Innovation"),("virtual_assets","Virtual assets"),("compliance","Compliance"),("product","Product"),("publishing","Publishing"),("revenue","Revenue"),("analytics","Analytics")], max_length=30)),
                ("status", models.CharField(choices=[("queued","Queued"),("research","Research"),("review","Review"),("approved","Approved"),("done","Done"),("blocked","Blocked")], default="queued", max_length=20)),
                ("brief", models.TextField()), ("output", models.TextField(blank=True)), ("owner_approval_required", models.BooleanField(default=True)), ("owner_approved", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="EconomicPublication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=250)),
                ("channel", models.CharField(choices=[("site","Website"),("report","Report"),("signal","Signal"),("social","Social"),("marketplace","Marketplace")], max_length=30)), ("content", models.TextField()), ("compliance_checked", models.BooleanField(default=False)), ("owner_approved", models.BooleanField(default=False)), ("published", models.BooleanField(default=False)), ("published_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
