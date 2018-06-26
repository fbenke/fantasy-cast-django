import logging
import tmdbsimple as tmdb

from django.conf import settings

from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tmdb import constants as c
from tmdb.serializers import MovieSerializer
from tmdb.models import Movie


from imdb.constants import TITLE_TYPE_MOVIE, TITLE_TYPE_SERIES, TITLE_TYPE_SHORT
from imdb.models import MovieTitle as ImdbMovie

tmdb.API_KEY = settings.TMDB_API_KEY
logger = logging.getLogger('django')


def get_movie(r):

    return Movie(
        tmdb_id=r.get('id'),
        title=r.get('title'),
        release_date=r.get('release_date'),
        popularity=r.get('popularity'),
        overview=r.get('overview') or '',
        original_title=r.get('original_title'),
        original_language=r.get('original_language'),
        vote_count=r.get('vote_count'),
        vote_average=r.get('vote_average'),
        backdrop_path=r.get('backdrop_path') or '',
        poster_path=r.get('poster_path') or '',
        genres=r.get('genre_ids'),
        is_adult=r.get('adult'),
        is_video=r.get('video')
    )


class MovieSuggestions(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        search = tmdb.Search()
        query = request.query_params.get('query')

        if not query:
            movies = []

        else:
            search.movie(query=query)

            movies = []

            for r in search.results:
                movies.append(get_movie(r))
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)


class GetMovie(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, imdb_id, format=None):
        try:
            imdb_movie = ImdbMovie.objects.get(id=imdb_id)
            find = tmdb.Find(id=imdb_movie.tconst)
            response = find.info(external_source=c.API_PARAM_EXTERNAL_SOURCES)

            if imdb_movie.title_type.name in [TITLE_TYPE_MOVIE, TITLE_TYPE_SHORT]:
                results = response[c.API_RESPONSE_MOVIE_RESULTS]
            elif imdb_movie.title_type.name == TITLE_TYPE_SERIES:
                results = response[c.API_RESPONSE_TV_SERIES_RESULTS]
            else:
                return Response({})

            if len(results) > 1:
                logger.info('More than one result for imdb id %s (%s)' %
                            (imdb_id, response))

            elif len(results) == 1:
                serializer = MovieSerializer(get_movie(results[0]))
                return Response(serializer.data)

            return Response({})

        except ImdbMovie.DoesNotExist:
            raise ParseError('Invalid imdb id')


def get_cast(tmdb_id, imdb_id):
    imdb_movie = ImdbMovie.objects.get(id=imdb_id)
    if imdb_movie.title_type.name == TITLE_TYPE_SERIES:
        tv = tmdb.TV(id=tmdb_id)
        return tv.credits().get(c.API_RESPONSE_CAST)
    elif imdb_movie.title_type.name in [TITLE_TYPE_MOVIE, TITLE_TYPE_SHORT]:
        movies = tmdb.Movies(id=tmdb_id)
        return movies.credits().get(c.API_RESPONSE_CAST)
