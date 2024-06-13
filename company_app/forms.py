from django import forms

from .models import Task, Department, CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        models = Task
        fields = ['title', 'description', 'department', 'assignee', 'status']


class DepartmentForm(forms.ModelForm):
    class Meta:
        models = Department
        fields = ['name', 'manager']

    
class CustomUserForm(forms.ModelForm):
    class Meta:
        models = CustomUser
        fields = ['username', 'password', 'is_manager']