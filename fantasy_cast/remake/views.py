from rest_framework import generics

from remake.models import Remake
from remake.serializers import RemakeSerializer


class RemakeList(generics.ListCreateAPIView):
    queryset = Remake.objects.all()
    serializer_class = RemakeSerializer


class RemakeDetail(generics.RetrieveDestroyAPIView):
    queryset = Remake.objects.all()
    serializer_class = RemakeSerializer
