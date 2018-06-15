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
