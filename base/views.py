from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, redirect
from .forms import TaskForm, TabForm
from .models import Tasks
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
def createTask(request):
    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
           # return redirect('home')
    context = {'form':form}
    return render(request,'task.html',context)

def dashboardPage(request):
    form = TabForm
    if request.method == 'POST':
        form = TabForm(request.POST)
        if form.is_valid():
            form.save()
           # return redirect('home')
    context = {'form':form}
    return render(request,'tab_form.html',context)
def home(request):
    return render(request,'home.html')

def tasks(request):
    return HttpResponse("tasks")
