from django.contrib import admin
from remake import models


class RemakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'movie', 'user')

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + ['user', 'movie']

admin.site.register(models.Remake, RemakeAdmin)
