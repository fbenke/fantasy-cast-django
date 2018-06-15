from collections import OrderedDict

from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from imdb.constants import PRINCIPAL_CATEGORY_ACTOR
from imdb.index import get_title_suggestions
from imdb.models import MovieTitle, Principal
from imdb.serializers import MovieSerializer, PrincipalSerializer


class MovieSuggestions(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = MovieSerializer

    def get_queryset(self):

        query = self.request.query_params.get('query')
        if not query:
            raise ParseError('Missing query parameter')

        limit = self.request.query_params.get('limit', 10)
        results = get_title_suggestions(query, limit)

        qs_sorted = list()
        for v in results:
            qs_sorted.append(MovieTitle.objects.get(tconst=v[0]))

        return qs_sorted


class PrincipalSuggestions(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = PrincipalSerializer

    def get_queryset(self):

        movie_id = self.request.query_params.get('movie_id')

        if not movie_id:
            raise ParseError('Missing movie_id parameter')

        return Principal.objects.filter(
            movie_title_id=movie_id,
            category__name__in=PRINCIPAL_CATEGORY_ACTOR)


def get_cast(imdb_id):

    return Principal.objects.filter(
        movie_title_id=imdb_id,
        category__name__in=PRINCIPAL_CATEGORY_ACTOR)
