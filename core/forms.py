# Импортируем модель поздравления.
from django import forms
from django.contrib.auth import get_user_model

from .views import validate_hostname

User = get_user_model()


class GithubForm(forms.ModelForm):

    def clean_github_url(self):
        data = self.cleaned_data['github_url']
        allowed_hosts = {'github.com', 'www.github.com', 'https://github.com'}
        validate_hostname(data, allowed_hosts)
        return data
