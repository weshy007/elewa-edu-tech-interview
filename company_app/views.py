from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserForm, TaskForm, DepartmentForm
from .models import Department, Task, CustomUser

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

@login_required
def summary_dashboard(request):
    if request.user.is_manager:
        departments = Department.objects.filter(manager=request.user)
        total_tasks = Task.objects.filter(department__in=departments).count()
        completed_tasks = Task.objects.filter(department__in=departments, status='Done').count()
        pending_tasks = Task.objects.filter(department__in=departments, status='In Progress').count()
        task_completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        context = {
            'departments': departments,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'task_completion_rate': task_completion_rate,
        }
        return render(request, 'summary_dashboard.html', context)
    return redirect('dashboard')


# Task views
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    context = {
        'form': form
    }

    return render(request, 'create_task.html', context)



@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form
    }

    return render(request, 'edit_task.html', context)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    
    context = {
        'task': task
    }

    return render(request, 'delete_task.html', context)


# Department views
@login_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            department = form.save(commit=False)
            department.manager = request.user
            department.save()
            return redirect('dashboard')
        
    else:
        form = DepartmentForm()

    context = {
        'form': form
    }

    return render(request, 'create_department.html', context)


@login_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
    else:
        form = DepartmentForm(instance=department)

    context = {
        'form': form
    }

    return render(request, 'edit_department.html', context)


@login_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        department.delete()
        return redirect('dashboard')
    
    context = {
        'department': department
    }

    return render(request, 'delete_department.html', context)


# User views
@login_required
def manage_employees(request):
    if request.user.is_manager:
        employees = CustomUser.objects.filter(is_manager=False, department__in=request.user)

        return render(request, 'manage_employees.html', {'employees': employees})
    
    return redirect('dashboard')


@login_required
def move_employee(request, employee_id, new_department_id):
    employee = get_object_or_404(CustomUser, id=employee_id)
    new_department = get_object_or_404(Department, id=new_department_id)
    employee.department = new_department
    employee.save()
    
    return redirect('manage_employees')


@login_required
def remove_employee(request, employee_id):
    employee = get_object_or_404(CustomUser, id=employee_id)
    employee.delete()
    return redirect('manage_employees')






