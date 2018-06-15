from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from remake.models import Remake
from remake import serializers as s

from tmdb.views import get_cast


class RemakeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Remake.objects.all()
    serializer_class = s.RemakeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RemakeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Remake.objects.all()
    serializer_class = s.RemakeNestedSerializer


class GetActorSuggestions(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        remake = Remake.objects.get(id=pk)

        print(get_cast(remake.tmdb_id))
        return Response({})
