from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)


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

    title = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_tasks')
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assignee_tasks')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title