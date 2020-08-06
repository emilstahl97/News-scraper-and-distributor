import requests
from bs4 import BeautifulSoup
import redis

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
            r.set(link.text, link)

