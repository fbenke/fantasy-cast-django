import logging
from datetime import datetime
from random import randint

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

from imdb.constants import INDEX_TITLE_TYPES
from imdb.index import SEARCH_INDEX, INDEX_TITLE
from imdb.models import TitleType

from elasticsearch import Elasticsearch, helpers
es = Elasticsearch(getattr(settings, 'ELASTICSEARCH', [{'host': 'localhost'}]))

logger = logging.getLogger('django')


def index_imdb_titles(index):

    with connections['default'].cursor() as cursor:

        next_round = True
        offset = 0
        step_size = 80000

        title_type_ids = [str(i) for i in TitleType.objects.filter(
            name__in=INDEX_TITLE_TYPES).values_list('id', flat=True)]

        while next_round:

            logger.info('Next batch of title applications: %s' % offset)

            query = '''
                SELECT tconst, primary_title
                FROM imdb_movietitle m
                JOIN imdb_titletype t on m.title_type_id = t.id
                WHERE
                    start_year IS NOT NULL AND
                    t.id in (%s)
                ORDER BY m.id
                LIMIT %s
                OFFSET %s;
            ''' % (', '.join(title_type_ids), step_size, offset)

            cursor.execute(query)
            rows = cursor.fetchall()

            actions = [
                {
                    '_index': index,
                    '_type': 'index',
                    '_source': {
                        'id': row[0],
                        'title': row[1]
                    }
                }
                for row in rows
            ]

            helpers.bulk(es, actions)

            next_round = cursor.rowcount > 0
            offset += step_size


class Command(BaseCommand):

    def handle(self, *args, **options):

        existing_part_indices = [
            r for r in es.indices.get(index=INDEX_TITLE + '-*')]

        while True:
            number = randint(100, 999)
            new_index = '%s-%s' % (INDEX_TITLE, number)
            if new_index not in existing_part_indices:
                break

        es.indices.create(index=new_index, body=SEARCH_INDEX)

        logger.info('Start building search index: %s' % datetime.now())
        index_imdb_titles(new_index)
        logger.info('Finished building index: %s' % datetime.now())

        es.indices.put_alias(name=INDEX_TITLE, index=new_index)
        es.indices.put_settings(index=new_index,
                                body={'index': {'max_result_window': 500000}})

        for i in existing_part_indices:
            try:
                es.indices.delete(index=i)
            except Exception:
                pass
