from django.core.mail import send_mail
from django.conf import settings

from .models import Task


def send_task_due_notification(task):

    subject = f'Task Due: {task.title}'
    message = f'The task "{task.title}" is due on {task.due_date}'

    recipient_list = [task.assigned_to.email, task.department.manager.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)