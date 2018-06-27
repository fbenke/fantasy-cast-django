from django.contrib import admin
from remake import models


class CharacterInline(admin.TabularInline):
    model = models.Character
    fields = ('id', 'character', 'actor_name',
                    'tmdb_id', 'imdb_principal')

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['imdb_principal', ]


class RemakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'movie', 'user')

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['user', 'movie']

    inlines = [
        CharacterInline,
    ]

admin.site.register(models.Remake, RemakeAdmin)


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'character', 'actor_name',
                    'tmdb_id', 'imdb_principal')

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['imdb_principal', ]

admin.site.register(models.Character, CharacterAdmin)
