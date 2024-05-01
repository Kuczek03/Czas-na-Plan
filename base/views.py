from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, redirect
from .forms import TaskForm
from .models import Tasks
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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

def tasksFormView(request):
    task = Tasks.objects.get() #tu moze cos dodac trzeba
    context = {'task':task}
    return render(request,'base/task.html',context)
def createTask(request):
    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
           # return redirect('home')
    context = {'form':form}
    return render(request,'task.html',context)
def home(request):
    return HttpResponse("Home page")

def tasks(request):
    return HttpResponse("tasks")
