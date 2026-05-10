from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
         'first_name',
         'last_name',
         'cin',
         'phone',
         'address',
         'permis_recto',
         'permis_verso'
          ]

        widgets = {

    'first_name': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),

    'last_name': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),

    'cin': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),

    'phone': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),

    'address': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 3
        }
    ),

    'permis_recto': forms.ClearableFileInput(
        attrs={
            'class': 'form-control'
        }
    ),

    'permis_verso': forms.ClearableFileInput(
        attrs={
            'class': 'form-control'
        }
    ),
}

class PermisVerificationForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'permis_recto',
            'permis_verso',
        ]