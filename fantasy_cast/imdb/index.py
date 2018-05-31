from elasticsearch import Elasticsearch

from django.conf import settings

es = Elasticsearch(getattr(settings, 'ELASTICSEARCH', [{'host': 'localhost'}]))

INDEX_TITLE = 'imdb-title'
SEARCH_INDEX = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
    },
    'mappings': {
        'index': {
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'title': {
                    'type': 'text'
                }
            }
        }
    }
}


def get_title_suggestions(title, no_results):

    query = {
        'query': {
            'match': {'title': title}
        }
    }

    titles = es.search(index=INDEX_TITLE, body=query, size=no_results)
    return [(t['_source']['id'], t['_score'])
            for t in titles['hits']['hits']]
