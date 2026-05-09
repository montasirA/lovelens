from django import forms

from .models import AnalysisReport


class AnalysisForm(forms.Form):
    input_type = forms.ChoiceField(choices=AnalysisReport.INPUT_TYPES)
    partner_name = forms.CharField(max_length=120, required=False)
    relationship_duration = forms.CharField(max_length=120, required=False)
    raw_text = forms.CharField(
        min_length=80,
        max_length=24000,
        widget=forms.Textarea(attrs={"rows": 14, "data-counter": "analysis-counter"}),
        help_text="Paste at least 80 characters. Remove phone numbers, addresses, and other private details when possible.",
    )

    def clean_raw_text(self):
        value = self.cleaned_data["raw_text"].strip()
        if len(value.split()) < 15:
            raise forms.ValidationError("Please add more context so LoveLens can analyze meaningful patterns.")
        return value
