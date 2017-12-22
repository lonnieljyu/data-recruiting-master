from random import randint, uniform
from flask import Flask, request
from elasticsearch_interface import ElasticSearchInterface
from sqlite_interface import SQLiteInterface
from data_interface import NullInterface
# from bradsinterface import BradsInterface

app = Flask(__name__)
# data_interface = ElasticSearchInterface()
data_interface = SQLiteInterface()
# data_interface = NullInterface()
# data_interface = BradsInterface()  # not tracked but this one was awesome, trust me.


@app.route("/initial", methods=["POST"])
def request_vowel_model():
    uuid = request.args.get('uuid')
    symbol = request.args.get('symbol')
    is_vowel = noisy_vowel_guess(symbol)
    data_interface.log_initial(uuid, symbol, is_vowel)
    return is_vowel


def noisy_vowel_guess(symbol):
    is_vowel = (symbol in 'aeiou') or (symbol == 'y' and randint(0, 1))
    if uniform(0, 1) < 0.1:
        return str(not is_vowel)
    else:
        return str(is_vowel)


@app.route("/followup", methods=["POST"])
def hooray():
    uuid = request.args.get('uuid')
    data_interface.log_followup(uuid)
    return 'hooray'


@app.route('/dashboard/symbol/<symbol>', methods=['GET'])
def symbol_agg(symbol):
    return str(data_interface.symbol_aggregates(symbol))


@app.route('/dashboard/range/<lower>/<upper>')
def range_agg(lower, upper):
    '''
    lower and upper should both have format "YYYY-MM-DD",  compatible with
    datetime.strptime(*, '%Y-%m-%d')
    Sub-day granularity to be provided in a future update.
    '''
    return str(data_interface.range_aggregates(lower, upper))
