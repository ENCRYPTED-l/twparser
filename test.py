from dbs import *

def selection():
    global cont
    c.execute("SELECT content FROM content")
    cont = c.fetchall()
    cont = [x[0] for x in cont]
    d.commit()

    c.execute("SELECT link FROM content")
    global link
    link = c.fetchall()
    link = [x[0] for x in link]
    d.commit()

    c.execute("SELECT id FROM content")
    global id
    id = c.fetchall()
    id = [x[0] for x in id]
    d.commit()

    c.execute("SELECT time FROM content")
    global time
    time = c.fetchall()
    time = [x[0] for x in time]
    d.commit()