import os
from datetime import datetime
from data_interface import DataInterface
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections


class ElasticSearchInterface(DataInterface):
    '''
    Data interface with Elasticsearch connection.
    Derived from DataInterface.
    Supports the app's 2 POST and 2 GET API calls.
    '''

    def __init__(self):
        '''
        Defines the default connection to Elasticsearch server, the module instance, the index name,
        and the document type name.
        '''

        es_host = os.environ['ES_server'] + ":" + os.environ['ES_port']
        connections.create_connection(hosts=[es_host])
        self.es = Elasticsearch()
        self.index = 'events'
        self.doc_type = 'initial'

    def log_initial(self, uuid, symbol, is_vowel):
        '''
        Logs an initial POST event by indexing a new initial event.

        :param uuid: Event UUID
        :type uuid: string
        :param symbol: Symbol in the alphabet
        :type symbol: string
        :param is_vowel: Symbol is_vowel flag
        :type is_vowel: int
        '''

        doc = {
            'event_type': self.doc_type,
            'date': str(datetime.utcnow()),
            'symbol': symbol,
            'is_vowel': is_vowel,
            'followups': list()
        }
        self.es.index(index=self.index, doc_type=self.doc_type, id=uuid, body=doc)

    def log_followup(self, uuid):
        '''
        Logs a followup POST event by updating the relevant initial event log.

        :param uuid: Event UUID
        :type uuid: string
        '''

        script = {
            'script': {
                'source': 'ctx._source.followups.add(params.followup)',
                'params': {
                    'followup': {
                        'date': str(datetime.utcnow())
                    }
                }
            }
        }
        self.es.update(index=self.index, doc_type=self.doc_type, id=uuid, body=script)

    def get_date_stats(self, symbol):
        '''
        Queries and returns the date stats for the given symbol.

        :param symbol: Symbol in the alphabet
        :type symbol: string
        :return result: Stats of the symbol
        :rtype result: dict
        '''
        response = Search(using=self.es, index=self.index)\
            .query('match', symbol=symbol)\
            .aggs.metric('date_stats', 'stats', field='date')\
            .execute()
        stats = response.aggregations.date_stats
        result = {
            'symbol': symbol,
            'count': stats.count,
            'earliest': stats.min_as_string,
            'latest': stats.max_as_string
        }
        return result

    def get_followups_count(self, symbol):
        '''
        Queries and counts the number of followups for the given symbol.

        :param symbol: Symbol in the alphabet
        :type symbol: string
        :return count: Followups count
        :rtype count: int
        '''
        count = 0
        query = Search(using=self.es, index=self.index) \
            .query('match', symbol=symbol)
        for hit in query.scan():
            count += len(hit.followups)
        return count

    def symbol_aggregates(self, symbol):
        '''
        Aggregates and returns the stats for the given symbol.

        :param symbol: Symbol in the alphabet
        :type symbol: string
        :return result: Stats of the symbol
        :rtype result: dict
        '''
        result = self.get_date_stats(symbol)
        result['followups'] = self.get_followups_count(symbol)
        return result

    def range_aggregates(self, lower, upper):
        pass
