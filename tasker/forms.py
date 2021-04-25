from django.forms import *
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        widgets = {

            # 'image': FileInput(attrs={
            #     'accept': 'image/jpeg, image/jpg',
            #     'placeholder': model.image,
            # }),

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
