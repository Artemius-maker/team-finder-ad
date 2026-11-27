from .models import Project
from core.forms import GithubForm


class ProjectForm(GithubForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
