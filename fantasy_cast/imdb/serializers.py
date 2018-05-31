from rest_framework import serializers
from imdb.models import MovieTitle, TitleType


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieTitle
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['title_type'] = instance.title_type.name
        return ret
