from django.utils import timezone

from .models import Task
from .utils import send_task_due_notification

def send_due_task_notifications():
    now = timezone.now()
    tasks = Task.objects.filter(due_date__lte=now, status='In Progress')
    for task in tasks:
        send_task_due_notification(task)