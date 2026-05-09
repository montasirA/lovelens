from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView, DetailView, ListView

from analyzer.models import AnalysisReport


class ReportAccessMixin:
    model = AnalysisReport

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        report_id = self.request.session.get("anonymous_report_id")
        return qs.filter(pk=report_id, user__isnull=True)


class ReportListView(LoginRequiredMixin, ListView):
    model = AnalysisReport
    template_name = "reports/history.html"
    context_object_name = "reports"

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user)


class ReportDetailView(ReportAccessMixin, DetailView):
    template_name = "reports/detail.html"
    context_object_name = "report"


class ReportDeleteView(ReportAccessMixin, DeleteView):
    success_url = "/reports/history/"
    template_name = "reports/confirm_delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Report deleted.")
        return super().form_valid(form)
