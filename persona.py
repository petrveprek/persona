#!python3
"""persona"""

import sys
import time
from collections import deque
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin

PERSONA = 'geek'
PERSONAS = \
{
    'geek': 
    {
        'seedUrls': ['https://github.com/petrveprek/persona'],
        'whiteList': None,
        'blackList': None,
    }
}

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    link = urljoin(self.baseUrl, value)
                    self.links.append(link)
    def get_links(self, url):
        self.baseUrl = url
        self.links = []
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode('utf-8')
            self.feed(htmlString)
        return self.links

def crawl(seedUrls, maxVisits = None, direction = None):
    urlsToVisit = deque(seedUrls)
    urlsVisited = set()
    if maxVisits == None:
        maxVisits = 10
    if direction == None:
        direction = 'breath-first'
    parser = LinkParser()
    while urlsToVisit and len(urlsVisited) < maxVisits:
        url = urlsToVisit.popleft()
        links = parser.get_links(url)
        urlsVisited.add(url)
        for link in links:
            if link not in urlsVisited and link not in urlsToVisit:
                if direction == 'depth-first':
                    urlsToVisit.appendleft(link) # depth first
                else:
                    urlsToVisit.append(link) # breath first
        print("{} / {} {} {}x".format(len(urlsVisited), len(urlsToVisit), url, len(links)))

def main():
    print("*** persona ***")
    print("Python {}".format(sys.version))
    print("Started at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    started_at = time.time()

    crawl(PERSONAS[PERSONA]['seedUrls'])

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
