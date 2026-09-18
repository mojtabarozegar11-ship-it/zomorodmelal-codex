from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("economy", "0002_signal_sales")]
    operations = [
        migrations.CreateModel(name="SignalCoupon", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("code",models.CharField(max_length=50,unique=True)),("percent",models.PositiveIntegerField(default=0)),("active",models.BooleanField(default=True)),("max_uses",models.PositiveIntegerField(default=0)),("used_count",models.PositiveIntegerField(default=0)),("expires_at",models.DateTimeField(blank=True,null=True))]),
        migrations.CreateModel(name="SignalSubscription", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("starts_at",models.DateTimeField()),("expires_at",models.DateTimeField()),("active",models.BooleanField(default=True)),("created_at",models.DateTimeField(auto_now_add=True)),("product",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="subscriptions",to="economy.signalproduct")),("user",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="signal_subscriptions",to="auth.user"))]),
        migrations.CreateModel(name="SignalPerformance", fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("outcome",models.CharField(default="open",max_length=30)),("return_percent",models.DecimalField(blank=True,decimal_places=4,max_digits=12,null=True)),("verified",models.BooleanField(default=False)),("closed_at",models.DateTimeField(blank=True,null=True)),("notes",models.TextField(blank=True)),("signal",models.OneToOneField(on_delete=django.db.models.deletion.PROTECT,related_name="performance",to="economy.signal"))]),
    ]
