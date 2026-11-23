from django.urls import include, path, reverse_lazy
from . import views
from .forms import RegisterForm, LoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('login/', LoginView.as_view(authentication_form=LoginForm, template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', CreateView.as_view(
            template_name='users/register.html',
            form_class=RegisterForm,
            success_url=reverse_lazy('projects:mainpage'),
        ),
        name='register',
    ),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
