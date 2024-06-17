from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Department, Task

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'manager']
        widgets = {
            'manager': forms.HiddenInput(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'status', 'due_date', 'recurring', 'department']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search Employees')