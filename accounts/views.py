from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from analyzer.models import AnalysisReport

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Welcome to LoveLens. Your account is ready.")
        return response

    def get_success_url(self):
        return "/accounts/dashboard/"


@login_required
def dashboard(request):
    reports = AnalysisReport.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "accounts/dashboard.html", {"reports": reports})
