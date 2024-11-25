import logging
import os
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task(name='send_email', bind=True)
def example_task(self, email):
    try:
        send_mail("Tested", 
                  f"Tested {os.getenv('MINUTES')}", 
                  os.getenv('EMAIL_HOST_USER'), 
                  [email], 
                  fail_silently=False)
        logger.info(f"Task {self.request.id} successful send email")
    except Exception as e:
        logger.error(f"Task {self.request.id} failed: {e}")
        raise self.retry(exc=e, countdown=60)