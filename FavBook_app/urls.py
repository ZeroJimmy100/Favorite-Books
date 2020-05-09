from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('books', views.),
    path('books/update', views),
    path('books/delete', views),
    path('books/<int:id_books', views),
    path('books/<int:view_books', views),
    path('books/add_favorite', views),
]