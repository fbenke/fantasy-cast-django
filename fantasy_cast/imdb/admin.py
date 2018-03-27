from django.contrib import admin
from imdb import models


class MovieTitleAdmin(admin.ModelAdmin):
    list_display = ('tconst', 'title_type', 'primary_title')


admin.site.register(models.MovieTitle, MovieTitleAdmin)
admin.site.register(models.Genre, admin.ModelAdmin)
admin.site.register(models.TitleType, admin.ModelAdmin)


class PersonAdmin(admin.ModelAdmin):

    list_display = ('nconst', 'primary_name')

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['known_for_titles', ]


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Profession, admin.ModelAdmin)
