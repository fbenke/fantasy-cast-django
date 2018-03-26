from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class TitleType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class MovieTitle(models.Model):

    tconst = models.CharField(max_length=50, unique=True)
    title_type = models.ForeignKey(
        TitleType, on_delete=models.CASCADE, null=True)
    primary_title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150)
    is_adult = models.BooleanField(default=False)
    start_year = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)
    runtime_minutes = models.IntegerField(null=True)
    genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.primary_title)


class Profession(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Person(models.Model):
    nconst = models.CharField(max_length=50, unique=True)
    primary_name = models.CharField(max_length=150)
    birth_year = models.IntegerField(null=True)
    death_year = models.IntegerField(null=True)
    primary_profession = models.ManyToManyField(Profession)
    known_for_titles = models.ManyToManyField(MovieTitle)

    def __str__(self):
        return str(self.primary_name)
