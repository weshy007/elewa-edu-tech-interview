from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CustomUserForm, TaskForm, DepartmentForm, EmployeeSearchForm
from .models import Department, Task, CustomUser

from .utils import fetch_users, fetch_tasks

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


"""
Manager Dashboard views 
- manager_dashboard, 
- create_department, create_task, 
- update_task, delete_task, 
- remove_employee, 
-search_employees    
"""
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
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
        
    return redirect('manager_dashboard')


@login_required
@user_passes_test(is_manager)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
        
    return redirect('manager_dashboard')


@login_required
@user_passes_test(is_manager)
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
        
    return redirect('manager_dashboard')


@login_required
@user_passes_test(is_manager)
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('manager_dashboard')
    
    
@login_required
@user_passes_test(is_manager)
def remove_employee(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('manager_dashboard')


@login_required
@user_passes_test(is_manager)
def search_employees(request):
    if request.is_ajax():
        query = request.GET.get('query', '')
        
        if len(query) >= 3:
            employees = CustomUser.objects.filter(username__icontains=query)
            results = [{'id': emp.id, 'username': emp.username} for emp in employees]
            return JsonResponse({'results': results})
    return JsonResponse({'results': []})
    


@login_required
def manager_dashboard(request):
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

