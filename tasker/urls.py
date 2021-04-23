from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new_task/', new_task, name='new_task'),
    path('task/<int:id>/', task, name='task'),
]
