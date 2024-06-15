from django import forms
from django.forms import ModelForm

from .models import Task, Department, CustomUser


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'department', 'assignee', 'status',  'due_date', 'recurring']


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'manager']

    
class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class EmployeeSearchForm(forms.Form):
    query = forms.CharField(max_length=100)