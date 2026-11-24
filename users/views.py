from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView
from django.views.generic.edit import BaseCreateView
from projects.models import Project
from .models import User
from .forms import RegisterForm, LoginForm, ProfileForm
from core.views import participated_projects, page_paginator, interested_users
from django.views import View
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.db.models import QuerySet
from django.contrib.auth.views import PasswordChangeView


# Create your views here.
class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.GET.get('filter'):
            if self.request.GET.get('filter') == 'owners-of-favorite-projects':
                filtered_id = self.request.user.favorites.values('owner__id')
            elif self.request.GET.get('filter') == 'owners-of-participating-projects':
                filtered_id = self.request.user.participated_projects().values('owner__id')
            elif self.request.GET.get('filter') == 'interested-in-my-projects':
                filtered_id = self.model.objects.filter(favorites__in=self.request.user.owned_projects()).values('id')
            elif self.request.GET.get('filter') == 'participants-of-my-projects':
                filtered_id = self.request.user.owned_projects().select_related('participants').values('participants__id')
            else:
                return self.model.objects.all()
            return self.model.objects.filter(pk__in=filtered_id).distinct()
        return self.model.objects.all()


class LoginView(View):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_short_name()}!')
                return redirect('projects:mainpage')
        print(form.errors)
        return render(request, self.template_name, {'form': form})


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
        return redirect('users:user_detail', user_id=request.user.id)
    context = {'form': form}
    return render(request, template_name, context)


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse_lazy('users:user_detail', kwargs={'user_id': self.request.user.id})