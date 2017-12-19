sudo yum install -y patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel

# sudo -u vagrant -H bash << EOF

git clone git://github.com/yyuu/pyenv.git ~/.pyenv

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

cat /vagrant/provision/python/pyenv.rc >> ~/.bashrc

# EOF
