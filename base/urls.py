from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('info/', views.info, name='info'),
    path('', views.home, name='home'),
    path('dashboards/', views.dashboardPage, name='dashboards'),
    path('dashboard/<int:dashboard_id>/create-task/', views.createTask, name='createTask'),
    path('register/', views.register, name='register'),
    path('update-task/<int:task_id>/', views.updateTask, name='updateTask'),
    path('delete-task/<int:task_id>/', views.deleteTask, name='deleteTask'),
    path('dashboard/delete/<int:dashboard_id>/', views.delete_dashboard, name='delete_dashboard'),
    path('dashboard/<int:dashboard_id>/', views.dashboard_tasks, name='dashboard_tasks')
]