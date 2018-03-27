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
        TitleType, on_delete=models.CASCADE)
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


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Principal(models.Model):
    movie_title = models.ForeignKey(
        MovieTitle, on_delete=models.CASCADE)
    person = models.ForeignKey(
        Profession, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)


class Character(models.Model):
    name = models.CharField(max_length=50, unique=True)
    principal = models.ForeignKey(
        Principal, on_delete=models.CASCADE, related_name='characters')

    def __str__(self):
        return str(self.name)
