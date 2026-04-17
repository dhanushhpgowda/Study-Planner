# ◈ StudyMind — AI-Powered Personalized Study Planner

> A smart study assistant that builds personalized day-by-day exam schedules using Groq AI (Llama 3.3 70B), tracks your progress, reminds you daily, and lets you chat with an AI tutor — all in one beautiful app.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square)
![Groq AI](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## What is StudyMind?

StudyMind is a full-stack web application that helps students prepare for exams by generating intelligent, personalized study schedules. Instead of manually planning your study sessions, you tell StudyMind your subjects, exam date, and available hours — and the AI does the rest.

---

## Features

| Feature | Description |
|---------|-------------|
| AI Schedule Generator | Llama 3.3 70B builds a balanced day-by-day plan with harder subjects getting more time |
| Progress Dashboard | Visual streaks, weekly activity chart, subject-level progress bars |
| Missed Day Recovery | Smart rescheduler redistributes missed sessions without overloading future days |
| PDF Export | Download your full schedule as a clean, printable PDF |
| AI Study Chat | Context-aware chatbot that knows your subjects, plan, and progress |
| Daily Email Reminders | Morning digest sent at 7AM with today's sessions via Gmail SMTP |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Flask 3.0 |
| Database | PostgreSQL 16 + SQLAlchemy + Flask-Migrate |
| AI | Groq API — Llama 3.3 70B Versatile |
| Email | Flask-Mail + APScheduler |
| PDF | ReportLab |
| Frontend | Jinja2 + Vanilla JS |
| Testing | Pytest |

---

## Project Structure

```
study-planner/
├── app.py                    # Flask app factory
├── config.py                 # Environment config (dev/prod)
├── extensions.py             # Flask extensions (db, mail)
├── models.py                 # SQLAlchemy models
├── requirements.txt          # All dependencies
├── .env.example              # Environment variable template
├── routes/
│   ├── main.py               # Landing page + notification routes
│   ├── planner.py            # Schedule generation routes
│   ├── tracker.py            # Dashboard + progress routes
│   ├── export.py             # PDF export + reschedule routes
│   └── chat.py               # AI chat routes
├── services/
│   ├── planner_service.py    # Groq AI + schedule builder
│   ├── rescheduler.py        # Missed day recovery logic
│   ├── pdf_export.py         # ReportLab PDF generator
│   ├── chat_service.py       # AI chat context builder
│   ├── notifications.py      # Email builder + sender
│   └── scheduler_jobs.py     # APScheduler daily job
├── templates/
│   ├── base.html             # Base layout + navbar
│   ├── index.html            # Landing page
│   ├── plan_new.html         # Subject intake form
│   ├── plan_view.html        # Day-by-day schedule view
│   ├── plan_list.html        # All plans list
│   ├── dashboard.html        # Progress dashboard
│   ├── export.html           # Export + reschedule page
│   ├── chat.html             # AI chat interface
│   └── email_daily.html      # Email template reference
├── static/
│   ├── css/style.css         # Full design system
│   └── js/
│       ├── planner.js        # Dynamic form interactions
│       ├── progress.js       # Chart animations
│       └── chat.js           # Chat UI + API calls
└── tests/
    ├── test_models.py        # Model + route tests
    └── test_planner.py       # Service logic tests
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Groq API key (free at console.groq.com)
- Gmail account with App Password (for emails)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/study-planner.git
cd study-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 4. Create PostgreSQL database
psql -U postgres
CREATE DATABASE study_planner;
\q

# 5. Run migrations
python -m flask db init
python -m flask db migrate -m "Initial models"
python -m flask db upgrade

# 6. Start the app
python -m flask run
```

Visit `http://localhost:5000`

---

## Environment Variables

```env
SECRET_KEY=your-random-secret-key
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:password@localhost:5432/study_planner
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=your-16-char-app-password
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## App Routes

| Route | Description |
|-------|-------------|
| `GET /` | Landing page |
| `GET /plan/new` | Create new study plan form |
| `POST /plan/generate` | Generate AI schedule |
| `GET /plan/<id>` | View schedule |
| `GET /dashboard` | All plans list |
| `GET /dashboard/<id>` | Progress dashboard |
| `GET /plan/<id>/export/pdf` | Download PDF |
| `POST /plan/<id>/reschedule` | Reschedule missed sessions |
| `GET /chat/<id>` | AI chat interface |
| `POST /notifications/test/<id>` | Send test email |
| `GET /health` | Health check |

---

## Development Roadmap

| Day | Feature | Status |
|-----|---------|--------|
| 1 | Project setup, DB models, landing page | ✅ Done |
| 2 | AI schedule generator | ✅ Done |
| 3 | Progress tracker dashboard | ✅ Done |
| 4 | Missed day rescheduler + PDF export | ✅ Done |
| 5 | AI study chat assistant | ✅ Done |
| 6 | Email reminder system | ✅ Done |
| 7 | Polish, tests, deploy-ready | ✅ Done |

---

## License

MIT — feel free to use, modify, and distribute.