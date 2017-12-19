eval "$(pyenv init -)";

echo "CURRENT PYTHON VERSION"
pyenv versions
pyenv install 2.7.13

echo "SETTING NEW PYTHON VERSION"
pyenv shell 2.7.13
pyenv global 2.7.13
pyenv versions
pyenv rehash
