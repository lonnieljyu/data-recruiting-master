cp /vagrant/provision/mongodb/mongodb-org-3.4.repo /etc/yum.repos.d/mongodb-org-3.4.repo
yum install -y mongodb-org

chkconfig mongod on
service mongod start
