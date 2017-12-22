import os
import elasticsearch_dsl as es_dsl
from elasticsearch_dsl.connections import connections

# Connect to Elasticsearch server and create 'symbols' index
es_host = os.environ['ES_server'] + ":" + os.environ['ES_port']
connections.create_connection(hosts=[es_host])
index = es_dsl.Index('symbols').settings(number_of_shards=1)
index.create()