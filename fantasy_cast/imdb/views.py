from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from imdb.models import MovieTitle
from imdb.serializers import MovieSerializer


class MovieSuggestions(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        query = request.query_params.get('query')

        movies = MovieTitle.objects.filter(primary_title__iexact=query)

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
