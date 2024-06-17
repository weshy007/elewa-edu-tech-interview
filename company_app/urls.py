from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    
    path('register/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),

    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/summary_dashboard/', views.summary_dashboard, name='summary_dashboard'),

    path('manager/create_department/', views.create_department, name='create_department'),
    path('manager/create_task/', views.create_task, name='create_task'),
    path('manager/edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('manager/delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('manager/move_employee/<int:user_id>/', views.move_employee, name='move_employee'),
    path('manager/remove_employee/<int:user_id>/', views.remove_employee, name='remove_employee'),
]