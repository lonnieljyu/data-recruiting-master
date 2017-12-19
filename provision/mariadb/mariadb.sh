cp /vagrant/provision/mariadb/MariaDB.repo /etc/yum.repos.d/MariaDB.repo
yum update
yum install MariaDB-server MariaDB-client MariaDB-devel -y

service mysql start
chkconfig --level 35 mysql on
service mysql status

mysql -e "CREATE DATABASE og;"
mysql -e "CREATE USER 'og'@'localhost' IDENTIFIED BY 'og';"
mysql -e "GRANT ALL PRIVILEGES ON og.* TO 'og'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"
