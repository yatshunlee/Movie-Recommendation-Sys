from django.contrib import admin
from .models import Movie, User, Rating, BelongsToGenres, Comment #import model

# Register your models here.

#admin.site.register(Movie)
# Define the admin class
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year') #show column in admin page

# Register the admin class with the associated model
admin.site.register(Movie, MovieAdmin)


#admin.site.register(Rating)
# Register the Admin classes for Rating using the decorator
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'review', 'movie_id','user_id') #show column in admin page


#admin.site.register(Category)
# Register the Admin classes for BookInstance using the decorator
@admin.register(BelongsToGenres)
class BelongsToGenresAdmin(admin.ModelAdmin):
    #list_display = ('movie_id','genre') #show column in admin page
    pass

#admin.site.register(Category)
# Register the Admin classes for BookInstance using the decorator
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    #list_display = ('id','user_id,'timestamp') #show column in admin page
    pass
