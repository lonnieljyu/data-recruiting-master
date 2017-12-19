rpm --import http://debian.neo4j.org/neotechnology.gpg.key
cp /vagrant/provision/neo4j/neo4j.repo /etc/yum.repos.d/neo4j.repo

yum install -y neo4j
