# Generated for LoveLens.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AnalysisReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("input_type", models.CharField(choices=[("description", "Relationship Description"), ("chat", "Chat Conversation")], max_length=32)),
                ("raw_text", models.TextField()),
                ("partner_name", models.CharField(blank=True, max_length=120)),
                ("relationship_duration", models.CharField(blank=True, max_length=120)),
                ("summary", models.TextField()),
                ("relationship_health_score", models.PositiveSmallIntegerField(default=0)),
                ("toxicity_score", models.PositiveSmallIntegerField(default=0)),
                ("emotional_safety_score", models.PositiveSmallIntegerField(default=0)),
                ("compatibility_score", models.PositiveSmallIntegerField(default=0)),
                ("narcissism_score", models.PositiveSmallIntegerField(default=0)),
                ("manipulation_score", models.PositiveSmallIntegerField(default=0)),
                ("trust_score", models.PositiveSmallIntegerField(default=0)),
                ("communication_score", models.PositiveSmallIntegerField(default=0)),
                ("attachment_style", models.CharField(blank=True, max_length=180)),
                ("red_flags", models.JSONField(blank=True, default=list)),
                ("yellow_flags", models.JSONField(blank=True, default=list)),
                ("green_flags", models.JSONField(blank=True, default=list)),
                ("narcissistic_traits", models.JSONField(blank=True, default=list)),
                ("gaslighting_patterns", models.JSONField(blank=True, default=list)),
                ("strengths", models.JSONField(blank=True, default=list)),
                ("risks", models.JSONField(blank=True, default=list)),
                ("advice", models.JSONField(blank=True, default=list)),
                ("boundary_suggestions", models.JSONField(blank=True, default=list)),
                ("recommended_questions", models.JSONField(blank=True, default=list)),
                ("urgent_warning", models.TextField(blank=True)),
                ("overall_verdict", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="analysis_reports", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
