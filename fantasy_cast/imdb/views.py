
from rest_framework.views import APIView
from rest_framework.response import Response

from imdb.models import MovieTitle
from imdb.serializers import MovieSerializer


class MovieSuggestions(APIView):

    def get(self, request, format=None):

        query = request.query_params.get('query')

        movies = MovieTitle.objects.filter(primary_title__iexact=query)

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
