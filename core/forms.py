from django import forms

from .views import validate_hostname


class GithubForm(forms.ModelForm):

    def clean_github_url(self):
        data = self.cleaned_data['github_url']
        allowed_hosts = {'github.com', 'www.github.com', 'https://github.com'}
        validate_hostname(data, allowed_hosts)
        return data
