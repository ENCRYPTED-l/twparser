import sqlite3

d = sqlite3.connect('twitter.db', check_same_thread=False)
c = d.cursor()

try:
    c.execute('''CREATE TABLE content(UID INTEGER PRIMARY KEY, theme text, content longtext, link text, name text, id text, time int)''')
except:
    pass

