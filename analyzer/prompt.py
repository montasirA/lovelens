SYSTEM_PROMPT = """You are an expert relationship communication analyst.

Your task is to analyze a user's relationship description or conversation and identify behavioral patterns based only on the provided evidence.

Rules:
1. Never provide a medical or psychological diagnosis.
2. Use cautious language.
3. Highlight both positive and negative patterns.
4. Return valid JSON only.
5. Scores must be integers from 0 to 100.
6. Explain findings clearly and compassionately.
7. If evidence is weak, say so.
8. If there are severe warning signs (abuse, threats, coercion), set urgent_warning.
9. Analyze narcissistic traits, manipulation, gaslighting, love bombing, controlling behavior, emotional unavailability, dishonesty, boundary violations, attachment indicators, and communication problems only when evidence appears in the text.
10. Use phrases such as "possible indicators", "patterns consistent with", and "likelihood" instead of diagnosis language.
"""

JSON_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "title",
        "summary",
        "relationship_health_score",
        "toxicity_score",
        "emotional_safety_score",
        "compatibility_score",
        "narcissism_score",
        "manipulation_score",
        "trust_score",
        "communication_score",
        "attachment_style",
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
        "urgent_warning",
        "overall_verdict",
    ],
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "relationship_health_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "toxicity_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "emotional_safety_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "compatibility_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "narcissism_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "manipulation_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "trust_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "communication_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "attachment_style": {"type": "string"},
        "red_flags": {"type": "array", "items": {"type": "string"}},
        "yellow_flags": {"type": "array", "items": {"type": "string"}},
        "green_flags": {"type": "array", "items": {"type": "string"}},
        "narcissistic_traits": {"type": "array", "items": {"type": "string"}},
        "gaslighting_patterns": {"type": "array", "items": {"type": "string"}},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "advice": {"type": "array", "items": {"type": "string"}},
        "boundary_suggestions": {"type": "array", "items": {"type": "string"}},
        "recommended_questions": {"type": "array", "items": {"type": "string"}},
        "urgent_warning": {"type": "string"},
        "overall_verdict": {"type": "string"},
    },
}
