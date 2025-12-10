from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_events, name='view_events'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/add/', views.add_favorite, name='add_favorite'),
    path('favorites/delete/', views.delete_favorite, name='delete_favorite'),
]
