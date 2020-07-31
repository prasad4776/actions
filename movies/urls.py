from django.urls import path
from .views import FilmView, home

urlpatterns = [
    path("movies", FilmView.as_view(), name="get-and-create-movies"),
    path("movies/del/<int:pk>", FilmView.as_view(), name="delete-movie"),
    path("movies/edit/<int:pk>", FilmView.as_view(), name="update-movie"),
    path("", home, name="home"),
]
