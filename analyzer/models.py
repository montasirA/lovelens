from django.conf import settings
from django.db import models
from django.urls import reverse


class AnalysisReport(models.Model):
    RELATIONSHIP_DESCRIPTION = "description"
    CHAT_CONVERSATION = "chat"
    INPUT_TYPES = (
        (RELATIONSHIP_DESCRIPTION, "Relationship Description"),
        (CHAT_CONVERSATION, "Chat Conversation"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="analysis_reports")
    title = models.CharField(max_length=160)
    input_type = models.CharField(max_length=32, choices=INPUT_TYPES)
    raw_text = models.TextField()
    partner_name = models.CharField(max_length=120, blank=True)
    relationship_duration = models.CharField(max_length=120, blank=True)
    summary = models.TextField()
    relationship_health_score = models.PositiveSmallIntegerField(default=0)
    toxicity_score = models.PositiveSmallIntegerField(default=0)
    emotional_safety_score = models.PositiveSmallIntegerField(default=0)
    compatibility_score = models.PositiveSmallIntegerField(default=0)
    narcissism_score = models.PositiveSmallIntegerField(default=0)
    manipulation_score = models.PositiveSmallIntegerField(default=0)
    trust_score = models.PositiveSmallIntegerField(default=0)
    communication_score = models.PositiveSmallIntegerField(default=0)
    attachment_style = models.CharField(max_length=180, blank=True)
    red_flags = models.JSONField(default=list, blank=True)
    yellow_flags = models.JSONField(default=list, blank=True)
    green_flags = models.JSONField(default=list, blank=True)
    narcissistic_traits = models.JSONField(default=list, blank=True)
    gaslighting_patterns = models.JSONField(default=list, blank=True)
    strengths = models.JSONField(default=list, blank=True)
    risks = models.JSONField(default=list, blank=True)
    advice = models.JSONField(default=list, blank=True)
    boundary_suggestions = models.JSONField(default=list, blank=True)
    recommended_questions = models.JSONField(default=list, blank=True)
    urgent_warning = models.TextField(blank=True)
    overall_verdict = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("report_detail", kwargs={"pk": self.pk})
