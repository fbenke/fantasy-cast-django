import tmdbsimple as tmdb

from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tmdb.serializers import MovieSerializer
from tmdb.models import Movie

tmdb.API_KEY = settings.TMDB_API_KEY


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

            for s in search.results:

                movies.append(
                    Movie(tmdb_id=s['id'],
                          title=s['title'],
                          release_date=s['release_date'],
                          popularity=s['popularity'],
                          overview=s['overview'],
                          original_title=s['original_title'],
                          original_language=s['original_language'],
                          vote_count=s['vote_count'],
                          vote_average=s['vote_average'],
                          backdrop_path=s['backdrop_path'],
                          poster_path=s['poster_path'],
                          genres=s['genre_ids'],
                          is_adult=s['adult'],
                          is_video=s['video']
                          )
                )

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
