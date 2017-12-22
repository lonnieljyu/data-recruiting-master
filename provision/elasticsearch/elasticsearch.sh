cp /vagrant/provision/elasticsearch/elasticsearch.repo /etc/yum.repos.d/elasticsearch.repo
yum install -y elasticsearch

export ES_server='localhost'
export ES_port='9200'

chkconfig --add elasticsearch
service elasticsearch start
