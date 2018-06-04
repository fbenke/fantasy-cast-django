from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from remake.models import Remake
from remake.serializers import RemakeSerializer


class RemakeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Remake.objects.all()
    serializer_class = RemakeSerializer


class RemakeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Remake.objects.all()
    serializer_class = RemakeSerializer
