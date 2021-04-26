from .models import *

def say_hello(user, *args, **kwargs):
    print(f'Hello {user}')
    return True


def can_create_task(user, *args, **kwargs):
    heads = Department.objects.values_list('head', flat=True)
    if user.id in heads:
        return True
    return False

def can_view_task(user, task_id):
    task = Task.objects.get(id=task_id)
    task_departments = task.department.all()
    for department in task_departments:
        dept_members = department.members.all()
        if user in dept_members:
            return True
    return False
