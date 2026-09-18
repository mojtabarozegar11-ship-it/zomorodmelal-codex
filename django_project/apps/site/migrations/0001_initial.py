from django.db import migrations, models
class Migration(migrations.Migration):
    initial=True
    operations=[
        migrations.CreateModel(name="SitePage",fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("title",models.CharField(max_length=200)),("slug",models.SlugField(unique=True)),
            ("content",models.TextField(blank=True)),("published",models.BooleanField(default=False))]),
        migrations.CreateModel(name="ActivityLog",fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("action",models.CharField(max_length=200)),("created_at",models.DateTimeField(auto_now_add=True))]),
    ]
