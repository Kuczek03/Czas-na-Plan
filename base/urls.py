from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('', views.home, name='home'),
    path('dashboards/', views.dashboardPage, name='dashboards'),
    path('tasks/',views.tasks, name='tasks'),
    path('dashboard/<int:dashboard_id>/create-task/', views.createTask, name='createTask'),
    path('register/', views.register, name='register'),
    path('update-task/<int:task_id>/', views.updateTask, name='updateTask'),
    path('delete-task/<int:task_id>/', views.deleteTask, name='deleteTask'),
    path('dashboard/<int:dashboard_id>/', views.dashboard_tasks, name='dashboard_tasks')
]