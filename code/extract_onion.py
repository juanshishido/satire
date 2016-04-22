'''
    python extract_onion.py [PATH] [START_INDEX] [NUM_ARTICLES]
    sample usage: python extract_onion.py oniondata 51760 1000
    This will create a folder callex oniondata and fill it with 1000 articles indexed from 51760 (and counting down)
    Note that not all article ids have a valid article, so the number of scraped articles may be fewer than 1000.
'''

from html.parser import HTMLParser
import urllib.request as urllib2
from bs4 import BeautifulSoup, Comment
import re
import os
import sys
import time

def onion_url(id):
    return ('http://www.theonion.com/r/' + str(id))

def download_and_parse_article(id):
    try:
        html_content = urllib2.urlopen(onion_url(id)).read()
        soup = BeautifulSoup(html_content, "html.parser")
        article_content = soup.find_all('div',attrs={"class" : "content-text"})[0]
        article_title = soup.find_all('header',attrs={"class" : "content-header"})[0]
        print("Succesffully extracted article id: " + str(id) + " with title: " + article_title.text.rstrip().lstrip())
        return (article_title.text.rstrip().lstrip(), article_content.text.rstrip().lstrip())
    except:
        print("Failed on id: " + str(id))
        return ('','')

path = sys.argv[1]
starting_id = int(sys.argv[2])
num_articles = int(sys.argv[3])
os.system("mkdir -p " + path)

for i in range(0,num_articles):
    id = starting_id - i
    (title, content) = download_and_parse_article(id)
    if title != '' and content != '':
        file = open(path + '/onion-' + str(id), 'w')
        file.write(title + '\n\n' + content + '\n')
        file.close()
    time.sleep(3)