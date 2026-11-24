from django.urls import include, path, reverse_lazy, reverse
from . import views
from .forms import RegisterForm, LoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView

app_name = "users"

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', CreateView.as_view(
        template_name='users/register.html',
        form_class=RegisterForm,
        success_url=reverse_lazy('users:login'),
    ),
         name='register',
         ),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.CustomPasswordChangeView.as_view(template_name='users/change_password.html'),
         name='change_password'),
]
