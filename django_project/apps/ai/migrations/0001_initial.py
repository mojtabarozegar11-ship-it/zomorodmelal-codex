from django.db import migrations, models


class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[migrations.CreateModel(name="AIConfiguration",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("provider",models.CharField(max_length=50,unique=True)),("enabled",models.BooleanField(default=False)),("api_key",models.CharField(blank=True,default="",max_length=500)),("base_url",models.URLField(blank=True,default="https://api.deepseek.com")),("model",models.CharField(default="deepseek-chat",max_length=100)),("updated_at",models.DateTimeField(auto_now=True))],options={"verbose_name":"AI Configuration","verbose_name_plural":"AI Configurations"})]