#!python3
"""persona"""

import sys
import time
from html.parser import HTMLParser
from urllib.request import urlopen

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            print("Tag 'a'")
            for (key, value) in attrs:
                if key == 'href':
                    print("Attribute 'href' {}".format(value))
    def get_links(self, url):
        self.baseUrl = url
        print("Request: {}".format(url))
        response = urlopen(url)
        print("Response: {}".format(response))
        print("Header: {}.".format(response.getheader('Content-Type')))
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode('utf-8')
            self.feed(htmlString)

def main():
    print("*** persona ***")
    print("Python {}".format(sys.version))
    print("Started at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    started_at = time.time()

    parser = LinkParser()
    parser.get_links('https://github.com/petrveprek/persona')

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
