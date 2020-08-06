import requests
from bs4 import BeautifulSoup
import redis
from fbchat import Client
from fbchat.models import *
from login import login_with_session
import re
import urlmaker


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
            #print(link.text)
            print("")
            #string = str(link)
            #split = string.split('"')[0]
            #print(split)
            string = str(link)
            print(re.findall(urlmaker.URL_REGEX,string))
            r.set(link.text, str(link))

    

    def send(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        links = [r.get(k) for k in r.keys()]
        print(links)
        
        client = login_with_session()
        for link in links:
            client.send(Message(text=link), thread_id=client.uid, thread_type=ThreadType.USER)
        
        r.flushdb()
        



s = Scraper(['is'])
s.parser()
s.store()
#print(s.saved_links)
#s.send()