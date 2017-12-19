eval "$(pyenv init -)";

echo "CURRENT PYTHON VERSION"
pyenv versions
pyenv install 3.6.1

echo "SETTING NEW PYTHON VERSION"
pyenv shell 3.6.1
pyenv global 3.6.1
pyenv versions
pyenv rehash
