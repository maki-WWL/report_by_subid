import sys
import os
from celery import Celery
from celery.schedules import crontab
from base import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

app = Celery("base")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.timezone = "Europe/Kiev"

app.conf.beat_schedule = {
    "run_script": {
        "task": "kt_comparison.tasks.run_script",
        "schedule": crontab(minute=1, hour=16),
    },
}

app.autodiscover_tasks()
