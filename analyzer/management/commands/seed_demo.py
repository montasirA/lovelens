from django.core.management.base import BaseCommand

from accounts.models import CustomUser
from analyzer.models import AnalysisReport
from analyzer.services import AnalysisInput, analyze_relationship


class Command(BaseCommand):
    help = "Create a demo user and sample LoveLens report."

    def handle(self, *args, **options):
        user, _ = CustomUser.objects.get_or_create(username="demo", defaults={"email": "demo@lovelens.app"})
        user.set_password("demo12345")
        user.save()
        if not AnalysisReport.objects.filter(user=user).exists():
            raw_text = (
                "My partner apologized after an argument and said they want to communicate better, "
                "but they also check my phone, get jealous about friends, and sometimes say I am too sensitive "
                "when I bring up things they said."
            )
            result = analyze_relationship(AnalysisInput(raw_text=raw_text, input_type="description", partner_name="Alex", relationship_duration="8 months"))
            AnalysisReport.objects.create(user=user, input_type="description", raw_text=raw_text, partner_name="Alex", relationship_duration="8 months", **result)
        self.stdout.write(self.style.SUCCESS("Demo user ready: demo / demo12345"))
