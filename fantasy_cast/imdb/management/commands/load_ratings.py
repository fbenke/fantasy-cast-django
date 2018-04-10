import logging
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections

from imdb.models import MovieTitle


logger = logging.getLogger('django')


def reset_tables():

    with connections['default'].cursor() as cursor:

        query = '''
            update imdb_movietitle set average_rating = NULL, number_votes = NULL;
        '''

        cursor.execute(query)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):

        try:

            reset_tables()

            path = os.path.join(settings.PROJECT_ROOT, options['path'])
            f = open(path, 'r')

            next(f)

            for line in list(f):

                try:

                    entry = line.rstrip('\n').split('\t')
                    movie = MovieTitle.objects.get(tconst=entry[0])
                    movie.average_rating = entry[1]
                    movie.number_votes = entry[2]
                    movie.save()

                except MovieTitle.DoesNotExist:
                    pass

        except FileNotFoundError:
            print('File could not be found')
