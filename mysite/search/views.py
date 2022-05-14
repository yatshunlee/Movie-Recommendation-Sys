from django.shortcuts import render, redirect

from movie.models import Movie

# Create your views here.
def search_movie(request):

    if request.POST:

        # get movie title from user
        searched = {}
        searched['title'] = request.POST['InputTitle']


        # try to retrieve the movie id from db
        # if len(Movie.objects.raw(f'SELECT id FROM movie_movie WHERE title = "{searched["title"]}"')) == 1:
        #     # use title to search m_id, des, year, poster
        #     for movie in Movie.objects.raw(f'SELECT id FROM movie_movie WHERE title = "{searched["title"]}"'):
        #         searched['id'] = movie.id # char
        #         return redirect(f'/movie/movie/{searched["id"]}')

        if len(Movie.objects.raw(f'''SELECT id FROM movie_movie WHERE title LIKE "%{searched["title"]}%"''')) >= 1:
            # # use title to search m_id, des, year, poster
            possible_results = []

            for movie in Movie.objects.raw(f'SELECT id, title, year FROM movie_movie WHERE title LIKE "%{searched["title"]}%"'):
                possible = {}
                possible['possible_id'] = movie.id # char
                possible['possible_title'] = movie.title  # char
                possible['possible_year'] = movie.year # int
                possible_results.append(possible)

            # default order by year (descending order)
            possible_results = sorted(sorted(possible_results,
                                             key = lambda i: i['possible_title']),
                                      key=lambda i: i['possible_year'], reverse=True)

            return render(request,
                          'search/search.html',
                          {'possible_results': possible_results,
                           'typo': False})
        else:
            return render(request,
                          'search/search.html',
                          {'searched': searched,
                           'typo': True})

    else:
        # UTF-8 error column 'Title'
        available_movies = Movie.objects.all()
        return render(request,
                      'search/search.html',
                      {'available_movies': available_movies}) #