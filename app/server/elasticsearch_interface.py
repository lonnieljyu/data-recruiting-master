import os
from elasticsearch import Elasticsearch as es_dsl
import elasticsearch_dsl as es_dsl
from elasticsearch_dsl.connections import connections
from data_interface import DataInterface
from datetime import datetime

class ElasticSearchInterface(DataInterface):

    def __init__(self):
        es_host = os.environ['ES_server'] + ":" + os.environ['ES_port']
        connections.create_connection(hosts=[es_host])
        self.index = 'symbols'

    def log_initial(self, uuid, symbol, is_vowel):
        pass

    def log_folowup(self, uuid):
        pass

    def symbol_aggregates(self, symbol):
        pass

    def range_aggregates(self, lower, upper):
        pass