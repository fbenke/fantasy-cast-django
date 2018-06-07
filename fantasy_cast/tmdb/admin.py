from django.contrib import admin
from tmdb import models


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )


admin.site.register(models.Movie, MovieAdmin)
