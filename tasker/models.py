from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(null=True, default=None, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='head')
    head = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateField(auto_now=True, null=False)
    due_on = models.DateField(null=True, blank=True, default=None)
    department = models.ManyToManyField(Department)

    def __str__(self):
        return self.name


# task item is goal in the website :D
class TaskItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    done = models.BooleanField(null=False, default=False)
    task = models.ManyToManyField(Task)

    def __str__(self):
        return self.name
