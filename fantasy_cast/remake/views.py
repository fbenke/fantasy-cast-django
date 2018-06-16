from django.core.exceptions import ValidationError

from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from remake import models as m
from remake import serializers as s

from tmdb.views import get_cast as get_tmdb_cast
from imdb.views import get_cast as get_imdb_cast


class CreateRemake(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = s.CreateRemakeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RemakeList(generics.ListAPIView):
    queryset = m.Remake.objects.filter(is_open=True)
    serializer_class = s.RemakeListSerializer


class RemakeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = m.Remake.objects.all()
    serializer_class = s.RemakeNestedSerializer


class GetCharacterSuggestions(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        imdb_id = self.request.query_params.get('imdbId')
        tmdb_id = self.request.query_params.get('tmdbId')

        if not imdb_id:
            raise ParseError('Missing query parameter')

        characters = []

        if tmdb_id:
            for c in get_tmdb_cast(tmdb_id, imdb_id):
                character = m.Character(
                    character=c.get('character'),
                    actor_name=c.get('name'),
                    tmdb_profile_path=c.get('profile_path') or '',
                    tmdb_id=c.get('id')
                )

                try:
                    character.clean_fields(exclude=('remake'))
                    characters.append(character)
                except ValidationError:
                    pass

        if not characters:
            for c in get_imdb_cast(imdb_id):

                character = m.Character(
                    character=c.characters.replace(
                        '\"', '').replace('[', '').replace(']', ''),
                    actor_name=c.person.primary_name,
                    imdb_principal=c
                )

                try:
                    character.clean_fields(exclude=('remake'))
                    characters.append(character)
                except ValidationError as e:
                    print(e)
                    pass

        serializer = s.CharacterSerializer(characters, many=True)
        return Response(serializer.data)
