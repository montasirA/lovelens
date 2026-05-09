from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from .forms import AnalysisForm
from .models import AnalysisReport
from .services import AnalysisInput, analyze_relationship


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class PrivacyView(TemplateView):
    template_name = "privacy.html"


class TermsView(TemplateView):
    template_name = "terms.html"


class AnalyzeView(FormView):
    template_name = "analyzer/analyze.html"
    form_class = AnalysisForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.session.get("anonymous_analysis_used"):
            messages.info(request, "Anonymous users can analyze once. Create a free account for unlimited LoveLens reports.")
            return redirect("register")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cleaned = form.cleaned_data
        result = analyze_relationship(AnalysisInput(**cleaned))
        report = AnalysisReport.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            input_type=cleaned["input_type"],
            raw_text=cleaned["raw_text"],
            partner_name=cleaned.get("partner_name", ""),
            relationship_duration=cleaned.get("relationship_duration", ""),
            **result,
        )
        if not self.request.user.is_authenticated:
            self.request.session["anonymous_analysis_used"] = True
            self.request.session["anonymous_report_id"] = report.pk
        messages.success(self.request, "Your LoveLens analysis is ready.")
        return redirect(report.get_absolute_url())

    def get_success_url(self):
        return reverse("dashboard")
