from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, redirect
from .forms import TaskForm
from .models import Tasks
from django.http import HttpResponse
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
