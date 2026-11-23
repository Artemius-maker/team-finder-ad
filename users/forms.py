# Импортируем модель поздравления.
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')


class LoginForm(AuthenticationForm):
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        })
    )
