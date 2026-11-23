from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Project
from users.models import User
from .forms import ProjectForm
from core.views import participated_projects, page_paginator, interested_users


class HomepageView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    paginate_by = 10


class FavoritesView(ListView):
    model = Project
    template_name = 'projects/favorite_project.html'
    paginate_by = 10


def project_detail(request, pk):
    template_name = 'projects/project-detail.html'
    post = get_object_or_404(is_published(Post.objects.select_related(
        'category'), request.user.username, True).filter(pk=pk))
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, template_name, context)


@login_required
def toggle_participate(request, pk):
    template_name = 'projects/project-detail.html'
    project = get_object_or_404(User.objects.select_related(
        'favorites'), request.user.username, True).favorites.filter(pk=pk)
    context = {"status": "ok", "favorited": ''}
    return render(request, template_name, context)


@login_required
def project_complete(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    if request.user != instance.author:
        return redirect('blog:post_detail', pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = PostForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('blog:index')
    # Если был получен GET-запрос — отображаем форму.
    template_name = 'blog/create.html'
    return render(request, template_name, context)


@login_required
def create_edit_project(request, pk=None):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Post, pk=pk)
        if request.user != instance.author:
            return redirect('blog:post_detail', pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=instance)
    if form.is_valid():
        # Создаём объект поста, но не сохраняем его в БД.
        post = form.save(commit=False)
        # В поле author передаём объект автора поста.
        post.author = request.user
        # Сохраняем объект в БД.
        post.save()
        # Перенаправляем пользователя назад, на страницу поста.
        if pk is not None:
            return redirect('blog:post_detail', pk=pk)
        return redirect('blog:profile', username=request.user.username)
    template_name = 'blog/create.html'
    context = {'form': form}
    return render(request, template_name, context)
