import os
from datetime import datetime
from data_interface import DataInterface
from elasticsearch import Elasticsearch
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

    def symbol_aggregates(self, symbol):
        pass

    def range_aggregates(self, lower, upper):
        pass
