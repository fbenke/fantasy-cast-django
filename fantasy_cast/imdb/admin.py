from django.contrib import admin
from imdb import models


class MovieTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'tconst', 'title_type',
                    'primary_title', 'start_year', 'average_rating')
    search_fields = ['primary_title', 'original_title']
    list_filter = ['is_adult', 'title_type']

admin.site.register(models.MovieTitle, MovieTitleAdmin)
admin.site.register(models.Genre, admin.ModelAdmin)


class TitleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(models.TitleType, TitleTypeAdmin)


class PersonAdmin(admin.ModelAdmin):

    list_display = ('id', 'nconst', 'primary_name', 'birth_year', 'death_year')
    search_fields = ['primary_name', ]

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['known_for_titles', ]


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Profession, admin.ModelAdmin)


class PrincipalAdmin(admin.ModelAdmin):

    list_display = ('id', 'movie_title', 'person',
                    'category', 'job', 'characters')

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['movie_title', 'person']

admin.site.register(models.Principal, PrincipalAdmin)
admin.site.register(models.Category, TitleTypeAdmin)
