# Импортируем модель поздравления.
from django import forms
from .models import Project
from users.models import User
from core.views import validate_hostname
from django.core.exceptions import ValidationError


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'status': forms.Select(choices=('Открыт', 'Закрыт'))
        }

    def clean_github_url(self):
        data = self.cleaned_data['github_url']
        allowed_hosts = {'github.com', 'www.github.com', 'https://github.com'}
        if not validate_hostname(data, allowed_hosts):  # используем функцию из предыдущего способа
            raise ValidationError('Некорректный домен для поля github_url')
        return data