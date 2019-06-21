from flask import Flask
from flask import render_template, request
app = Flask(__name__)
from dbs import *
from test import selection



import requests
from bs4 import BeautifulSoup as bs



@app.route('/')
def index():
    return render_template('index.html', data=cont, link=link, time=time, id=id)

@app.route('/', methods=['POST'])
def my_form_post():
    global req
    req = request.form['text']
    parse_it(req)
    selection()
    return render_template('index.html', data=cont, link=link, time=time, id=id)

def parse_it(req):
    l = req.split()
    sl = '%20'.join(l)
    headers = {"accept": "*/*",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    parse_url = 'https://twitter.com/search?q=' + sl + '&src=typd&lang=en'
    # parse_url = 'https://twitter.com/search?q=информационная%20безопасность&src=typd&lang=en'
    ses = requests.Session()
    request = ses.get(parse_url, headers=headers)
    if request.status_code == 200:
        content = bs(request.content, 'html.parser')
        twit = content.findAll("div", attrs={"class": "tweet"})
        for twits in twit:
            txt = twits.find("p", attrs={"class": "TweetTextSize js-tweet-text tweet-text"}).text
            name = twits.find("span", attrs={"class": "FullNameGroup"}).text
            username = twits.find("span", attrs={"class": "username u-dir u-textTruncate"}).text
            postime = twits.find("a", attrs={"class": "tweet-timestamp js-permalink js-nav js-tooltip"})["title"]
            try:
                url = twits.find("span", attrs={"class": "js-display-url"}).text
                fullurl = str("http://" + url)
            except:
                fullurl = "None"

            data = []
            data.append(('is', txt, fullurl, name, username, postime))
            c.executemany("INSERT INTO content(theme, content, link, name, id, time) VALUES (?, ?, ?, ?, ?, ?)", data)
            d.commit()

    else:
        print("ERR")
    deduplicate()


def deduplicate():
    c.execute('DELETE FROM content WHERE rowid NOT IN (SELECT min(rowid) FROM content GROUP BY content)')
    d.commit()



