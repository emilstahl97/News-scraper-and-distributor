import re

import redis
import requests
from bs4 import BeautifulSoup
from fbchat import Client
from fbchat.models import *

import urlmaker
from login import login_with_session


class Scraper:
    def __init__(self, keywords):
        url = "https://news.ycombinator.com"
        self.markup = requests.get(url).text
        self.keywords = keywords



    def parser(self):
        soup = BeautifulSoup(self.markup, "html.parser")
        links = soup.findAll("a", {"class":  "storylink"})
        self.saved_links = []
        for link in links:
            for keyword in self.keywords:
                if keyword in link.text:
                    self.saved_links.append(link)
    

    def store(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        for link in self.saved_links:
            r.set(link.text, str(link))

    

    def send(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        numberOfArticles = len(r.keys())
        if numberOfArticles != 0:
            client = login_with_session()

            greeting = f"Hi, Emil. Here is {numberOfArticles} news article that you might found interesting"
            client.send(Message(text=greeting), thread_id=client.uid, thread_type=ThreadType.USER)

            for k in r.keys():
                url = re.findall(urlmaker.URL_REGEX, str(r.get(k)))
                message = str(k)[2:-1] + "\n\n" + ' '.join(map(str, url))
                client.send(Message(text=message), thread_id=client.uid, thread_type=ThreadType.USER)
            
            r.flushdb()
        

s = Scraper(['is'])
s.parser()
s.store()
s.send()
