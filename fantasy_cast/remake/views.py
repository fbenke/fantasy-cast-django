from django.core.exceptions import ValidationError

from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
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
    serializer_class = s.RemakeDetailSerializer

    def delete(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
        return self.destroy(request, *args, **kwargs)


class CloseRemake(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, format=None):
        try:
            remake = m.Remake.objects.get(
                is_open=True, user=request.user, id=pk)
            remake.is_open = False
            remake.save()
            return Response()
        except m.Remake.DoesNotExist as e:
            raise ValidationError(e)


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
                    tmdb_id=c.get('id'),
                    order=c.get('order')
                )

                try:
                    character.clean_fields(exclude=('remake'))
                    characters.append(character)
                except ValidationError:
                    pass

        if not characters:
            order = 0
            for c in get_imdb_cast(imdb_id):

                character = m.Character(
                    character=c.characters.replace(
                        '\"', '').replace('[', '').replace(']', ''),
                    actor_name=c.person.primary_name,
                    imdb_principal=c,
                    order=order
                )

                try:
                    character.clean_fields(exclude=('remake'))
                    characters.append(character)
                    order += 1
                except ValidationError:
                    pass

        serializer = s.CharacterSerializer(characters, many=True)
        return Response(serializer.data)
