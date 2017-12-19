import sqlite3
from data_interface import DataInterface
from datetime import datetime


class SQLiteInterface(DataInterface):
    '''
    it's so easy to write code when it's supposed to be bad.
    '''

    def __init__(self, batch_size=100):
        self.conn = sqlite3.connect('/vagrant/app/server/og_homework.db')
        self.c = self.conn.cursor()

    def log_initial(self, uuid, symbol, is_vowel):
        row = (uuid, symbol, is_vowel, "initial", str(datetime.utcnow()))
        self.c.execute('INSERT INTO api_events VALUES (?, ?, ?, ?, ?)', row)
        self.conn.commit()

    def log_followup(self, uuid):
        row = (uuid, None, None, "followup", str(datetime.utcnow()))
        self.c.execute('INSERT INTO api_events VALUES (?, ?, ?, ?, ?)', row)
        self.conn.commit()

    def simple_stats(self, symbol):
        self.c.execute(
            '''
            SELECT symbol, COUNT(*), max(date), min(date) from api_events where symbol=?
            ''',
            (symbol,)
        )
        keys = ('symbol', 'count', 'latest', 'earliest')
        vals = self.c.fetchone()
        return dict(zip(keys, vals))

    def count_followups(self, symbol):
        self.c.execute(
            '''
                select count(*)
                from (
                    select uuid
                    from api_events
                    where symbol=?
                ) ids
                inner join (
                    select *
                    from api_events
                    where url='followup'
                ) followups
                on ids.uuid = followups.uuid
            ''',
            (symbol,)
        )
        return self.c.fetchone()[0]

    def symbol_aggregates(self, symbol):
        stats = self.simple_stats(symbol)
        stats['followups'] = self.count_followups(symbol)
        return stats

    def count_ranged_followups(self, symbol, lower, upper):
        self.c.execute(
            '''
                select count(*)
                from (
                    select uuid
                    from api_events
                    where symbol=?
                    and ? < date
                    and date < ?
                ) ids
                inner join (
                    select *
                    from api_events
                    where url='followup'
                ) followups
                on ids.uuid = followups.uuid
            ''',
            (symbol, lower, upper)
        )
        return self.c.fetchone()[0]

    def range_aggregates(self, lower, upper):
        symbol_aggs = []
        for symbol in 'abcdefghijklkmnopqrstuvwxyz':
            self.c.execute(
                '''
                SELECT symbol, COUNT(*), max(date), min(date)
                from api_events
                where symbol=?
                and ? < date
                and date < ?
                ''',
                (symbol, lower, upper)
            )
            keys = ('symbol', 'count', 'latest', 'earliest')
            vals = self.c.fetchone()
            simple_ranged_stats = dict(zip(keys, vals))
            simple_ranged_stats['followups'] = self.count_ranged_followups(symbol, lower, upper)
            symbol_aggs.append(simple_ranged_stats)
        return symbol_aggs
