◈ StudyMind — AI-Powered Personalized Study Planner
Project Report | Full-Stack Web Application · Python · Flask · PostgreSQL · Groq AI | 2025
1. Executive Summary
StudyMind is a full-stack AI-powered web application designed to help students prepare for exams by generating intelligent, personalized study schedules. The system leverages the Groq API with Llama 3.3 70B to create balanced day-by-day study plans tailored to each student's subjects, difficulty levels, and available time.
The project was built over 7 days using Python and Flask as the backend framework, PostgreSQL for data persistence, and Vanilla JavaScript for frontend interactivity. It delivers six major features: AI schedule generation, progress tracking, missed-day recovery, PDF export, an in-app AI chat assistant, and daily email reminders.
Attribute
Details
Project Name
StudyMind — AI-Powered Personalized Study Planner
Technology Stack
Python 3.11, Flask 3.0, PostgreSQL, Groq AI (Llama 3.3 70B)
Development Duration
7 Days (1 feature per day)
Target Users
College students and exam-preparing individuals
Key Features
AI Schedule, Progress Dashboard, PDF Export, Chat, Email Reminders
Test Coverage
28 unit tests — 100% passing
2. Project Overview
2.1 Problem Statement
Students preparing for exams often struggle with structuring their study time effectively. Common challenges include uneven distribution of study time across subjects, difficulty prioritizing harder subjects, no clear recovery plan when a study day is missed, lack of motivation and progress visibility, and no personalized guidance aligned with exam timelines.
2.2 Proposed Solution
StudyMind addresses these challenges by acting as a personal AI study planner. Students input their exam details and subjects, and the AI generates a complete optimized schedule — automatically allocating more time to harder subjects, including revision sessions, and adapting when sessions are missed.
2.3 Goals and Objectives
Build a smart assistant that generates personalized study schedules using AI
Provide real-time progress tracking with visual dashboards
Enable recovery from missed study days without overloading future days
Allow students to download their schedule as a PDF
Offer an AI chat assistant for in-session academic support
Send automated daily email reminders to maintain study consistency
3. System Architecture
3.1 Technology Stack
Layer
Technology
Purpose
Backend
Python 3.11 + Flask 3.0
Web framework, routing, business logic
Database
PostgreSQL + SQLAlchemy
Data persistence, ORM, migrations
AI Engine
Groq API — Llama 3.3 70B
Schedule generation, chat assistant
Email
Flask-Mail + APScheduler
Daily reminders via Gmail SMTP at 7AM
PDF
ReportLab
Schedule export as downloadable PDF
Frontend
Jinja2 + Vanilla JS
Dynamic UI, form interactions, charts
Testing
Pytest
Unit tests for models, routes, services
3.2 Application Structure
Module
Responsibility
routes/main.py
Landing page, health check, notification controls
routes/planner.py
Plan creation form, schedule generation, session updates
routes/tracker.py
Progress dashboard, weekly activity, subject stats
routes/export.py
PDF download, missed session rescheduler
routes/chat.py
AI chat endpoint, quick tips generation
services/planner_service.py
Groq API integration, prompt builder, schedule parser
services/rescheduler.py
Missed day detection, smart session redistribution
services/pdf_export.py
ReportLab PDF document builder
services/chat_service.py
Chat context builder with plan-aware system prompt
services/notifications.py
HTML email builder, Flask-Mail sender
services/scheduler_jobs.py
APScheduler background job — daily 7AM trigger
4. Database Design
4.1 Entity Relationship Overview
User → has many StudyPlans
StudyPlan → has many Subjects and StudySessions
Subject → belongs to StudyPlan, has many StudySessions
StudySession → belongs to StudyPlan and Subject
4.2 Model Definitions
Model
Key Fields
Description
User
name, email
Stores student info and email reminder preferences
StudyPlan
title, exam_date, daily_hours
Master plan with exam details and computed progress stats
Subject
name, difficulty, topics
Subjects with difficulty (1=Easy, 2=Medium, 3=Hard)
StudySession
date, topic, duration, type
Study blocks with completion tracking and notes
5. Features and Implementation
5.1 AI Schedule Generator
The core feature of StudyMind. When a student submits the intake form, the system constructs a structured prompt containing the student name, exam date, available daily hours, list of subjects with difficulty levels and topics, and rules for smart distribution. The prompt is sent to Groq's Llama 3.3 70B model which returns a JSON array of study sessions. Each session includes a day number, date, subject, topic, duration in minutes, session type (study / revision / mock test), and a study tip.
5.2 Progress Tracker Dashboard
The dashboard provides a comprehensive view including a streak counter for consecutive days completed, an overall progress ring, a weekly activity bar chart, per-subject progress bars with total hours, today's sessions with done/skip actions, and total time studied.
5.3 Missed Day Recovery
When a student skips sessions, the rescheduler identifies all uncompleted past sessions, marks them as missed, finds future days with remaining capacity within the daily hour limit, and creates new rescheduled sessions tagged with their original date — without overloading any single day.
5.4 PDF Export
Students can download their complete study schedule as a professional PDF using ReportLab. It includes a cover summary table, day-by-day session tables with subject, topic, duration, type and status, colour-coded completion status, and repeating headers on every page.
5.5 AI Study Chat Assistant
An in-app chatbot powered by Groq that is context-aware of the student's plan. The system prompt includes the student name, exam date, days remaining, all subjects with difficulty, today's sessions, and overall progress. The chat maintains conversation history enabling multi-turn conversations.
5.6 Email Reminder System
A background APScheduler job runs daily at 7:00 AM sending personalised HTML emails containing a greeting, key stats (days until exam, progress, today's study load), a formatted session table, a call-to-action button, and a motivational quote.
6. Application Routes
Method
Route
Description
GET
/
Landing page
GET
/plan/new
Subject intake form
POST
/plan/generate
Generate AI schedule
GET
/plan/<id>
View day-by-day schedule
POST
/plan/<id>/session/<id>/complete
Mark session completed
POST
/plan/<id>/session/<id>/miss
Mark session skipped
GET
/dashboard
List all study plans
GET
/dashboard/<id>
Full progress dashboard
GET
/plan/<id>/export
Export and reschedule page
GET
/plan/<id>/export/pdf
Download PDF schedule
POST
/plan/<id>/reschedule
Reschedule missed sessions
GET
/chat/<id>
AI chat interface
POST
/chat/<id>/message
Send message to AI
GET
/chat/<id>/tips
Get AI quick tips
POST
/notifications/test/<id>
Send test reminder email
GET
/health
Health check endpoint
7. Development Timeline
Day
Feature
Files Created
Status
Day 1
Project foundation & database
app.py, models.py, config.py, index.html, style.css
✅ Complete
Day 2
AI schedule generator
planner_service.py, planner.py, plan_new.html, plan_view.html
✅ Complete
Day 3
Progress tracker dashboard
tracker.py, dashboard.html, plan_list.html, progress.js
✅ Complete
Day 4
Missed day recovery + PDF
rescheduler.py, pdf_export.py, export.py, export.html
✅ Complete
Day 5
AI study chat assistant
chat_service.py, chat.py, chat.html, chat.js
✅ Complete
Day 6
Email reminder system
notifications.py, scheduler_jobs.py, email_daily.html
✅ Complete
Day 7
Tests, polish, documentation
test_models.py, test_planner.py, conftest.py, README.md
✅ Complete
8. Testing
Test Class
Tests
Coverage
TestUserModel
2
User creation, repr method
TestStudyPlanModel
6
Days until exam, progress %, total/completed sessions
TestSubjectModel
3
Difficulty label, topic list parsing, empty topics
TestStudySessionModel
3
Mark complete, mark missed, repr method
TestRoutes
6
Index, new plan, dashboard, health, 404, session complete
TestPromptBuilder
4
Student name, subject, exam date, daily hours in prompt
TestSessionsToDb
1
JSON sessions saved correctly to database
TestRescheduler
2
No missed sessions case, empty missed list
TestGetSessionsByDay
1
Session grouping by day number
TOTAL
28
100% Passing
9. Setup and Installation
Prerequisites
Python 3.11+, PostgreSQL 14+, Groq API key, Gmail with App Password
Installation
Clone the repository and navigate to the project folder
Install dependencies: pip install -r requirements.txt
Copy .env.example to .env and fill in your credentials
Create the database: CREATE DATABASE study_planner;
Run migrations: flask db init → flask db migrate → flask db upgrade
Start the server: python -m flask run
Visit http://localhost:5000
Environment Variables
Variable
Description
SECRET_KEY
Flask secret key for session security
DATABASE_URL
PostgreSQL connection string
GROQ_API_KEY
Groq API key for AI features
MAIL_USERNAME
Gmail address for sending reminders
MAIL_PASSWORD
Gmail App Password (16-character)
10. Conclusion
StudyMind successfully delivers a production-quality AI-powered study planning application built from scratch in 7 days. Key technical achievements include seamless Groq AI integration with structured JSON output parsing, a smart rescheduler that redistributes missed sessions, a context-aware AI chat assistant with multi-turn conversation support, a ReportLab PDF generator, APScheduler background jobs, and 28 automated tests covering models, routes and service logic.
The codebase is modular, well-structured, and ready for deployment — making it an excellent portfolio project demonstrating full-stack development skills with AI integration.
◈ StudyMind · 2025 · Built with AI, for students