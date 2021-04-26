from django.shortcuts import render, redirect
from django.db.models import Q, QuerySet
from django.db.utils import IntegrityError

from allauth.account.decorators import login_required

from .models import *
from .forms import UserForm
from .decorators import user_permission_test
from .test_functions import *


# Create your views here.def index(request):
def index(request):
    return render(request, 'index/index.html', {})


@login_required
def dashboard(request):
    user_id = request.user.id
    user_departments = Department.objects.filter(members__in=[user_id])
    tasks = Task.objects.filter(department__in=user_departments)
    context = {
        'tasks': tasks,
        'departments': user_departments,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def account_settings(request):
    form = UserForm(instance=request.user)
    errors = None

    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            errors = form.errors

    return render(request, 'account/account-settings.html', {
        'form': form,
        'errors': errors
    })


@login_required
@user_permission_test(can_create_task)
def new_task(request, dept_id):
    context = {}
    if request.method == 'POST':
        try:
            name = request.POST['name']
            desc = request.POST['desc']
            due_date = None if request.POST['due'] == '' else request.POST['due']
            dept = Department.objects.get(id=dept_id)
            task = Task(name=name, description=desc, due_on=due_date)
            task.save()
            task.department.add(dept)

            return redirect(dashboard)

        except IntegrityError as e:
            return render(request, 'dashboard/new-taskform.html', {'error': e})

    return render(request, 'dashboard/new-taskform.html', {})


@login_required
def task(request, id):
    task = Task.objects.get(id=id)

    goals = TaskItem.objects.filter(task__in=[task])

    # check if user if permitted to view task
    if not can_view_task(request.user, id):
        return render(request, 'access-denied.html', {})

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


@login_required
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


@login_required
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
