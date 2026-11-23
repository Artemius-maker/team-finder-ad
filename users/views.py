from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import BaseCreateView
from projects.models import Project
from .models import User
from .forms import ProfileForm
from core.views import participated_projects, page_paginator, interested_users


# Create your views here.
class UserListView(ListView):
    # page_paginator()
    model = Project
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return count_comments(is_published(self.model.objects.
                                           select_related('category')))


def user_detail(request, pk):
    template_name = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = count_comments(
        is_published(Post.objects
                     .select_related('category', 'author'),
                     request.user.username, True)
            .filter(author__username=username))
    page_obj = page_paginator(request, post_list)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template_name, context)


@login_required  # Доступ только авторизованным пользователям
def edit_profile(request):
    template_name = 'blog/user.html'
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, template_name, context)


def login():
    pass


def logout():
    pass
