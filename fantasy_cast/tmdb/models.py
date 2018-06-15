from django.db import models


class Movie(models.Model):

    tmdb_id = models.IntegerField(unique=True)
    overview = models.CharField(max_length=150, default='')
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150)
    original_language = models.CharField(max_length=150)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    backdrop_path = models.CharField(max_length=150, default='')
    poster_path = models.CharField(max_length=150, default='')
    release_date = models.DateField()
    genres = models.CharField(max_length=150)
    is_adult = models.BooleanField()
    is_video = models.BooleanField()

    def __str__(self):
        return str(self.title)
