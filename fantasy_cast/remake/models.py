from django.db import models
from imdb.models import MovieTitle


class Remake(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    movie = models.ForeignKey(
        MovieTitle, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.title)
