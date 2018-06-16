from django.db import models

from account.models import CustomUser

from imdb.models import MovieTitle, Principal


class Remake(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    movie = models.ForeignKey(
        MovieTitle, on_delete=models.CASCADE)
    tmdb_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.title)


class Character(models.Model):

    character = models.CharField(max_length=150)
    actor_name = models.CharField(max_length=150)
    tmdb_profile_path = models.CharField(
        max_length=150, default='', blank=True)
    remake = models.ForeignKey(
        Remake, on_delete=models.CASCADE, related_name='characters')
    tmdb_id = models.IntegerField(null=True, blank=True)
    imdb_principal = models.ForeignKey(
        Principal, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.character)
