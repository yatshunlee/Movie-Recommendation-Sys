from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.MovieListView.as_view(), name='movies'), #movie list page
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'), #view movie by specific id
   
    path('accounts/', include('django.contrib.auth.urls')), #Add Django site authentication urls (for login, logout, password management)
    
    path('myratings/', views.RatedMoviesByUserListView.as_view(), name='my-rated'),
    path(r'rated/', views.RatedMoviesAllListView.as_view(), name='all-rated'),
    
    path('genres/', views.GenreListView.as_view(), name='genres'), #genres list page
    path('users/', views.UserListView.as_view(), name='users'), #users list page

    
    path('maintenance/', views.Maintenance.as_view(), name='maintenance'),     
    path('movie/create/', views.MovieCreate.as_view(), name='movie_create'),
    path('movie/<int:pk>/update/', views.MovieUpdate.as_view(), name='movie_update'),
    path('movie/<int:pk>/delete/', views.MovieDelete.as_view(), name='movie_delete'),    
    path('genres/create/', views.GenreCreate.as_view(), name='genre_create'),
    path('genres/<int:pk>/update/', views.GenreUpdate.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', views.GenreDelete.as_view(), name='genre_delete'), 
    path('users/create/', views.UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'), 

    path("register", views.register_request, name="register"),    
    
    path("movie/<int:pk>/rating/", views.rating_movie_user, name='rating-movie-user'),
    #path('rating/create/', views.RatingCreate.as_view(), name='rating_create'),
    
    path('genreMovie/<str:genre>', views.GenreMovieDetailView.as_view(), name='genreMovie'),
]