from collections import OrderedDict

from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from imdb.models import MovieTitle
from imdb.serializers import MovieSerializer
from imdb.index import get_title_suggestions


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
