from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('', views.home, name='home'),
    path('dashboards/', views.dashboardPage, name='dashboards'),
    path('tasks/',views.tasks, name='tasks'),
    path('createtask/', views.createTask, name='createtask')
]