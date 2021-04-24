from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('account-settings/', account_settings, name='account_settings'),
    path('new_task/', new_task, name='new_task'),
    path('task/<int:id>/', task, name='task'),
    path('delete-goal/<int:id>', delete_goal, name='delete_goal'),
    path('delete-task/<int:id>', delete_task, name='delete_task'),
]
