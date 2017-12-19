wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install

mkdir -p /etc/redis  # -p for pseudo-idempotency
mkdir -p /var/redis/6379

cp /vagrant/provision/redis/redis_init_script /etc/init.d/redis_6379
cp /vagrant/provision/redis/redis.conf /etc/redis/6379.conf

sysctl vm.overcommit_memory=1
echo never > /sys/kernel/mm/transparent_hugepage/enabled

chkconfig --add redis_6379
chkconfig --level 345 redis_6379 on

service redis_6379 start
