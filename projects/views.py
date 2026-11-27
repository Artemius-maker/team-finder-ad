from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import exceptions

from .models import Project
from .forms import ProjectForm
from .constants import consts
from team_finder.settings import paginate_by

User = get_user_model()


class HomepageView(ListView):
    model = Project
    template_name = 'templates_var1/projects/project_list.html'
    paginate_by = paginate_by


class FavoritesView(ListView):
    model = Project
    template_name = 'templates_var1/projects/favorite_project.html'
    paginate_by = paginate_by

    def get_queryset(self):
        return self.request.user.favorites.all()


def project_detail(request, project_id):
    template_name = 'projects/project-details.html'
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    return render(request, template_name, context)


@login_required
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if project.participants.filter(pk=user.id).exists():
        project.participants.remove(user)
        context = {"status": "ok"}
    else:
        project.participants.add(user)
        context = {"status": "ok", "participant": 'participate'}
    project.save()
    return JsonResponse(context)


@login_required
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    context = {"status": "ok"}
    if user.favorites.filter(pk=project.id).exists():
        user.favorites.remove(project)
        context["favorited"] = 'not-favorite'
    else:
        user.favorites.add(project)
        context["favorited"] = 'favorite'
    user.save()
    return JsonResponse(context)


@login_required
def project_complete(request, project_id):
    instance = get_object_or_404(Project, pk=project_id)
    if request.method != 'POST':
        raise exceptions.MethodNotAllowed("Разрешены только POST-запросы")
    if request.user != instance.owner:
        raise exceptions.PermissionDenied("Только автор может выполнить это действие")
    if instance.status in consts.choices[1]:
        raise exceptions.ValidationError("Невозможно выполнить действие для закрытого проекта")
    instance.status = consts.choices[1][1]
    instance.save()
    context = {"status": "ok", "project_status": instance.status}
    return JsonResponse(context)


@login_required
def create_edit_project(request, project_id=None):
    if project_id is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Project, pk=project_id)
        if request.user != instance.owner:
            return redirect('projects:project_detail', project_id=project_id)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    form = ProjectForm(request.POST or None, instance=instance)
    if not form.is_valid():
        template_name = 'projects/create-project.html'
        context = {'form': form}
        return render(request, template_name, context)
    # Создаём объект поста, но не сохраняем его в БД.
    project = form.save(commit=False)
    # В поле author передаём объект автора поста.
    if project_id is None:
        project.owner = request.user
    # Сохраняем объект в БД.
    project.save()
    # Перенаправляем пользователя назад, на страницу поста.
    return redirect('projects:project_detail', project_id=project.id)
