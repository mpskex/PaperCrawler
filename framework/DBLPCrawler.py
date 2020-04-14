#coding: utf-8

import os
from bs4 import BeautifulSoup
import requests
import sqlite3
from .PaperElement import PaperElement
import time
import hashlib


"""
General Paper Crawler

Fangrui Liu @ UBC
mpskex@github

Under GPLv3 License
"""
from .DataCrawler import DataCrawler
from .PaperElement import PaperElement

class DBLPCrawler(DataCrawler):
    """
    We Crawl DBLP for indexing papers by conference or journals
    This module only parse the result page, and we still need a guide for this Crawler
    """
    def __init__(self, name, dataElement, log_level=1):
        """
        url:        target web url
        name:       name for the associate files
        log_level:  1 - CRITICAL => 5 - VERBOSE
        """
        assert isinstance(dataElement, PaperElement)
        super(DBLPCrawler, self).__init__(name, dataElement, log_level)


    def iteration(self, article):
        #   Get Title
        cite = article.find('cite', class_='data', itemprop='headline')
        title = cite.find('span', class_='title', itemprop='name').contents[0]
        authors = cite.find_all('span', itemprop='author')
        authors = ', '.join(map(lambda a: a.find('span', itemprop='name').contents[0], authors))
        year = int(cite.find('meta', itemprop='datePublished').attrs['content'].contents[0])
        head = article

        if self.log_level >=2:
            print("[*]\tAdding %s Authors: %s at %s in year %i" % (title, authors, cjname, int(year)))
        self.dataElement.Title = title
        self.dataElement.Authors = authors
        self.dataElement.CJName = cjname
        self.dataElement.Year = int(year)
        #   Internal ID and status
        self.dataElement._ID = hashlib.sha256((title+authors+cjname).encode('utf-8')).hexdigest()
        self.dataElement._TIME = time.time()
        self.dataElement._STATUS = 5

        nav = article.find('nav', class_='publ')
        for url in nav.find_all('a', itemprop="url"):
            if 'doi.org' in url:
                if self.log_level >= 4:
                    print('[*]\tAdding Attribute DOI=`'+url['href']+'` to Title `'+title+'`')
                self.dataElement.DOI = url['href']
            elif 'dblp.org' not in url:
                if self.log_level >= 4:
                    print('[*]\tAdding Attribute URL=`'+url['href']+'` to Title `'+title+'`')
                self.dataElement.URL = url['href']
        self.conn.execute(self.dataElement.insert_sql())

    def update(self, url):
        r = self.get(url)
        html_str = r.text
        soup = BeautifulSoup(html_str, 'html.parser')
        if self.log_level >= 4:
            print("[*]\tSuccessfully Parsed URL: `", url, "`")
        if self.log_level >= 5:
            self.dump(soup.prettify())
        articles = soup.find_all('li', class_="entry inproceedings")
        for article in articles:
            self.iteration(article, self.name)
        self.conn.commit()



if __name__ == '__main__':
    p = DBLPCrawler('CVPR2019', log_level=5)
    p.update('https://dblp.org/db/conf/cvpr/cvpr2019.html')