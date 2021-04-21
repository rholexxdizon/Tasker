from django.shortcuts import render
from django.db.models import Q
from .models import *

# Create your views here.def index(request):
def index(request):
    return render(request, 'index/index.html', {})

def dashboard(request):
    user_id = request.user.id

    tasks = Task.objects.filter(
        Q (department__head__in=[user_id]) | Q(department__members__in=[user_id])
    ).distinct()

    print(tasks)
    context = {'tasks': tasks}

    return render(request, 'dashboard/dashboard.html', context)