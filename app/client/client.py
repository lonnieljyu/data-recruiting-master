from requests import post, get
from uuid import uuid4
from itertools import cycle
from random import randint, uniform


BASE = "http://localhost:"
PORT = "5000"


def initial_request(uuid, symbol):
    data = {'uuid': uuid, 'symbol': symbol}
    resp = post(
        url=BASE + PORT + '/initial',
        params=data
    )
    return resp


def is_vowel(symbol):
    return (symbol in 'aeiou') or (symbol == 'y' and randint(0, 1))


def success(symbol, response):
    response_bool = response.text == "True"
    return is_vowel(symbol) == response_bool


def second_request(uuid):
    post(
        url=BASE + PORT + '/followup',
        params={'uuid': uuid}
    )
    return 0


def main():
    source_file = open('/vagrant/app/client/sherlock.txt')
    symbol_source = cycle([x.lower() for x in source_file.read() if x.isalpha()])
    response_strength = {True: 0.1, False: 0.2}

    while True:
        uuid = str(uuid4())
        symbol = next(symbol_source)

        response = initial_request(uuid, symbol)

        engage = (
            success(symbol, response) and
            uniform(0, 1) < response_strength[is_vowel(symbol)]
        )
        if engage:
            second_request(uuid)


if __name__ == '__main__':
    main()
