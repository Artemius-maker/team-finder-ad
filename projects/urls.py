from django.urls import path

from . import views

app_name = "projects"
urlpatterns = [
    path('list/', views.HomepageView.as_view(), name='mainpage'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/complete/', views.project_complete,
         name='project_complete'),
    path('<int:project_id>/toggle-participate/', views.toggle_participate,
         name='toggle_participate'),
    path('<int:project_id>/toggle-favorite/', views.toggle_favorite,
         name='toggle_favorite'),
    path('create-project/', views.create_edit_project,
         name='create_project'),
    path('<int:project_id>/edit/', views.create_edit_project,
         name='edit_project'),
]
