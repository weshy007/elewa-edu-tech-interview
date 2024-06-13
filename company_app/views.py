from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CustomUserForm
from .models import Department, Task

# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # TODO: Redirect to the dashboard page
            return redirect('index')
    else:
        form = CustomUserForm()

    context = {
        'form': form
    }
        
    return render(request, 'signup.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)  

        redirect('index')

        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    if request.user.is_manager:
        # Get all departments
        departments = Department.objects.filter(manager=request.user)
        tasks = Task.objects.filter(department__in=departments)
    else:
        tasks = Task.objects.filter(assignee=request.user)
    
    context = {
        # 'departments': departments,
        'tasks': tasks
    }

    return render(request, 'manager_dashboard.html', context)