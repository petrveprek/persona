#!python3
"""persona"""

import sys
import time
from collections import deque
from html.parser import HTMLParser
from random import randint
from urllib.parse import urljoin
from urllib.request import urlopen

PERSONA = 'persona'
PERSONAS = {
    'geek': {
        'spider': {
            'seedUrls': ['http://www.wired.com/', 'http://www.engadget.com/', 'http://www.gizmodo.co.uk/', 'http://www.ubergizmo.com/', 'http://techcrunch.com/'],
            'blackList': ['entertainment', 'fashion', 'politics', 'sport']}},
    'persona': {
        'spider': {
            'seedUrls': ['https://github.com/petrveprek/persona']}}}

class HtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    link = urljoin(self.baseUrl, value)
                    self.links.append(link)
    def get_text_links(self, url):
        self.baseUrl = url
        self.links = []
        text = ""
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode('utf-8')
            self.feed(htmlString)
            text = htmlString
        return text, self.links

def crawl(persona, maxVisits = None, direction = None):
    seedUrls = []
    whiteList = []
    blackList = []
    if 'spider' in persona:
        if 'seedUrls' in persona['spider']:
            seedUrls = persona['spider']['seedUrls']
        if 'whiteList' in persona['spider']:
            whiteList = persona['spider']['whiteList']
        if 'blackList' in persona['spider']:
            blackList = persona['spider']['blackList']
    print("{} {}x URLs {}x mandatory {}x forbidden".format(PERSONA, len(seedUrls), len(whiteList), len(blackList)))
    urlsToVisit = deque(seedUrls)
    urlsVisited = set()
    if maxVisits == None:
        maxVisits = 10
    if direction == None:
        direction = 'breath-first'
    if direction not in ['breath-first', 'depth-first']:
        direction = 'random-walk'
    parser = HtmlParser()
    while urlsToVisit and len(urlsVisited) < maxVisits:
        url = urlsToVisit.popleft()
        text, links = parser.get_text_links(url)
        urlsVisited.add(url)
        if blackList == None or not any(black.lower() in text.lower() for black in blackList):
            for link in links:
                if link not in urlsVisited and link not in urlsToVisit:
                    if direction == 'breath-first':
                        urlsToVisit.append(link) # breath first
                    elif direction == 'depth-first':
                        urlsToVisit.appendleft(link) # depth first
                    else:
                        urlsToVisit.insert(randint(0, len(urlsToVisit)), link) # random walk
        print("{} / {} {} {}x".format(len(urlsVisited), len(urlsToVisit), url, len(links)))

def main():
    print("*** persona ***")
    print("Python {}".format(sys.version))
    print("Started at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    started_at = time.time()

    crawl(PERSONAS[PERSONA])

    print("Completed at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    elapsed = time.time() - started_at
    seconds = round(elapsed)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    print("Elapsed {:d}w {:d}d {:d}h {:d}m {:d}s ({:,.3f}s)".format(weeks, days, hours, minutes, seconds, elapsed))

if __name__ == '__main__':
    main()
