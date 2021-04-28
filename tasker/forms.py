from django.forms import *
from .models import *


class UserForm(ModelForm):
    class Meta:
        model = User
        widgets = {

            'first_name': TextInput(attrs={
                'placeholder': model.first_name,
            }),

            'last_name': TextInput(attrs={
                'placeholder': model.last_name,
            }),

            'username': TextInput(attrs={
                'placeholder': model.username,
            }),

            'email': EmailInput(attrs={
                'placeholder': model.email,
            }),

        }
        fields = [
            'image',
            'first_name',
            'last_name',
            'username',
            'email'
        ]


class SubmitionForm(ModelForm):
    class Meta:
        model = Submition
        fields = [
            'title',
            'description',
        ]
