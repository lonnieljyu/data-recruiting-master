cp /vagrant/provision/elasticsearch/elasticsearch.repo /etc/yum.repos.d/elasticsearch.repo
yum install -y elasticsearch

chkconfig --add elasticsearch
service elasticsearch start
