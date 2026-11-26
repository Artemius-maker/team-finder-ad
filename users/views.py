from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.views.generic import ListView
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView

from .forms import LoginForm, ProfileForm
from core.views import participated_projects
from core.models import consts

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    paginate_by = consts.paginate_by

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.GET.get('filter'):
            if self.request.GET.get('filter') == 'owners-of-favorite-projects':
                filtered_id = self.request.user.favorites.values('owner__id')
            elif self.request.GET.get('filter') == 'owners-of-participating-projects':
                filtered_id = self.request.user.participated_projects().values('owner__id')
            elif self.request.GET.get('filter') == 'interested-in-my-projects':
                filtered_id = self.model.objects.filter(favorites__in=self.request.user.owned_projects()).values('id')
            elif self.request.GET.get('filter') == 'participants-of-my-projects':
                filtered_id = self.request.user.owned_projects().select_related('participants').values(
                    'participants__id')
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
        if not form.is_valid():
            print(form.errors)
            return render(request, self.template_name, {'form': form})
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return render(request, self.template_name, {'form': form})
        login(request, user)
        messages.success(request, f'Добро пожаловать, {user.get_short_name()}!')
        return redirect('projects:mainpage')


def user_detail(request, user_id):
    template_name = 'users/user-details.html'
    user = get_object_or_404(User, id=user_id)
    context = {"user": user}
    return render(request, template_name, context)


@login_required  # Доступ только авторизованным пользователям
def edit_profile(request):
    template_name = 'users/edit_profile.html'
    form = ProfileForm(request.POST or None, instance=request.user)
    if not form.is_valid():
        context = {'form': form}
        return render(request, template_name, context)
    form.save()
    return redirect('users:user_detail', user_id=request.user.id)


class PasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'user_id': self.request.user.id})
