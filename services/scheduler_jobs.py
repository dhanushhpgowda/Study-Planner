from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

scheduler = BackgroundScheduler()
_started  = False


def init_scheduler(app):
    global _started
    if _started:
        return

    from services.notifications import send_reminders_for_all_plans

    scheduler.add_job(
        func=lambda: send_reminders_for_all_plans(app),
        trigger=CronTrigger(hour=7, minute=0),
        id="daily_reminder",
        name="Send daily study reminders",
        replace_existing=True,
    )

    scheduler.start()
    _started = True
    print("[Scheduler] Started — daily reminders at 07:00")

    atexit.register(lambda: scheduler.shutdown(wait=False))


def trigger_now(app):
    from services.notifications import send_reminders_for_all_plans
    return send_reminders_for_all_plans(app)