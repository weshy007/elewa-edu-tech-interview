from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    
    path('dashboard/', views.manager_dashboard, name='dashboard'),
    path('summary_dashboard/', views.summary_dashboard, name='summary_dashboard'),

    path('task/create/', views.create_task, name='create_task'),
    path('task/edit/<int:task_id>/', views.update_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('department/create/', views.create_department, name='create_department'),
    path('department/edit/<int:department_id>/', views.edit_department, name='edit_department'),
    path('department/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    
    path('manage_employees/', views.manage_employees, name='manage_employees'),
    path('employee/move/<int:employee_id>/<int:new_department_id>/', views.move_employee, name='move_employee'),
    path('employee/remove/<int:employee_id>/', views.remove_employee, name='remove_employee'),
]