from rest_framework import serializers
from imdb.models import MovieTitle


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieTitle
        fields = '__all__'
