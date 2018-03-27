import logging
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from django.db.utils import DataError

from imdb.models import MovieTitle, Genre, TitleType
from imdb.management.commands.converter_utils import convert_int, convert_boolean
from imdb.management.commands.load_name_basics import reset_tables as reset_person_tables


logger = logging.getLogger('django')


def reset_tables():

    reset_person_tables()

    with connections['default'].cursor() as cursor:

        query = '''
            delete from imdb_movietitle_genres;
            delete from imdb_movietitle;
            delete from imdb_titletype;
            delete from imdb_genre;
            alter sequence imdb_movietitle_id_seq restart with 1;
            alter sequence imdb_movietitle_genres_id_seq restart with 1;
            alter sequence imdb_titletype_id_seq restart with 1;
            select setval(pg_get_serial_sequence(' imdb_movietitle_genres', 'id'), coalesce(max(id),0) + 1, false) from imdb_movietitle_genres;
            select setval(pg_get_serial_sequence(' imdb_movietitle', 'id'), coalesce(max(id),0) + 1, false) from imdb_movietitle;
            select setval(pg_get_serial_sequence(' imdb_titletype', 'id'), coalesce(max(id),0) + 1, false) from imdb_titletype;
            select setval(pg_get_serial_sequence(' imdb_genre', 'id'), coalesce(max(id),0) + 1, false) from imdb_genre;
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

            for line in list(f):

                try:
                    entry = line.rstrip('\n').split('\t')

                    movie = MovieTitle.objects.create(
                        tconst=entry[0],
                        primary_title=entry[2],
                        original_title=entry[3],
                        is_adult=convert_boolean(entry[4]),
                        start_year=convert_int(entry[5]),
                        end_year=convert_int(entry[6]),
                        runtime_minutes=convert_int(entry[7])
                    )

                    title_type, _ = TitleType.objects.update_or_create(name=entry[
                                                                       1])
                    movie.title_type = title_type
                    movie.save()

                    if entry[8] != '\\N':

                        for g in entry[8].split(','):
                            genre, _ = Genre.objects.update_or_create(name=g)
                            movie.genres.add(genre)

                except DataError as e:
                    logger.info(e)

        except FileNotFoundError:
            print('File could not be found')
