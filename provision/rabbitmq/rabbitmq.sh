wget https://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
yum install -y erlang

wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.5.3/rabbitmq-server-3.5.3-1.noarch.rpm
rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
yum install -y rabbitmq-server-3.5.3-1.noarch.rpm

chkconfig rabbitmq-server on
service rabbitmq-server start

rabbitmq-plugins enable rabbitmq_management
