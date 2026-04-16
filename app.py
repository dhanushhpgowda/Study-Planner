from flask import Flask, render_template
from config import config
from extensions import db, migrate, mail
import os


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.planner import planner_bp
    from routes.tracker import tracker_bp
    from routes.export import export_bp
    from routes.chat import chat_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(tracker_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(chat_bp)

    # Start background scheduler for email reminders
    from services.scheduler_jobs import init_scheduler
    init_scheduler(app)

    # Register models so Flask-Migrate can detect them
    from models import User, StudyPlan, Subject, StudySession  # noqa: F401

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)