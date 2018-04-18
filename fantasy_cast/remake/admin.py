from django.contrib import admin
from remake import models

admin.site.register(models.Remake, admin.ModelAdmin)
