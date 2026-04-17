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
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_data(app):
    with app.app_context():
        user = User(name="Test Student", email="test@studymind.com")
        db.session.add(user)
        db.session.flush()

        plan = StudyPlan(
            user_id=user.id,
            title="Test Plan",
            exam_date=date.today() + timedelta(days=14),
            daily_hours=4.0,
        )
        db.session.add(plan)
        db.session.flush()

        subject = Subject(
            plan_id=plan.id,
            name="Mathematics",
            difficulty=3,
            topics="Calculus, Algebra",
        )
        db.session.add(subject)
        db.session.flush()

        session = StudySession(
            plan_id=plan.id,
            subject_id=subject.id,
            day_number=1,
            date=date.today(),
            topic="Introduction to Calculus",
            duration_minutes=90,
            session_type="study",
        )
        db.session.add(session)
        db.session.commit()

        return {
            "user_id": user.id,
            "plan_id": plan.id,
            "subject_id": subject.id,
            "session_id": session.id,
        }


class TestUserModel:
    def test_create_user(self, app):
        with app.app_context():
            user = User(name="Alice", email="alice@test.com")
            db.session.add(user)
            db.session.commit()
            assert user.id is not None
            assert user.name == "Alice"
            assert user.email_reminders is True

    def test_user_repr(self, app):
        with app.app_context():
            user = User(name="Bob", email="bob@test.com")
            db.session.add(user)
            db.session.commit()
            assert "Bob" in repr(user)


class TestStudyPlanModel:
    def test_create_plan(self, app, sample_data):
        with app.app_context():
            plan = StudyPlan.query.get(sample_data["plan_id"])
            assert plan is not None
            assert plan.title == "Test Plan"
            assert plan.daily_hours == 4.0

    def test_days_until_exam(self, app, sample_data):
        with app.app_context():
            plan = StudyPlan.query.get(sample_data["plan_id"])
            assert plan.days_until_exam == 14

    def test_progress_percent_zero(self, app, sample_data):
        with app.app_context():
            plan = StudyPlan.query.get(sample_data["plan_id"])
            assert plan.progress_percent == 0

    def test_progress_percent_after_complete(self, app, sample_data):
        with app.app_context():
            session = StudySession.query.get(sample_data["session_id"])
            session.mark_complete()
            db.session.commit()
            plan = StudyPlan.query.get(sample_data["plan_id"])
            assert plan.progress_percent == 100

    def test_total_sessions(self, app, sample_data):
        with app.app_context():
            plan = StudyPlan.query.get(sample_data["plan_id"])
            assert plan.total_sessions == 1

    def test_completed_sessions(self, app, sample_data):
        with app.app_context():
            plan = StudyPlan.query.get(sample_data["plan_id"])
            assert plan.completed_sessions == 0


class TestSubjectModel:
    def test_difficulty_label(self, app, sample_data):
        with app.app_context():
            subject = Subject.query.get(sample_data["subject_id"])
            assert subject.difficulty_label == "Hard"

    def test_topic_list(self, app, sample_data):
        with app.app_context():
            subject = Subject.query.get(sample_data["subject_id"])
            topics = subject.topic_list
            assert "Calculus" in topics
            assert "Algebra" in topics

    def test_empty_topic_list(self, app):
        with app.app_context():
            user = User(name="Test", email="topictest@test.com")
            db.session.add(user)
            db.session.flush()
            plan = StudyPlan(
                user_id=user.id, title="P",
                exam_date=date.today() + timedelta(days=7),
                daily_hours=3
            )
            db.session.add(plan)
            db.session.flush()
            subject = Subject(plan_id=plan.id, name="Physics", difficulty=2)
            db.session.add(subject)
            db.session.commit()
            assert subject.topic_list == []


class TestStudySessionModel:
    def test_mark_complete(self, app, sample_data):
        with app.app_context():
            session = StudySession.query.get(sample_data["session_id"])
            assert session.completed is False
            session.mark_complete()
            db.session.commit()
            assert session.completed is True
            assert session.completed_at is not None

    def test_mark_missed(self, app, sample_data):
        with app.app_context():
            session = StudySession.query.get(sample_data["session_id"])
            assert session.missed is False
            session.mark_missed()
            db.session.commit()
            assert session.missed is True

    def test_session_repr(self, app, sample_data):
        with app.app_context():
            session = StudySession.query.get(sample_data["session_id"])
            assert "Day1" in repr(session)


class TestRoutes:
    def test_index_page(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_new_plan_page(self, client):
        res = client.get("/plan/new")
        assert res.status_code == 200

    def test_dashboard_list(self, client):
        res = client.get("/dashboard/", follow_redirects=True)
        assert res.status_code == 200

    def test_health_check(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_404_plan(self, client):
        res = client.get("/plan/99999")
        assert res.status_code == 404

    def test_complete_session(self, client, app, sample_data):
        with app.app_context():
            plan_id    = sample_data["plan_id"]
            session_id = sample_data["session_id"]
        res = client.post(f"/plan/{plan_id}/session/{session_id}/complete")
        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "ok"
        assert "progress" in data