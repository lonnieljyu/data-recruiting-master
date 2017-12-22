import os
import elasticsearch_dsl as es_dsl
from elasticsearch_dsl.connections import connections

# Define connection to Elasticsearch server
es_host = os.environ['ES_server'] + ":" + os.environ['ES_port']
connections.create_connection(hosts=[es_host])

# Create index
index = 'events'

es_dsl.Index(index).delete(ignore=404) # for testing
es_dsl.Index(index)\
    .settings(number_of_shards=1)\
    .create()

# Create and save mapping to index
date_format = 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss.SSSSSS'
followups = es_dsl.Nested()\
    .field('date', 'date', format=date_format)
es_dsl.Mapping('initial')\
    .field('date', 'date', format=date_format)\
    .field('followups', followups)\
    .save(index)
