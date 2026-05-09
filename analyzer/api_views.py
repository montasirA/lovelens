from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AnalysisReportSerializer, AnalysisRequestSerializer


class AnalysisAPIView(APIView):
    throttle_scope = "user"

    def post(self, request):
        serializer = AnalysisRequestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        if not request.user.is_authenticated and request.session.get("anonymous_analysis_used"):
            return Response({"detail": "Anonymous users can analyze once. Create a free account for unlimited analyses."}, status=status.HTTP_403_FORBIDDEN)
        report = serializer.save()
        if not request.user.is_authenticated:
            request.session["anonymous_analysis_used"] = True
            request.session["anonymous_report_id"] = report.pk
        return Response(AnalysisReportSerializer(report).data, status=status.HTTP_201_CREATED)
