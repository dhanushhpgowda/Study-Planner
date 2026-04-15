# ◈ StudyMind — AI-Powered Personalized Study Planner

> A smart study assistant that builds personalized day-by-day exam schedules using Claude AI.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Claude AI](https://img.shields.io/badge/Claude-AI-orange)

---

## Features

- **AI-Generated Study Schedules** — Claude builds a balanced day-by-day plan based on your subjects, exam date, and difficulty
- **Missed Day Recovery** — Smart rescheduler redistributes load without overwhelming future days
- **Progress Dashboard** — Streaks, topic completion tracking, visual progress bars
- **PDF Export** — Download your full schedule as a clean, printable PDF
- **AI Study Chat** — Context-aware chatbot that knows your subjects and plan
- **Email Reminders** — Daily digest sent to your inbox every morning

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Flask 3.0 |
| Database | PostgreSQL + SQLAlchemy |
| AI | Anthropic Claude API |
| Email | Flask-Mail + APScheduler |
| PDF | ReportLab |
| Frontend | Jinja2 + Vanilla JS |

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 14+

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/study-planner.git
cd study-planner

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials and Anthropic API key

# 5. Create the database
createdb study_planner

# 6. Run migrations
flask db init
flask db migrate -m "Initial models"
flask db upgrade

# 7. Run the app
flask run
```

Visit `http://localhost:5000`

---

## Project Structure

```
study-planner/
├── app.py                  # Flask app factory
├── config.py               # Environment configuration
├── extensions.py           # Flask extensions
├── models.py               # Database models
├── requirements.txt
├── .env.example
├── routes/
│   ├── main.py             # Landing page
│   ├── planner.py          # Schedule generation (Day 2)
│   ├── tracker.py          # Progress tracking (Day 3)
│   ├── export.py           # PDF export (Day 4)
│   ├── chat.py             # AI assistant (Day 5)
│   └── notifications.py    # Email reminders (Day 6)
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
└── static/
    ├── css/style.css
    └── js/
```

---

## Development Roadmap

| Day | Feature | Status |
|-----|---------|--------|
| 1 | Project setup, DB models, landing page | ✅ Done |
| 2 | AI schedule generator | ✅ Done |
| 3 | Progress tracker dashboard | ✅ Done |
| 4 | Missed day rescheduler + PDF export | ✅ Done |
| 5 | AI study chat assistant | ✅ Done |
| 6 | Email reminder system | ⏳ Pending |
| 7 | Polish, tests, deploy-ready | ⏳ Pending |

---

## License

MIT