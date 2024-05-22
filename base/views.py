
# ----- Uwaga ----- #
# Do naprawy: kiedy dodaje się dashboard i nie zaznaczy się siebie to nie doda go wgl do żadnego użytkownika a jeśli
# dodasz siebie to dashboard na twojej stronie głównej będzie podwójny chuj wie ocb
# do zrobienia: przypisywanie tasków do użytkowników, lączenie z kalendarzem google, priorytety
# usuwanie dashboardów mam prawie zrobione więc nie rób

from django.shortcuts import render

from django.shortcuts import redirect, render, redirect
from .forms import TaskForm, TabForm, UserRegisterForm
from .models import Tasks, Users_Dashboards, Dashboards
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



from django.db import IntegrityError


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




def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
           messages.error(request, "użytkownik nie istnieje")
           user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"username or password incorrect")

    context = {}
    return render(request,'login_register.html',context)


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
        form = TaskForm()

    context = {'form': form, 'dashboard': dashboard}
    return render(request, 'create_task.html', context)

@login_required(login_url='login')
def updateTask(request, task_id):
    task = get_object_or_404(Tasks, task_id=task_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Tasks.STATUS_CHOICES):
            task.task_status = new_status
            task.save()
    return redirect('dashboard_tasks', dashboard_id=task.board_id.dashboard_id)

@login_required(login_url='login')
def deleteTask(request, task_id):
    task = get_object_or_404(Tasks, task_id=task_id)
    dashboard_id = task.board_id.dashboard_id
    if request.method == 'POST':
        task.delete()
    return redirect('dashboard_tasks', dashboard_id=dashboard_id)


@login_required(login_url='login')
def dashboardPage(request):
    if request.method == 'POST':
        form = TabForm(request.POST)
        if form.is_valid():
            dashboard = form.save(commit=False)
            dashboard.dashboard_admin_id = request.user
            dashboard.save()
            form.save_m2m()
            for user in form.cleaned_data['users']:
                Users_Dashboards.objects.create(user_id=user, dashboard_id=dashboard)

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

def tasks(request):
    return HttpResponse("tasks")

