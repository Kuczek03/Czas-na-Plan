
# ----- Uwaga ----- #
# do zrobienia: przypisywanie tasków do użytkowników, lączenie z kalendarzem google, priorytety

from django.shortcuts import render

from django.shortcuts import redirect, render, redirect
from .forms import TaskForm, TabForm, UserRegisterForm
from .models import Tasks, Users_Dashboards, Dashboards
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.db import IntegrityError


def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    users_list = list(users.values('id', 'username'))
    return JsonResponse(users_list, safe=False)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, f'Account created for {username}!')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Username already exists. Please choose another one.')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

#############################################
def info(request):
    return render(request, 'info.html')
#############################################
def settings(request):
    if request.method == 'POST':
        user = request.user
        # Aktualizacja nazwy użytkownika i adresu e-mail
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        # Zmiana hasła
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Aktualizacja sesji, aby uniknąć wylogowania

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'settings.html', {'form': form})
#############################################

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Używamy authenticate zamiast próbować ręcznie pobierać użytkownika
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nazwa użytkownika lub hasło niepoprawne!")

    context = {}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def createTask(request, dashboard_id):
    dashboard = get_object_or_404(Dashboards, pk=dashboard_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.board_id = dashboard
            task.save()
            return redirect('dashboard_tasks', dashboard_id=dashboard_id)
    else:
        initial_data = {'board_id': dashboard}  # Przekazanie wartości początkowej do pola board_id
        form = TaskForm(initial=initial_data)

    context = {'form': form, 'dashboard': dashboard}
    return render(request, 'create_task.html', context)


@login_required(login_url='login')
def deleteTask(request, task_id):
    task = get_object_or_404(Tasks, task_id=task_id)
    dashboard_id = task.board_id.dashboard_id
    if request.method == 'POST':
        task.delete()
    return redirect('dashboard_tasks', dashboard_id=dashboard_id)

#############################################

def deleteDashboard(request, dashboard_id):
    if request.method == 'POST':
        dashboard = get_object_or_404(Dashboards, pk=dashboard_id)
        dashboard.delete()
    return redirect('home')

#############################################

@login_required(login_url='login')
def dashboardPage(request):
    if request.method == 'POST':
        form = TabForm(request.POST)
        if form.is_valid():
            dashboard = form.save(commit=False)
            dashboard.dashboard_admin_id = request.user
            dashboard.save()
            selected_users = request.POST.getlist('users')
            selected_users.append(str(request.user.id))
            dashboard.users.set(selected_users)

            messages.success(request, 'Tablica została stworzona.')
            return redirect('home')
    else:
        form = TabForm()

    context = {'form': form}
    return render(request, 'tab_form.html', context)


@login_required(login_url='login')
def addUser(request):
    if request.method == 'POST':
        pass

@login_required(login_url='login')
def dashboard_tasks(request, dashboard_id):
    try:
        dashboard = Dashboards.objects.get(pk=dashboard_id)
    except Dashboards.DoesNotExist:
        return redirect('home')

    if request.user.is_staff or Users_Dashboards.objects.filter(user_id=request.user, dashboard_id=dashboard).exists():
        tasks_to_do = Tasks.objects.filter(board_id=dashboard, task_status='to do')
        tasks_in_progress = Tasks.objects.filter(board_id=dashboard, task_status='in progress')
        tasks_done = Tasks.objects.filter(board_id=dashboard, task_status='done')
    else:
        tasks_to_do = tasks_in_progress = tasks_done = []

    context = {
        'dashboard': dashboard,
        'tasks_to_do': tasks_to_do,
        'tasks_in_progress': tasks_in_progress,
        'tasks_done': tasks_done,
    }
    return render(request, 'dashboard_tasks.html', context)

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            admin_dashboards = Dashboards.objects.all()
        else:
            admin_dashboards = Dashboards.objects.filter(users_dashboards__user_id=request.user)
    else:
        admin_dashboards = []

    context = {
        'admin_dashboards': admin_dashboards
    }
    return render(request, 'home.html', context)

