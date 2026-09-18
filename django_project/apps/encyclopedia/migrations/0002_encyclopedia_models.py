from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("encyclopedia", "0001_initial")]
    operations = [
        migrations.DeleteModel(name="Article"),
        migrations.CreateModel(name="EncyclopediaCategory", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=200)), ("slug", models.SlugField(unique=True)),
            ("description", models.TextField(blank=True)),
        ]),
        migrations.CreateModel(name="EncyclopediaArticle", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=300)), ("slug", models.SlugField(unique=True)),
            ("summary", models.TextField(blank=True)), ("content", models.TextField()),
            ("keywords", models.TextField(blank=True)), ("sources", models.TextField(blank=True)),
            ("published", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="encyclopedia.encyclopediacategory")),
        ]),
        migrations.CreateModel(name="KnowledgeRelation", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="encyclopedia.encyclopediaarticle")),
            ("related_article", models.ForeignKey(related_name="relations", on_delete=django.db.models.deletion.CASCADE, to="encyclopedia.encyclopediaarticle")),
        ]),
    ]
