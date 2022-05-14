from django.urls import path
from .views import search_movie


urlpatterns = [
    path('', search_movie, name='search'),
    path('../movie/movie/<int:pk>', search_movie, name='movie-detail'),
]