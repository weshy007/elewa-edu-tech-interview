from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(post_save, sender=Task)
def send_task_completion_email(sender, instance, **kwargs):
    if instance.status == 'Completed':
        # Send email to the manager
        manager_email = instance.department.manager.email
        subject = f'Task Completed: {instance.title}'
        message = (
            f'The task "{instance.title}" assigned to {instance.assignee.username} '
            f'has been completed.\n\n'
            f'Task Details:\n'
            f'Title: {instance.title}\n'
            f'Due Date: {instance.due_date.strftime("%A, %B %d, %Y at %I:%M %p")}\n'
            f'Assignee: {instance.assignee.username}\n\n'
            f'Please check the portail for further details.\n\nRegards'
        )
        recipient_list = [manager_email]
        send_mail(subject, message, None, recipient_list)
