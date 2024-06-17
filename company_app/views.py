from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import *
from .models import Department, Task, CustomUser

from .utils import fetch_users, fetch_tasks

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_manager:
                    return redirect('manager_dashboard')  # Redirect to manager dashboard if user is a manager
                else:
                    return redirect('employee_dashboard')  # Redirect to employee dashboard if user is a normal user
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill out both fields.')
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

"""
Manager Functions: 
- manager_dashboard, 
- create_department, create_task, 
- update_task, delete_task, 
- remove_employee, 
-search_employees    
"""
def is_manager(user):
    return user.is_manager


@login_required
@user_passes_test(is_manager)
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('manager_dashboard')
    else:
        form = DepartmentForm()
    
    return render(request, 'create_department.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            send_task_assignment_email(task)
            messages.success(request, 'Task created successfully.')
            return redirect('manager_dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'create_task.html', {'form': form})

@login_required
@user_passes_test(is_manager)
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('manager_dashboard')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'edit_task.html', {'form': form, 'task': task})

@login_required
@user_passes_test(is_manager)
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('manager_dashboard')
    
    return render(request, 'delete_task.html', {'task': task})

@login_required
@user_passes_test(is_manager)
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        assignee_id = request.POST.get('assignee')
        if assignee_id:
            task.assignee_id = assignee_id
            task.save()
            send_task_assignment_email(task)
            messages.success(request, 'Task assigned successfully.')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please select an assignee.')
    
    return render(request, 'assign_task.html', {'task': task})

@login_required
@user_passes_test(is_manager)
def move_employee(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        new_department_id = request.POST.get('new_department')
        if new_department_id:
            user.department_id = new_department_id
            user.save()
            messages.success(request, 'Employee moved to a new department successfully.')
            return redirect('manager_dashboard')
        else:
            messages.error(request, 'Please select a department.')
    
    departments = Department.objects.all()
    return render(request, 'move_employee.html', {'user': user, 'departments': departments})

@login_required
@user_passes_test(is_manager)
def remove_employee(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Employee removed from the organization successfully.')
        return redirect('manager_dashboard')
    
    return render(request, 'remove_employee.html', {'user': user})

def send_task_assignment_email(task):
    subject = 'Task Assignment'
    message = f'You have been assigned a new task: {task.title}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = task.assignee.email
    send_mail(subject, message, from_email, [to_email])


"""
Employee Dashboard views - employee_dashboard, update_task_status
"""
@login_required
def employee_dashboard(request):
    user = request.user
    tasks = Task.objects.filter(assignee=user)

    # Filter by task status
    status_filter = request.GET.get('status')

    if status_filter in ['Done', 'In Progress']:
        tasks = tasks.filter(status=status_filter)

    # Pagination
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,
        'user': user,
        'status_filter': status_filter
    }

    return render(request, 'employee_dashboard.html', context)


@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, assignee=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES).keys():
            task.status = new_status
            task.save()
    return redirect(reverse('employee_dashboard'))



def is_manager(user):
    return user.is_authenticated and user.is_manager


@login_required
def manager_dashboard(request):
    departments = Department.objects.all()
    tasks = Task.objects.all()
    employees = CustomUser.objects.all()
    department_form = DepartmentForm()
    task_form = TaskForm()
    search_form = EmployeeSearchForm()

    # Pagination for departments
    departments_paginator = Paginator(departments, 10)
    page_number = request.GET.get('departments_page')
    try:
        departments = departments_paginator.page(page_number)
    except PageNotAnInteger:
        departments = departments_paginator.page(1)
    except EmptyPage:
        departments = departments_paginator.page(departments_paginator.num_pages)
    
    # Pagination for tasks
    tasks_paginator = Paginator(tasks, 10)
    page_number = request.GET.get('tasks_page')
    try:
        tasks = tasks_paginator.page(page_number)
    except PageNotAnInteger:
        tasks = tasks_paginator.page(1)
    except EmptyPage:
        tasks = tasks_paginator.page(tasks_paginator.num_pages)

    context = {
        'departments': departments,
        'tasks': tasks,
        'employees': employees,
        'department_form': department_form,
        'task_form': task_form,
        'search_form': search_form
    }

    return render(request, 'manager_dashboard.html', context)

    
@login_required
@user_passes_test(is_manager)
def summary_dashboard(request):
    # Calculate overall task completion rates
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    overall_completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Calculate departmental performances
    departments = Department.objects.all()
    department_performances = []
    for department in departments:
        department_tasks = Task.objects.filter(department=department)
        total_department_tasks = department_tasks.count()
        completed_department_tasks = department_tasks.filter(status='completed').count()
        department_completion_rate = (completed_department_tasks / total_department_tasks) * 100 if total_department_tasks > 0 else 0
        department_performances.append({
            'department': department,
            'completion_rate': department_completion_rate,
            'total_tasks': total_department_tasks,
            'completed_tasks': completed_department_tasks
        })

    # Calculate pending tasks (not started or ongoing)
    pending_tasks = Task.objects.filter(Q(status='not_started') | Q(status='ongoing')).count()

    context = {
        'overall_completion_rate': overall_completion_rate,
        'department_performances': department_performances,
        'pending_tasks': pending_tasks,
    }

    return render(request, 'manager_dashboard.html', context)

