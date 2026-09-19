from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("encyclopedia", "0002_encyclopedia_models"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="encyclopediaarticle",
            options={"ordering": ("-updated_at", "title")},
        ),
        migrations.AlterField(
            model_name="knowledgerelation",
            name="article",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="outgoing_relations",
                to="encyclopedia.encyclopediaarticle",
            ),
        ),
        migrations.AlterField(
            model_name="knowledgerelation",
            name="related_article",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="incoming_relations",
                to="encyclopedia.encyclopediaarticle",
            ),
        ),
        migrations.AddConstraint(
            model_name="knowledgerelation",
            constraint=models.UniqueConstraint(
                fields=("article", "related_article"),
                name="encyclopedia_relation_unique",
            ),
        ),
    ]
