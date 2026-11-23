from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import BaseCreateView
from projects.models import Project
from .models import User
from .forms import RegisterForm, LoginForm
from core.views import participated_projects, page_paginator, interested_users


# Create your views here.
class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(filter=self.request.filter)
        return self.model.objects.all()


def user_detail(request, user_id):
    template_name = 'users/user-details.html'
    user = get_object_or_404(User, id=user_id)
    context = {"user": user}
    return render(request, template_name, context)


@login_required  # Доступ только авторизованным пользователям
def edit_profile(request):
    template_name = 'users/edit_profile.html'
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('user:user_detail', email=request.user.email)
    context = {'form': form}
    return render(request, template_name, context)
