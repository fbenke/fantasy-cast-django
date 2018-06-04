from rest_framework import serializers

from imdb.constants import INDEX_TITLE_LABELS
from imdb.models import MovieTitle


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieTitle
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['title_type'] = INDEX_TITLE_LABELS[instance.title_type.name]
        return ret
