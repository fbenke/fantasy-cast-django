from rest_framework import serializers
from remake import models


class RemakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Remake
        exclude = ('user',)


class RemakeNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Remake
        fields = '__all__'
        depth = 1


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Character
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret['id']:
            ret['id'] = instance.tmdb_id if instance.tmdb_id else instance.imdb_principal.id
        return ret
