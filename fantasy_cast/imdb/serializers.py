from rest_framework import serializers

from imdb.constants import INDEX_TITLE_LABELS
from imdb import models


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MovieTitle
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['title_type'] = INDEX_TITLE_LABELS[instance.title_type.name]
        return ret


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Person
        fields = ('id', 'nconst', 'primary_name')


class PrincipalSerializer(serializers.ModelSerializer):

    person = PersonSerializer(many=False, read_only=True)

    class Meta:
        model = models.Principal
        exclude = ('movie_title', 'category')
        depth = 1

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['characters'] = instance.characters.replace(
            '\"', '').replace('[', '').replace(']', '')
        return ret
