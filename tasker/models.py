from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser

from PIL import Image
from io import BytesIO


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        self._process_img()
        
        super().save(*args, **kwargs)

    def _make_square(self, img):
        min_size = 256
        fill_color = (1, 1, 1)
        x, y = img.size
        size = max(min_size, x, y)
        new_im = Image.new('RGB', (size, size), fill_color)
        new_im.paste(img, (int((size - x) / 2), int((size - y) / 2)))
        return new_im
    
    def _process_img(self):
        pil_img = Image.open(self.image)
        pil_img = self._make_square(pil_img)

        f = BytesIO()
        try:
            pil_img.save(f, format='JPEG')
            self.image = ContentFile(f.getvalue(), self.image.name)
        finally:
            f.close()


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='head')
    head = models.ManyToManyField(User)

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
