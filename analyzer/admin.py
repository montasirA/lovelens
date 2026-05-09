from django.contrib import admin

from .models import AnalysisReport


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "input_type", "relationship_health_score", "toxicity_score", "created_at")
    list_filter = ("input_type", "created_at")
    search_fields = ("title", "summary", "raw_text", "partner_name")
