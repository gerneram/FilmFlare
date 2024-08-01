from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import TextItemCreate,TextItemDelete



urlpatterns = [
    path('', views.index ),
    path('text/add/', TextItemCreate.as_view(), name='add-text'),
    path('text/delete/<int:pk>/', TextItemDelete.as_view(), name='delete-text'),
    path('get_movies/', views.get_movies, name='get_movies'),
    path('add_comment/<int:film_id>/', views.add_comment, name='add_comment'),
    path('get_comments/<int:film_id>/', views.get_comments, name='get_comments'),


]

urlpatterns += staticfiles_urlpatterns()
