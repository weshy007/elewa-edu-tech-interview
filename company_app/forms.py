from django.forms import ModelForm

from .models import Task, Department, CustomUser


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'department', 'assignee', 'status',  'due_date']


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'manager']

    
class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']