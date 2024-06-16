from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].required = True  
    
class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class EmployeeSearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
