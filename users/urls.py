from django.urls import include, path, reverse_lazy
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

app_name = "users"

urlpatterns = [
    path('users/list/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/login/', views.login, name='login'),
    path('users/logout/', views.logout, name='logout'),
    path('users/register/', CreateView.as_view(
            template_name='/templates/users/register.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('projects/list'),
        ),
        name='registration',
    ),
    path('users/edit_profile/', views.edit_profile, name='edit_profile'),
]
