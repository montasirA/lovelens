# 💖 LoveLens  
### 🔍 AI-Powered Relationship Analysis Platform  
**Author:** Montasir Arafin Tasin

---

## 🌟 About LoveLens

**LoveLens** is a production-ready **Django 5** web application that uses AI to analyze romantic relationships and communication patterns.

Users can paste a relationship story, chat conversation, or situation description and instantly receive:

- ❤️ Relationship health scores
- ⚠️ Toxicity detection
- 🛡️ Emotional safety assessment
- 🤝 Compatibility analysis
- 🧠 Narcissism likelihood
- 🎭 Manipulation and gaslighting detection
- 💬 Personalized advice
- 🚧 Healthy boundary suggestions
- ❓ Recommended questions to ask a partner
- 📜 Saved report history

> ⚠️ **Disclaimer:** LoveLens is for educational and informational purposes only. It is **not therapy**, **legal advice**, **medical advice**, or a **clinical diagnosis**.

---

## ✨ Features

### 👤 Authentication & User System
- ✅ User registration
- ✅ Login and logout
- ✅ Password reset
- ✅ Personal dashboard

### 🆓 Anonymous Access
- 🔍 Guest users can perform **one free analysis**

### 🔐 Registered Users
- ♾️ Unlimited relationship analyses
- ♾️ Unlimited report history

### 🤖 AI Analysis Engine
- 🧠 OpenAI structured JSON output
- 🛠️ Local fallback mode for development

### 📊 Detailed Scoring
- ❤️ Relationship Health Score
- ☠️ Toxicity Score
- 🛡️ Emotional Safety Score
- 💞 Compatibility Score
- 🎭 Narcissism Likelihood
- 🕵️ Manipulation Score
- 🤝 Trust Score
- 🗣️ Communication Score

### 🚩 Behavioral Insights
- 🔴 Red Flags
- 🟡 Yellow Flags
- 🟢 Green Flags
- 🎭 Narcissistic Traits
- 🧠 Gaslighting Patterns
- ⚠️ Risks and Warnings
- 💪 Relationship Strengths

### 🧭 Actionable Guidance
- 💡 Personalized Advice
- 🚧 Boundary Recommendations
- ❓ Important Questions to Ask

### 🔌 API Support
- 🌐 REST API endpoint at `/api/analyze/`

---

## 🚀 Local Setup

```bash
cd lovelens
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
