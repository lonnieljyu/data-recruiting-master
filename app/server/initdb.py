import sqlite3


conn = sqlite3.connect('/vagrant/app/server/og_homework.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE api_events
    (uuid text, symbol text, is_vowel int, url text, date text)''')
