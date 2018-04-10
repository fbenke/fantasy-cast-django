import logging
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from django.db.utils import DataError

from imdb.models import Profession, Person, MovieTitle
from imdb.management.commands.converter_utils import convert_int


logger = logging.getLogger('django')


def reset_tables():
    with connections['default'].cursor() as cursor:

        query = '''
            delete from imdb_person_known_for_titles;
            delete from imdb_person_primary_profession;
            delete from imdb_person;
            delete from imdb_profession;
            alter sequence imdb_person_known_for_titles_id_seq restart with 1;
            alter sequence imdb_person_primary_profession_id_seq restart with 1;
            alter sequence imdb_person_id_seq restart with 1;
            alter sequence imdb_profession_id_seq restart with 1;
            select setval(pg_get_serial_sequence(' imdb_person_known_for_titles', 'id'), coalesce(max(id),0) + 1, false) from imdb_person_known_for_titles;
            select setval(pg_get_serial_sequence(' imdb_person_primary_profession', 'id'), coalesce(max(id),0) + 1, false) from imdb_person_primary_profession;
            select setval(pg_get_serial_sequence(' imdb_person', 'id'), coalesce(max(id),0) + 1, false) from imdb_person;
            select setval(pg_get_serial_sequence(' imdb_profession', 'id'), coalesce(max(id),0) + 1, false) from imdb_profession;
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

                    person = Person.objects.create(
                        nconst=entry[0],
                        primary_name=entry[1],
                        birth_year=convert_int(entry[2]),
                        death_year=convert_int(entry[3])
                    )

                    if entry[4] != '\\N' and entry[4] != '':

                        for p in entry[4].split(','):
                            profession, _ = Profession.objects.update_or_create(
                                name=p)
                            person.primary_profession.add(profession)

                    if entry[5] != '\\N':

                        for t in entry[5].split(','):

                            try:

                                movie_title = MovieTitle.objects.get(tconst=t)
                                person.known_for_titles.add(movie_title)

                            except MovieTitle.DoesNotExist as e:
                                pass

                except DataError as e:
                    logger.info('%s: %s' % (e, line))

        except FileNotFoundError:
            print('File could not be found')
