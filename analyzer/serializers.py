from rest_framework import serializers

from .forms import AnalysisForm
from .models import AnalysisReport
from .services import AnalysisInput, analyze_relationship


class AnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = "__all__"
        read_only_fields = ("user", "created_at")


class AnalysisRequestSerializer(serializers.Serializer):
    input_type = serializers.ChoiceField(choices=AnalysisReport.INPUT_TYPES)
    partner_name = serializers.CharField(required=False, allow_blank=True, max_length=120)
    relationship_duration = serializers.CharField(required=False, allow_blank=True, max_length=120)
    raw_text = serializers.CharField(min_length=80, max_length=24000)

    def validate(self, attrs):
        form = AnalysisForm(data=attrs)
        if not form.is_valid():
            raise serializers.ValidationError(form.errors)
        return form.cleaned_data

    def create(self, validated_data):
        request = self.context["request"]
        result = analyze_relationship(AnalysisInput(**validated_data))
        report = AnalysisReport.objects.create(
            user=request.user if request.user.is_authenticated else None,
            input_type=validated_data["input_type"],
            raw_text=validated_data["raw_text"],
            partner_name=validated_data.get("partner_name", ""),
            relationship_duration=validated_data.get("relationship_duration", ""),
            **result,
        )
        return report
