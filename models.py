from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    email_reminders = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    study_plans = db.relationship("StudyPlan", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name}>"


class StudyPlan(db.Model):
    __tablename__ = "study_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    daily_hours = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subjects = db.relationship("Subject", backref="plan", lazy=True, cascade="all, delete-orphan")
    sessions = db.relationship("StudySession", backref="plan", lazy=True, cascade="all, delete-orphan")

    @property
    def days_until_exam(self):
        today = datetime.utcnow().date()
        delta = self.exam_date - today
        return max(delta.days, 0)

    @property
    def total_sessions(self):
        return len(self.sessions)

    @property
    def completed_sessions(self):
        return sum(1 for s in self.sessions if s.completed)

    @property
    def progress_percent(self):
        if self.total_sessions == 0:
            return 0
        return round((self.completed_sessions / self.total_sessions) * 100)

    def __repr__(self):
        return f"<StudyPlan {self.title}>"


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("study_plans.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    # 1=Easy, 2=Medium, 3=Hard
    difficulty = db.Column(db.Integer, nullable=False, default=2)
    topics = db.Column(db.Text, nullable=True)  # comma-separated topics

    @property
    def topic_list(self):
        if not self.topics:
            return []
        return [t.strip() for t in self.topics.split(",") if t.strip()]

    @property
    def difficulty_label(self):
        return {1: "Easy", 2: "Medium", 3: "Hard"}.get(self.difficulty, "Medium")

    def __repr__(self):
        return f"<Subject {self.name}>"


class StudySession(db.Model):
    __tablename__ = "study_sessions"

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("study_plans.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    day_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    topic = db.Column(db.String(300), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    session_type = db.Column(db.String(50), default="study")  # study | revision | mock_test
    completed = db.Column(db.Boolean, default=False)
    missed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    subject = db.relationship("Subject", backref="sessions")

    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.utcnow()

    def mark_missed(self):
        self.missed = True

    def __repr__(self):
        return f"<StudySession Day{self.day_number}: {self.topic}>"