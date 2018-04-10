import logging
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from django.db.utils import DataError

from imdb.models import MovieTitle, Person, Principal, Category


logger = logging.getLogger('django')


def reset_tables():
    with connections['default'].cursor() as cursor:

        query = '''
            delete from imdb_principal;
            delete from imdb_category;
            alter sequence imdb_principal_id_seq restart with 1;
            alter sequence imdb_category_id_seq restart with 1;
            select setval(pg_get_serial_sequence(' imdb_principal', 'id'), coalesce(max(id),0) + 1, false) from imdb_principal;
            select setval(pg_get_serial_sequence(' imdb_category', 'id'), coalesce(max(id),0) + 1, false) from imdb_category;
        '''

        cursor.execute(query)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):

        reset_tables()

        try:
            path = os.path.join(settings.PROJECT_ROOT, options['path'])
            f = open(path, 'r')

            next(f)

            for line in f:

                try:
                    entry = line.rstrip('\n').split('\t')
                    movie = MovieTitle.objects.get(tconst=entry[0])

                    person = Person.objects.get(nconst=entry[2])
                    principal = Principal(
                        movie_title=movie,
                        person=person,
                        ordering=entry[1],
                        job=entry[4] if entry[4] != '\\N' else '',
                        characters=entry[5] if entry[5] != '\\N' else ''
                    )

                    category, _ = Category.objects.update_or_create(
                        name=entry[3])
                    principal.category = category
                    principal.save()

                except (MovieTitle.DoesNotExist, Person.DoesNotExist) as e:
                    pass

                except DataError as e:
                    logger.info('%s: %s' % (e, line))

        except FileNotFoundError:
            print('File could not be found')
