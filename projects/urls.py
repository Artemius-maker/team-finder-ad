from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path('projects/list/', views.HomepageView.as_view(), name='mainpage'),
    path('projects/favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/complete/', views.project_complete,
         name='project_complete'),
    path('projects/<int:project_id>/toggle_participate/', views.toggle_participate,
         name='toggle_participate'),
    path('projects/create-project/', views.create_edit_project,
         name='create_project'),
    path('projects/<int:project_id>/edit-project/', views.create_edit_project,
         name='edit_project'),
]
