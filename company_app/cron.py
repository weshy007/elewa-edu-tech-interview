from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Task
from .utils import send_task_due_notification

def send_due_task_notifications():
    now = timezone.now()
    tasks = Task.objects.filter(due_date__lte=now, status='In Progress')
    for task in tasks:
        send_task_due_notification(task)


def handle_recurring_tasks():
    now = timezone.now()
    tasks = Task.objects.filter(status='Done', recurring__in=['Daily', 'Weekly', 'Monthly'])
    for task in tasks:
        if task.recurring == 'Daily':
            new_due_date = task.due_date + relativedelta(days=1)
        elif task.recurring == 'Weekly':
            new_due_date = task.due_date + relativedelta(weeks=1)
        elif task.recurring == 'Monthly':
            new_due_date = task.due_date + relativedelta(months=1)
        
        Task.objects.create(
            title=task.title,
            description=task.description,
            status='In Progress',
            assigned_to=task.assigned_to,
            department=task.department,
            due_date=new_due_date,
            recurring=task.recurring
        )
        task.delete()