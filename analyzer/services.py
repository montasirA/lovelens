import json
import re
from dataclasses import dataclass

from django.conf import settings
from openai import OpenAI

from .prompt import JSON_SCHEMA, SYSTEM_PROMPT

LIST_FIELDS = [
    "red_flags",
    "yellow_flags",
    "green_flags",
    "narcissistic_traits",
    "gaslighting_patterns",
    "strengths",
    "risks",
    "advice",
    "boundary_suggestions",
    "recommended_questions",
]
SCORE_FIELDS = [
    "relationship_health_score",
    "toxicity_score",
    "emotional_safety_score",
    "compatibility_score",
    "narcissism_score",
    "manipulation_score",
    "trust_score",
    "communication_score",
]


@dataclass
class AnalysisInput:
    raw_text: str
    input_type: str
    partner_name: str = ""
    relationship_duration: str = ""


def analyze_relationship(payload: AnalysisInput) -> dict:
    if settings.OPENAI_API_KEY:
        return _analyze_with_openai(payload)
    return _local_evidence_based_fallback(payload)


def _analyze_with_openai(payload: AnalysisInput) -> dict:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    user_prompt = (
        f"Input type: {payload.input_type}\n"
        f"Partner nickname: {payload.partner_name or 'Not provided'}\n"
        f"Relationship duration: {payload.relationship_duration or 'Not provided'}\n\n"
        f"Text to analyze:\n{payload.raw_text}"
    )
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "relationship_analysis",
                "schema": JSON_SCHEMA,
                "strict": True,
            }
        },
    )
    return normalize_analysis(json.loads(response.choices[0].message.content))


def normalize_analysis(data: dict) -> dict:
    normalized = dict(data or {})
    for field in SCORE_FIELDS:
        try:
            normalized[field] = max(0, min(100, int(normalized.get(field, 0))))
        except (TypeError, ValueError):
            normalized[field] = 0
    for field in LIST_FIELDS:
        value = normalized.get(field, [])
        normalized[field] = value if isinstance(value, list) else [str(value)]
    for field in ["title", "summary", "attachment_style", "urgent_warning", "overall_verdict"]:
        normalized[field] = str(normalized.get(field, "") or "")
    if not normalized["title"]:
        normalized["title"] = "Relationship Analysis"
    return normalized


def _local_evidence_based_fallback(payload: AnalysisInput) -> dict:
    text = payload.raw_text.lower()
    patterns = {
        "red_flags": [
            (r"\b(threat|hit|afraid|scared|unsafe|force|coerc|blackmail)\b", "Possible safety risk or coercive behavior appears in the text."),
            (r"\b(i never said|you're crazy|you are crazy|imagining|too sensitive)\b", "Language appears consistent with gaslighting or reality-denying behavior."),
            (r"\b(check your phone|share your password|where are you|who are you with)\b", "Possible controlling or monitoring behavior is present."),
        ],
        "yellow_flags": [
            (r"\b(silent treatment|ignore me|ignored me|stonewall)\b", "Stonewalling or withdrawal may be affecting communication."),
            (r"\b(jealous|jealousy|insecure|accuse)\b", "Jealousy or repeated accusations may be creating trust pressure."),
            (r"\b(lied|lying|secret|hidden|hide)\b", "Secrecy or dishonesty patterns may need direct clarification."),
        ],
        "green_flags": [
            (r"\b(apologized|sorry|listened|understood|respect|safe|support)\b", "There is evidence of repair, support, or respect."),
            (r"\b(boundary|space|honest|talk calmly|communicate)\b", "The text includes signs of boundary awareness or constructive communication."),
        ],
        "narcissistic_traits": [
            (r"\b(my fault|blame me|blames me|never wrong|entitled|superior)\b", "Possible indicators of blame shifting or entitlement."),
            (r"\b(all about them|only talks about|no empathy|doesn't care)\b", "Possible indicators of self-focus or low empathy."),
        ],
        "gaslighting_patterns": [
            (r"\b(i never said|that never happened|you made it up|remember wrong)\b", "Denying or rewriting events may be present."),
            (r"\b(too sensitive|overreacting|crazy|dramatic)\b", "Minimizing your perception may be present."),
        ],
    }
    found = {key: _find_matches(text, checks) for key, checks in patterns.items()}
    risk_count = len(found["red_flags"]) + len(found["yellow_flags"]) + len(found["narcissistic_traits"]) + len(found["gaslighting_patterns"])
    positive_count = max(1, len(found["green_flags"]))
    toxicity = min(100, 20 + risk_count * 12)
    safety = max(0, 88 - risk_count * 10)
    health = max(0, min(100, 70 + positive_count * 5 - risk_count * 8))
    urgent = ""
    if re.search(r"\b(threat|hit|afraid|scared|unsafe|force|coerc|blackmail)\b", text):
        urgent = "This text includes possible severe warning signs. Consider prioritizing your immediate safety and speaking with trusted support or local emergency resources."
    return normalize_analysis(
        {
            "title": f"LoveLens analysis{f' for {payload.partner_name}' if payload.partner_name else ''}",
            "summary": "This development fallback analyzed visible keywords and patterns only. Add an OpenAI API key in production for deeper contextual analysis.",
            "relationship_health_score": health,
            "toxicity_score": toxicity,
            "emotional_safety_score": safety,
            "compatibility_score": max(0, health - 5),
            "narcissism_score": min(100, len(found["narcissistic_traits"]) * 28),
            "manipulation_score": min(100, (len(found["red_flags"]) + len(found["gaslighting_patterns"])) * 22),
            "trust_score": max(0, 82 - risk_count * 9),
            "communication_score": max(0, 76 - len(found["yellow_flags"]) * 12),
            "attachment_style": "Evidence is limited; possible anxious, avoidant, secure, or mixed indicators should be interpreted cautiously.",
            "red_flags": found["red_flags"],
            "yellow_flags": found["yellow_flags"],
            "green_flags": found["green_flags"] or ["Some context was provided, which is a useful first step toward clarity."],
            "narcissistic_traits": found["narcissistic_traits"],
            "gaslighting_patterns": found["gaslighting_patterns"],
            "strengths": found["green_flags"] or ["Willingness to reflect on the relationship."],
            "risks": found["red_flags"] + found["yellow_flags"],
            "advice": [
                "Look for repeated patterns over time rather than judging the relationship from one message.",
                "Name one concrete behavior you need to change and ask for a specific repair.",
                "If you feel unsafe, prioritize support from trusted people or local services.",
            ],
            "boundary_suggestions": [
                "I am willing to talk when we both stay respectful and do not insult each other.",
                "I need privacy with my phone and friendships; monitoring is not okay with me.",
            ],
            "recommended_questions": [
                "What do you think each of us needs to feel emotionally safe?",
                "How will we repair conflict when one of us feels hurt?",
                "What boundaries are non-negotiable for both of us?",
            ],
            "urgent_warning": urgent,
            "overall_verdict": "Use this as a reflective starting point, not a diagnosis. The strongest conclusions should come from repeated, specific evidence.",
        }
    )


def _find_matches(text: str, checks: list[tuple[str, str]]) -> list[str]:
    return [message for pattern, message in checks if re.search(pattern, text)]
