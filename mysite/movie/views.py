from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Rating, BelongsToGenres, Comment  # import model
from django.views import generic  # view data
from django.contrib.auth.mixins import LoginRequiredMixin  # only login user can use
from django.contrib.auth.admin import UserAdmin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse  # for delete
from django.views.generic import TemplateView
from django.contrib.auth.models import User
# Register
from .forms import NewUserForm, MovieRatingForm
from django.contrib.auth import login
from django.contrib import messages  # show error message

from django.template.defaulttags import register

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from datetime import datetime, date
import calendar;
import time;
from django.http import HttpResponseRedirect, HttpResponseForbidden


# Create your views here.

@register.filter
def keyvalue(dict, key1):
    return dict[key1]

@register.filter
def keyvalueempty(dict, key):
    return len(dict[key])==0

# Machine Learning
def recommended_by(m_id):
    # get input from db
    ratings = pd.DataFrame(list(Rating.objects.all().values()))

    # preprocessing
    movie_features = ratings.pivot_table(values="rating",
                                         index="movie_id_id",
                                         columns="user_id_id").fillna(0)

    # check if the movie is rated
    try:
        x = movie_features.loc[m_id, :].values.reshape(1, -1)
    except:
        return [-1]


    movie_vectors = csr_matrix(movie_features)

    # instantiation
    knn = NearestNeighbors(metric="cosine")
    # fit_predict
    knn.fit(movie_vectors)

    distances, indices = knn.kneighbors(x, n_neighbors=6)
    return movie_features.index[indices[0]]


# get comment, rating, and user id from db
def show_reviews(m_id):
    related_reviews = {}

    for user_review in Rating.objects.raw(f'''SELECT id, rating, timestamp, review
                                              FROM movie_rating WHERE movie_id = {m_id}
                                              ORDER BY timestamp DESC'''):
        related_reviews[user_review.id] = {}
        related_reviews[user_review.id]['timestamp'] = datetime.fromtimestamp(int(user_review.timestamp))
        related_reviews[user_review.id]['review'] = user_review.review
        related_reviews[user_review.id]['rating'] = user_review.rating
        # something wrong with the columns in db
        related_reviews[user_review.id]['username'] = user_review.user_id

    return related_reviews

# check if the user rated the movie
def check_rated(movie_id,user_id):
    try:
        return Rating.objects.get(movie_id_id= movie_id, user_id_id = user_id)
    except Rating.DoesNotExist:
        return False

# retrieve comment {review_id: {username: username, timestamp: timestamp, comment: comment}}
def retrieve_comments_of_review(review_ids):
    comments = {}
    for r_id in review_ids:
        comments[r_id] = []
        for cm in Comment.objects.all().filter(rating_id=r_id):
            comments[r_id].append((cm.user_id,datetime.fromtimestamp(int(cm.timestamp)),cm.comment))
    return comments

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_movies = Movie.objects.all().count()
    # The 'all()' is implied by default.
    num_rating = Rating.objects.count()
    # Show set Genres
    num_genres = set([genre.genre for genre in BelongsToGenres.objects.all() if genre.genre != '(no genres listed)'])
    # Show new movie
    new_movies = []
    for new_movie in Movie.objects.order_by('-pk')[:10]:
        new = {}
        new['id'] = new_movie.id
        new['title'] = new_movie.title
        new['year'] = new_movie.year
        new_movies.append(new)


    context = {
        'num_movies': num_movies,
        'num_rating': num_rating,
        'num_genres': num_genres,
        'new_movies': new_movies,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class MovieListView(generic.ListView):  # show different movie
    """Generic class-based view for a list of movies."""
    model = Movie  # all record in movie
    paginate_by = 10  # 10 records for 1 page


class MovieDetailView(generic.DetailView):  # show particular movie details
    """Generic class-based detail view for a movie."""
    model = Movie

    def post(self, request, *args, **kwargs):
        # rating / review id
        form_id = request.POST.get('addcomment', False)
        # user id
        form_user = request.user.id
        # user comment
        form_comment = request.POST.get('comment', False)
        # current timestamp
        form_ts = datetime.now().timestamp()
        # insert comment tuple into db
        c = Comment(rating_id_id=form_id, user_id_id=form_user, timestamp=form_ts, comment=form_comment)
        c.save()
        return redirect(f'/movie/movie/{self.kwargs["pk"]}')

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        
        # retrieve tuple from database
        movie = Movie.objects.get(pk=self.kwargs['pk'])
        
        # searched movie info (storing into a dict)
        searched = {}
        searched['id'] = movie.id  # char
        searched['title'] = movie.title  # char
        searched['des'] = movie.description  # str
        searched['year'] = movie.year  # int

        # use m_id to search genres
        for genre in BelongsToGenres.objects.raw(
                f'SELECT * FROM movie_belongstogenres WHERE movie_id = {searched["id"]}'):
            try:
                searched['genres'] += [genre.genre]
            except:
                searched['genres'] = [genre.genre]

        # machine learning model fit predict
        recommended_ids = tuple(recommended_by(searched['id']))

        # the movie is rated by user
        if recommended_ids[0] != -1:
            # convert ids into titles as a list
            recommended_movies = []
            for m in Movie.objects.raw(f'SELECT id, title FROM movie_movie WHERE id IN {recommended_ids}'):
                if m.id != searched['id']:
                    mv = {}
                    mv['id'] = m.id
                    mv['title'] = m.title
                    recommended_movies.append(mv)
        else:
            recommended_movies = False

        # get movie reviews
        related_reviews = show_reviews(searched["id"])
        
        # front-end application
        context['rated'] = check_rated(searched["id"], self.request.user.id)
        context['isUser'] = self.request.user.id
        context['movie'] = movie
        context['searched'] = searched
        context['recommended'] = recommended_movies
        context['related_reviews'] = related_reviews
        context['comments'] = retrieve_comments_of_review(related_reviews.keys())

        # context['now'] = timezone.now()
        return context

    # except Movie.DoesNotExist:
    #     raise Http404('Movie does not exist')

    # from django.shortcuts import get_object_or_404
    # Movie = get_object_or_404(Movie, pk=primary_key)


class RatedMoviesByUserListView(LoginRequiredMixin, generic.ListView):  # show specific user's rating
    """Generic class-based view listing movies rated to current user."""
    model = Rating
    template_name = 'movie/rating_list_rated_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Rating.objects.filter(user_id=self.request.user)


class RatedMoviesAllListView(LoginRequiredMixin, generic.ListView):  # show all users rating
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Rating
    template_name = 'movie/rating_list_rated_all.html'
    paginate_by = 10




class GenreListView(generic.ListView):  # show different genre
    """Generic class-based view for a list of movies."""
    model = BelongsToGenres  # all record in genre
    paginate_by = 10  # 10 records for 1 page


class UserListView(generic.ListView):  # show different user
    model = User  # all record in user
    paginate_by = 10  # 10 records for 1 page


class MovieCreate(CreateView):
    model = Movie
    fields = ['title','year','description']

    #initial = {"id": "%d" %(max(id)+1)}

    # def get_initial(self):
        # initial = super(ResumeNew, self).get_initial()
        # initial.update({'id': self.request.user.id})
        # return initial
        
        
class MovieUpdate(UpdateView):
    model = Movie
    fields = ['title','year','description']

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['id'] = self.kwargs["pk"]
        except:
            pass
        return context


class MovieDelete(DeleteView):
    model = Movie
    success_url = reverse_lazy('movies')  # redirect to our movie list after a movie has been deleted


class GenreCreate(CreateView):
    model = BelongsToGenres
    fields = '__all__'
    success_url = reverse_lazy('genres')  # redirect to our genre list


class GenreUpdate(UpdateView):
    model = BelongsToGenres
    fields = '__all__'
    success_url = reverse_lazy('genres')  # redirect to our genre list


class GenreDelete(DeleteView):
    model = BelongsToGenres
    success_url = reverse_lazy('genres')  # redirect to our genre list after a movie has been deleted


class UserCreate(CreateView):
    model = User
    fields = ['username','password']
    success_url = reverse_lazy('users')  # redirect to our genre list


class UserUpdate(UpdateView):
    model = User
    fields = ['username','password']
    success_url = reverse_lazy('users')  # redirect to our genre list


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('users')  # redirect to our genre list after a movie has been deleted


class Maintenance(TemplateView):
    template_name = "movie/maintenance.html"


# Register account
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="movie/register.html", context={"register_form": form})


# rating movie
def rating_movie_user(request, pk):
    movie = Movie.objects.get(id=pk)
    review_inst = check_rated(movie.id, request.user.id)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # form attributes
        form_movie = pk
        form_user = request.user.id
        form_rating = request.POST.get('rating',False)
        form_review = request.POST.get('review',False)
        form_ts = datetime.now().timestamp()

        # delete rating
        if 'Delete' in request.POST:
            review_inst.delete()

        # add rating
        elif not review_inst:
            r = Rating(movie_id_id=form_movie,user_id_id=form_user,rating=form_rating,
                       review=form_review,timestamp=form_ts)
            r.save()

        # edit rating
        else:
            review_inst.rating = form_rating
            review_inst.review = form_review
            review_inst.timestamp = form_ts
            review_inst.save()

        return redirect(f"/movie/movie/{pk}")

    # If this is a GET (or any other method) create the default form.
    else:
        form = MovieRatingForm()

        context = {
            'review_inst': review_inst,
            'title': movie.title,
            'form': form,
            'user': request.user
        }

        return render(request, 'movie/movie_rating_user.html', context)

# class RatingCreate(CreateView):
# model = Rating
# fields = ['rating','review']


def show_GenreMovie(m_genre):
     related_genre = {}

     for movie_genres in BelongsToGenres.objects.raw(f'''SELECT movie_id FROM movie_belongstogenres WHERE genre = {m_genre}'''):

         related_genre['movieByGenre'] = [movie_genres.title]
     return related_genre



class GenreMovieDetailView(TemplateView):  #generic.DetailView?
    template_name = "movie/belongstogenres_detail.html"
    model = BelongsToGenres
    paginate_by = 10

    
    # def get_queryset(self):
        # return BelongsToGenres.objects.filter(genre=self.genre)
        # #return show_GenreMovie(self.genre)
    def get_context_data(self, **kwargs):
        context = super(GenreMovieDetailView, self).get_context_data(**kwargs)
        
        #related_genres = show_GenreMovie(self.genre)
        #context['related_genres'] = related_genres
        
        related_genre = {}

#use genre to find movie
        for movie_genres in BelongsToGenres.objects.raw(f'''SELECT movie_id FROM movie_belongstogenres WHERE genre = {self.genre}'''):

            related_genre['movieByGenre'] = [movie_genres.title]


        context['related_genres'] = related_genre
        return context