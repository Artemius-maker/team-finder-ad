# Импортируем модель поздравления.
from .models import Project
from core.forms import GithubForm

User = get_user_model()


class ProjectForm(GithubForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
