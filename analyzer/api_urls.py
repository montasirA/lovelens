from django.urls import path

from .api_views import AnalysisAPIView

urlpatterns = [
    path("analyze/", AnalysisAPIView.as_view(), name="api_analyze"),
]
