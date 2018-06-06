from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from remake.models import Remake
from remake.serializers import RemakeSerializer, RemakeNestedSerializer


class RemakeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Remake.objects.all()
    serializer_class = RemakeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RemakeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Remake.objects.all()
    serializer_class = RemakeNestedSerializer
