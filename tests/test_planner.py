import pytest
from datetime import date, timedelta
from app import create_app
from extensions import db
from models import User, StudyPlan, Subject, StudySession


@pytest.fixture
def app():
    app = create_app("development")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


class TestPromptBuilder:
    def test_prompt_contains_student_name(self, app):
        with app.app_context():
            from services.planner_service import build_prompt
            subjects = [{
                "name": "Physics",
                "difficulty": 2,
                "difficulty_label": "Medium",
                "topics": "Kinematics"
            }]
            prompt = build_prompt(
                subjects,
                date.today() + timedelta(days=10),
                4.0,
                "Arjun"
            )
            assert "Arjun" in prompt

    def test_prompt_contains_subject(self, app):
        with app.app_context():
            from services.planner_service import build_prompt
            subjects = [{
                "name": "Chemistry",
                "difficulty": 3,
                "difficulty_label": "Hard",
                "topics": "Organic"
            }]
            prompt = build_prompt(
                subjects,
                date.today() + timedelta(days=7),
                3.0,
                "Test"
            )
            assert "Chemistry" in prompt
            assert "Hard" in prompt

    def test_prompt_contains_exam_date(self, app):
        with app.app_context():
            from services.planner_service import build_prompt
            exam = date.today() + timedelta(days=5)
            subjects = [{
                "name": "Maths",
                "difficulty": 1,
                "difficulty_label": "Easy",
                "topics": ""
            }]
            prompt = build_prompt(subjects, exam, 2.0, "Test")
            assert exam.strftime("%B") in prompt

    def test_prompt_contains_daily_hours(self, app):
        with app.app_context():
            from services.planner_service import build_prompt
            subjects = [{
                "name": "Biology",
                "difficulty": 2,
                "difficulty_label": "Medium",
                "topics": ""
            }]
            prompt = build_prompt(
                subjects,
                date.today() + timedelta(days=10),
                6.0,
                "Test"
            )
            assert "6.0" in prompt


class TestSessionsToDb:
    def test_sessions_saved_correctly(self, app):
        with app.app_context():
            user = User(name="Test", email="planner@test.com")
            db.session.add(user)
            db.session.flush()

            plan = StudyPlan(
                user_id=user.id,
                title="Test Plan",
                exam_date=date.today() + timedelta(days=7),
                daily_hours=4.0,
            )
            db.session.add(plan)
            db.session.flush()

            subject = Subject(plan_id=plan.id, name="Maths", difficulty=2)
            db.session.add(subject)
            db.session.commit()

            subjects_map = {"maths": subject.id}

            sessions_json = [
                {
                    "day_number": 1,
                    "date": (date.today() + timedelta(days=1)).isoformat(),
                    "subject": "Maths",
                    "topic": "Algebra basics",
                    "duration_minutes": 60,
                    "session_type": "study",
                    "tip": "Use flashcards",
                },
                {
                    "day_number": 2,
                    "date": (date.today() + timedelta(days=2)).isoformat(),
                    "subject": "Maths",
                    "topic": "Calculus intro",
                    "duration_minutes": 90,
                    "session_type": "revision",
                    "tip": "Practice problems",
                },
            ]

            from services.planner_service import sessions_to_db
            sessions_to_db(sessions_json, plan, subjects_map)

            saved = StudySession.query.filter_by(plan_id=plan.id).all()
            assert len(saved) == 2
            assert saved[0].topic == "Algebra basics"
            assert saved[1].duration_minutes == 90
            assert saved[0].subject_id == subject.id


class TestRescheduler:
    def test_no_missed_sessions(self, app):
        with app.app_context():
            user = User(name="Test", email="reschedule@test.com")
            db.session.add(user)
            db.session.flush()

            plan = StudyPlan(
                user_id=user.id,
                title="Reschedule Test",
                exam_date=date.today() + timedelta(days=10),
                daily_hours=4.0,
            )
            db.session.add(plan)
            db.session.commit()

            from services.rescheduler import reschedule_missed
            result = reschedule_missed(plan.id)
            assert result["rescheduled"] == 0

    def test_get_missed_sessions_empty(self, app):
        with app.app_context():
            user = User(name="Test2", email="missed@test.com")
            db.session.add(user)
            db.session.flush()

            plan = StudyPlan(
                user_id=user.id,
                title="Miss Test",
                exam_date=date.today() + timedelta(days=10),
                daily_hours=4.0,
            )
            db.session.add(plan)
            db.session.commit()

            from services.rescheduler import get_missed_sessions
            missed = get_missed_sessions(plan.id)
            assert missed == []


class TestGetSessionsByDay:
    def test_groups_correctly(self, app):
        with app.app_context():
            user = User(name="Group", email="group@test.com")
            db.session.add(user)
            db.session.flush()

            plan = StudyPlan(
                user_id=user.id,
                title="Group Test",
                exam_date=date.today() + timedelta(days=5),
                daily_hours=3.0,
            )
            db.session.add(plan)
            db.session.flush()

            for i in range(3):
                s = StudySession(
                    plan_id=plan.id,
                    day_number=1 if i < 2 else 2,
                    date=date.today() + timedelta(days=i),
                    topic=f"Topic {i}",
                    duration_minutes=60,
                    session_type="study",
                )
                db.session.add(s)
            db.session.commit()

            from services.planner_service import get_sessions_by_day
            days = get_sessions_by_day(plan.id)
            assert len(days[1]) == 2
            assert len(days[2]) == 1