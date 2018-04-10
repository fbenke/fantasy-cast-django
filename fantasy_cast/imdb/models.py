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
    average_rating = models.DecimalField(
        null=True, max_digits=3, decimal_places=1)
    number_votes = models.IntegerField(null=True)

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

    class Meta:
        verbose_name = 'Principal Category'
        verbose_name_plural = 'Principal Categories'


class Principal(models.Model):
    movie_title = models.ForeignKey(
        MovieTitle, on_delete=models.CASCADE)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    job = models.CharField(max_length=150, default='')
    characters = models.CharField(max_length=150, default='')

    def __str__(self):
        return str('%s - %s' % (self.movie_title, self.person))
