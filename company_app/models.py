from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_manager(self):
        return Department.objects.filter(manager=self).exists()


class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='department_manager')

    def __str__(self):
        return self.name
    

class Task(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        
    ]

    RECURRING_CHOICES = [
        ('None', 'None'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_tasks')
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assignee_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    due_date = models.DateTimeField(default=timezone.now)
    recurring = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='None')


    def __str__(self):
        return self.title