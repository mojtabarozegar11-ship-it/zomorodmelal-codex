from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Farm", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200)), ("location", models.CharField(blank=True, max_length=300)), ("active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True))]),
        migrations.CreateModel(name="ProductionChain", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200, unique=True)), ("description", models.TextField(blank=True)), ("active", models.BooleanField(default=True))]),
        migrations.CreateModel(name="ProductionProduct", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200)), ("category", models.CharField(blank=True, max_length=120)), ("active", models.BooleanField(default=True))]),
    ]
