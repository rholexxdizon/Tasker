from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.utils import IntegrityError

from .models import *
from .forms import UserForm


# Create your views here.def index(request):
def index(request):
    return render(request, 'index/index.html', {})


def dashboard(request):
    user_id = request.user.id
    tasks = Task.objects.filter(
        Q(department__head__in=[user_id]) | Q(department__members__in=[user_id])
    ).distinct()

    return render(request, 'dashboard/dashboard.html', { 'tasks': tasks })


def account_settings(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'account/account-settings.html', {'form': form})


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


def task(request, id):
    task = Task.objects.get(id=id)

    goals = TaskItem.objects.filter(task__in=[task])

    if request.method == 'POST':

        option = request.POST['option']
        option = option.lower().strip()

        if option == 'delete task':
            print('delete task')
            return redirect('delete_task', task.id)


        # save task edit
        task.name = request.POST['name']
        task.description = request.POST['desc']
        task.due_on = None if request.POST['due'] == '' else request.POST['due']
        task.save()

        # save goals
        post = request.POST
        for k in post.keys():
            if 'goal-' in post[k]:
                
                val = post[k]

                try:
                    if '-True-' in val:
                        g_name = val.replace('goal-True-', '')
                        g_done = True

                        goal = TaskItem(name=g_name, done=g_done)
                        goal.save()
                        goal.task.add(task)


                    elif '-False-' in val:
                        g_name = val.replace('goal-False-', '')
                        g_done = False

                        goal = TaskItem(name=g_name, done=g_done)
                        goal.save()
                        goal.task.add(task)
                    
                except IntegrityError as e:
                    
                    print(e)

                    print(val)

                    if '-True-' in val:
                        g_name = val.replace('goal-True-', '')
                        goal = TaskItem.objects.filter(name=g_name)[0]
                        goal.done = True
                        goal.save()
                        goal.task.add(task)

                    elif '-False-' in val:
                        g_name = val.replace('goal-False-', '')
                        goal = TaskItem.objects.filter(name=g_name)[0]
                        goal.done = False
                        goal.save()
                        goal.task.add(task)

    context = {
        'task':task,
        'goals': goals,
    }

    return render(request, 'dashboard/task.html', context)


def delete_task(request, id):
    tsk = Task.objects.get(id=id)

    if request.method == 'POST':
        option = request.POST['option']
        option = option.lower().strip() # clean the string

        if option == 'delete':
            tsk.delete()
            return redirect(dashboard)
        
        elif option == 'cancel':
            return redirect(task, tsk.id)


    return render(request, 'dashboard/delete-item.html', {'item': tsk})


def delete_goal(request, id):
    goal = TaskItem.objects.get(id=id)
    g_task = goal.task.all()[0]
    
    if request.method == 'POST':
        option = request.POST['option']
        option = option.lower().strip() # clean the string

        if option == 'delete':
            goal.delete()
            return redirect(task, g_task.id)
        
        elif option == 'cancel':
            return redirect(task, g_task.id)

    return render(request, 'dashboard/delete-item.html', {'item': goal})
