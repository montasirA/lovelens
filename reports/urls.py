from django.urls import path

from .views import ReportDeleteView, ReportDetailView, ReportListView

urlpatterns = [
    path("history/", ReportListView.as_view(), name="report_history"),
    path("<int:pk>/", ReportDetailView.as_view(), name="report_detail"),
    path("<int:pk>/delete/", ReportDeleteView.as_view(), name="report_delete"),
]
