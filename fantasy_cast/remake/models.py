from django.db import models


class Remake(models.Model):

    title = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.title)
