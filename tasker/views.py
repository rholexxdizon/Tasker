from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *

from django.db.utils import IntegrityError

# Create your views here.def index(request):
def index(request):
    return render(request, 'index/index.html', {})

def dashboard(request):
    user_id = request.user.id
    tasks = Task.objects.filter(
        Q (department__head__in=[user_id]) | Q(department__members__in=[user_id])
    ).distinct()

    return render(request, 'dashboard/dashboard.html', { 'tasks': tasks })

def new_task(request):
    context = {}
    if request.method == 'POST':
        try:
            name = request.POST['name']
            desc = request.POST['desc']
            due_date = None if request.POST['due'] == '' else request.POST['due']
            dept = Department.objects.filter(members__in=[request.user.id])

            task = Task(name=name, description=desc, due_on=due_date)
            task.save()
            task.department.add(dept[0])

            return redirect(dashboard)

        except IntegrityError as e:
            return render(request, 'dashboard/new-taskform.html', {'error': e})

    return render(request, 'dashboard/new-taskform.html', {})

def task(request, name):
    task = Task.objects.get(name=name)

    if request.method == 'POST':
        task.name = request.POST['name']
        task.description = request.POST['desc']
        task.due_on = None if request.POST['due'] == '' else request.POST['due']
        task.save()

    return render(request, 'dashboard/task.html', {'task':task})

