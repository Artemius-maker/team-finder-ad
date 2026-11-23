# Импортируем модель поздравления.
from django import forms
from .models import Project
from users.models import User


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'status': forms.ChoiceField(choices=('Открыт', 'Закрыт'))
        }