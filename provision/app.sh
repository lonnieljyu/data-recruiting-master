echo "export FLASK_APP=/vagrant/app/server/app.py" >> /home/vagrant/.bashrc
pip install -r /vagrant/requirements.txt

rm -f /vagrant/app/server/og_*.db
python /vagrant/app/server/initdb.py
python /vagrant/app/server/init_elasticsearch_index.py
