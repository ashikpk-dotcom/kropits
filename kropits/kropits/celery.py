import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kropits.settings')

app = Celery('kropits')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

app.autodiscover_tasks()
