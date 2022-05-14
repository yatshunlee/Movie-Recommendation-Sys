from django.db import models
from django.contrib.auth.models import User #get User
from django.urls import reverse  # To generate URLS by reversing URL patterns
# Create your models here.

class Movie(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField() # not allow only Year => must change into IntegerField instead
    # poster = models.TextField()
    description = models.TextField()

    # ManyToManyField used because a genre can contain many movies and a movie can cover many genres.
    # genre = models.ManyToManyField(BelongsToGenres)

    # ordering of output
    class Meta:
        ordering = ['title']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.id} ({self.title})'
   
   #show genre in admin page of Movie
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.genre for genre in self.genre.all()[:3]) #show first 3 genre in admin page

    display_genre.short_description = 'Genre'
    
    def get_absolute_url(self):
        """Returns the url to access a particular movie instance."""
        return reverse('movie-detail', args=[str(self.id)])


# class User(models.Model):
    # """A typical class defining a model, derived from the Model class."""

    # # Fields
    # user_id = models.CharField(max_length=64, primary_key=True)
    # username = models.CharField(max_length=20, help_text='Enter field documentation')
    # password = models.CharField(max_length=20, help_text='Enter field documentation')
  

    # # ordering of output
    # class Meta:
        # ordering = ['user_id']

    # # Methods
    # def __str__(self):
        # """String for representing the MyModelName object (in Admin site etc.)."""
        # return f'{self.user_id}'


class BelongsToGenres(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    # genre_id = models.IntegerField(max_length=64, primary_key=True)
    movie_id = models.ForeignKey(Movie, db_column='movie_id', on_delete=models.CASCADE)
    genre = models.CharField(max_length=64)


    # ordering of output
    class Meta:
        unique_together = (('movie_id', 'genre'),)
        ordering = ['genre']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.genre}'


class Rating(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    rating = models.IntegerField(('rating'))
    timestamp = models.IntegerField(('timestamp'))
    review = models.TextField(('review'), max_length=500)

    # FK
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, db_column='movie_id', on_delete=models.CASCADE)

    # ordering of output
    class Meta:
        ordering = ['user_id']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'User{self.user_id} Movie{self.movie_id} Rating ({self.rating})'


class Comment(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    id = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=500)
    timestamp = models.IntegerField()

    # FK
    rating_id = models.ForeignKey(Rating, db_column='rating_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)

    # ordering of output
    class Meta:
        ordering = ['id']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'Cid{self.id} User {self.user_id} timestamp ({self.timestamp})'