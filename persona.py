#!python3
"""persona"""

import html.parser
import sys
import time
import urllib.request
from collections import deque
from random import randint
from urllib.parse import urljoin
from urllib.request import urlopen

PERSONA = 'persona'
PERSONAS = {
    'geek': {
        'browse': {
            'seeds': [
                'http://www.wired.com/',
                'http://www.engadget.com/',
                'http://www.gizmodo.co.uk/',
                'http://www.ubergizmo.com/',
                'http://techcrunch.com/'
            ],
            'blacks': [
                'entertainment',
                'fashion',
                'politics',
                'sport'
            ]
        }
    },
    'persona': {
        'browse': {
            'seeds': [
                'http://github.com/petrveprek/persona'
            ]
        },
        'search': {
            'queries': [
                'http://search.yahoo.com/search?p={}',
                'http://www.google.com/search?q={}'
            ],
            'terms': [
                'github',
                'persona'
            ]
        }
    }
}

class HtmlParser(html.parser.HTMLParser):
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
        headers = {'User-Agent': 'Self'}
        request = urllib.request.Request(url, headers=headers)
        response = urlopen(request)
        if 'text/html' in response.getheader('Content-Type'):
            character_set = response.headers.get_content_charset()
            htmlBytes = response.read()
            htmlString = htmlBytes.decode(character_set)
            self.feed(htmlString)
            text = htmlString
        return text, self.links

def browse(persona, maxVisits = None, direction = None):
    seedUrls = persona.get('browse', {}).get('seeds', [])
    whiteList = persona.get('browse', {}).get('whites', [])
    blackList = persona.get('browse', {}).get('blacks', [])
    if maxVisits == None:
        maxVisits = 10
    if direction not in ['breath-first', 'depth-first']:
        direction = 'random-walk'
    print("browse: {} {}x max {} {}x seeds {}x mandatory {}x forbidden".format(
          PERSONA, maxVisits, direction, len(seedUrls), len(whiteList), len(blackList)))
    urlsToVisit = deque(seedUrls)
    urlsVisited = set()
    parser = HtmlParser()
    while urlsToVisit and len(urlsVisited) < maxVisits:
        url = urlsToVisit.popleft()
        text, links = parser.get_text_links(url)
        urlsVisited.add(url)
        if not any(black.lower() in text.lower() for black in blackList):
            for link in links:
                if link not in urlsVisited and link not in urlsToVisit:
                    if direction == 'breath-first':
                        urlsToVisit.append(link) # breath first
                    elif direction == 'depth-first':
                        urlsToVisit.appendleft(link) # depth first
                    else:
                        urlsToVisit.insert(randint(0, len(urlsToVisit)), link) # random walk
        print("{} / {} {} {}x".format(len(urlsVisited), len(urlsToVisit), url, len(links)))

def search(persona):
    queries = persona.get('search', {}).get('queries', [])
    terms = persona.get('search', {}).get('terms', [])
    print("search: {} {}x queries {}x terms".format(
          PERSONA, len(queries), len(terms)))
    searches = 0
    parser = HtmlParser()
    for query in queries:
        for term in terms:
            url = query.format(term)
            text, links = parser.get_text_links(url)
            searches += 1
            print("{} / {} {}".format(searches, len(queries) * len(terms), url))

def main():
    print("*** persona ***")
    print("Python {}".format(sys.version))
    print("Started at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    started_at = time.time()

    browse(PERSONAS[PERSONA])
    search(PERSONAS[PERSONA])

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
