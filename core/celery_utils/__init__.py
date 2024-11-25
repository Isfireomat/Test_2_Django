import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(email_backend=settings.EMAIL_BACKEND)

app.autodiscover_tasks()
app.autodiscover_tasks(['celery_utils.tasks'])