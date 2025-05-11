import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')

app = Celery('finance')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-prediction-metrics-daily-at-8am': {
        'task': 'machine_learning.tasks.update_all_predictions_metrics',
        'schedule': crontab(hour=5, minute=0),  # Каждый день в 8:00 утра
    },
}
