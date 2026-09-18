from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ai", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="ContentChannel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("platform", models.CharField(choices=[("instagram","Instagram"),("youtube","YouTube"),("tiktok","TikTok"),("telegram","Telegram"),("x","X"),("facebook","Facebook"),("linkedin","LinkedIn"),("website","Website")], max_length=30)),
                ("handle", models.CharField(blank=True,max_length=180)),
                ("topic", models.CharField(max_length=250)),
                ("audience", models.TextField(blank=True)),
                ("language", models.CharField(default="fa",max_length=30)),
                ("tone", models.CharField(default="professional",max_length=80)),
                ("posting_frequency", models.PositiveIntegerField(default=3)),
                ("timezone", models.CharField(default="Asia/Tehran",max_length=80)),
                ("active", models.BooleanField(default=True)),
                ("auto_publish", models.BooleanField(default=False)),
                ("owner_approved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering":("platform","name")},
        ),
        migrations.CreateModel(
            name="ContentCompetitor",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("name", models.CharField(max_length=180)), ("platform", models.CharField(max_length=30)),
                ("url", models.URLField(blank=True)), ("notes", models.TextField(blank=True)), ("active", models.BooleanField(default=True)),
                ("channel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="competitors",to="ai.contentchannel")),
            ],
        ),
        migrations.CreateModel(
            name="ContentStrategy",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("pillars", models.JSONField(blank=True,default=list)), ("audience_personas", models.JSONField(blank=True,default=list)),
                ("formats", models.JSONField(blank=True,default=list)), ("hooks", models.JSONField(blank=True,default=list)),
                ("banned_topics", models.JSONField(blank=True,default=list)), ("brand_rules", models.JSONField(blank=True,default=dict)),
                ("algorithm_notes", models.JSONField(blank=True,default=dict)), ("active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("channel", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name="strategy",to="ai.contentchannel")),
            ],
        ),
        migrations.CreateModel(
            name="ContentResearchSnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("query", models.CharField(max_length=300)), ("source", models.CharField(max_length=120)), ("url", models.URLField(blank=True)),
                ("title", models.CharField(blank=True,max_length=300)), ("summary", models.TextField(blank=True)), ("metrics", models.JSONField(blank=True,default=dict)),
                ("captured_at", models.DateTimeField(auto_now_add=True)),
                ("channel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="research_snapshots",to="ai.contentchannel")),
            ],
            options={"ordering":("-captured_at",)},
        ),
        migrations.CreateModel(
            name="ContentBrief",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("topic", models.CharField(max_length=300)), ("objective", models.CharField(blank=True,max_length=200)),
                ("format", models.CharField(default="short_video",max_length=80)), ("angle", models.TextField(blank=True)),
                ("audience_pain", models.TextField(blank=True)), ("hook", models.TextField(blank=True)), ("call_to_action", models.TextField(blank=True)),
                ("keywords", models.JSONField(blank=True,default=list)), ("status", models.CharField(choices=[("idea","Idea"),("research","Research"),("briefed","Briefed"),("drafting","Drafting"),("review","Review"),("approved","Approved"),("scheduled","Scheduled"),("published","Published"),("failed","Failed")],default="idea",max_length=20)),
                ("scorecard", models.JSONField(blank=True,default=dict)), ("owner_approved", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("channel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="briefs",to="ai.contentchannel")),
                ("created_by", models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering":["-created_at"]} if False else {},
        ),
        migrations.CreateModel(
            name="ContentAsset",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("asset_type", models.CharField(choices=[("script","Script"),("caption","Caption"),("title","Title"),("description","Description"),("thumbnail_prompt","Thumbnail prompt"),("hashtags","Hashtags"),("carousel","Carousel"),("image_prompt","Image prompt")],max_length=40)),
                ("version", models.PositiveIntegerField(default=1)), ("body", models.TextField()), ("metadata", models.JSONField(blank=True,default=dict)), ("approved", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)),
                ("brief", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="assets",to="ai.contentbrief")),
            ],
            options={"ordering":["asset_type","-version"]},
        ),
        migrations.CreateModel(
            name="ContentPublication",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("scheduled_for", models.DateTimeField(blank=True,null=True)), ("status", models.CharField(choices=[("queued","Queued"),("scheduled","Scheduled"),("publishing","Publishing"),("published","Published"),("failed","Failed"),("cancelled","Cancelled")],default="queued",max_length=20)),
                ("provider", models.CharField(default="manual",max_length=60)), ("external_id", models.CharField(blank=True,max_length=180)),
                ("idempotency_key", models.CharField(max_length=180,unique=True)), ("response_metadata", models.JSONField(blank=True,default=dict)), ("owner_approved", models.BooleanField(default=False)), ("published_at", models.DateTimeField(blank=True,null=True)), ("created_at", models.DateTimeField(auto_now_add=True)),
                ("brief", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="publications",to="ai.contentbrief")),
                ("channel", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="publications",to="ai.contentchannel")),
            ],
            options={"ordering":["-created_at"]},
        ),
        migrations.CreateModel(
            name="ContentPerformance",
            fields=[
                ("id", models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
                ("impressions", models.PositiveBigIntegerField(default=0)), ("views", models.PositiveBigIntegerField(default=0)),
                ("likes", models.PositiveBigIntegerField(default=0)), ("comments", models.PositiveBigIntegerField(default=0)), ("shares", models.PositiveBigIntegerField(default=0)),
                ("saves", models.PositiveBigIntegerField(default=0)), ("watch_time_seconds", models.FloatField(default=0)), ("retention_percent", models.FloatField(default=0)),
                ("click_through_rate", models.FloatField(default=0)), ("followers_gained", models.IntegerField(default=0)), ("captured_at", models.DateTimeField(auto_now=True)),
                ("publication", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name="performance",to="ai.contentpublication")),
            ],
        ),
        migrations.AddConstraint(
            model_name="contentchannel",
            constraint=models.UniqueConstraint(fields=("platform","name"),name="ai_channel_platform_name_uniq"),
        ),
        migrations.AddConstraint(
            model_name="contentasset",
            constraint=models.UniqueConstraint(fields=("brief","asset_type","version"),name="ai_content_asset_version_uniq"),
        ),
    ]
