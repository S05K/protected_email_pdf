from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import os
import logging


logger = logging.getLogger(__name__)


@shared_task
def send_email(pdf_file_path,email):
        subject = "Welcome! Your Protected PDF"
        body = "Hello! Please find the attached PDF. Use your registered password to open it."
        email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [email])
        email.attach_file(pdf_file_path)
        email.send(fail_silently=False)
        try:
            os.remove(pdf_file_path)
        except OSError as e:
            print(f"Error deleting file {pdf_file_path}: {e}")
        
