from rest_framework import serializers
from tmdb.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = ('id',)
