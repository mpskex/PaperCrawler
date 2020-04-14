#coding: utf-8


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

class CVFCrawler(DataCrawler):
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
        super(CVFCrawler, self).__init__(name, dataElement, log_level)


    def iteration(self, article):
        #   Get Title
        title = article.find('a')
        url = 'http://openaccess.thecvf.com/' + title.attrs['href']
        asoup = self.get_soup(url)
        authors = asoup.find('div', id='authors').find('b').contents[0].contents[0]
        abstract = ''.join(asoup.find('div', id='abstract').contents[0].split('\n'))
        head = asoup.find('title').contents[0].split(' ')
        cjname, year = head[0], int(head[1])

        if self.log_level >= 2:
            print("[*]\tAdding %s Authors: %s at %s in year %i" % (title.contents[0], authors, cjname, int(year)))
        self.dataElement.Title = title.contents[0]
        self.dataElement.Authors = authors
        self.dataElement.Abstract = abstract
        self.dataElement.CJName = cjname
        self.dataElement.Year = int(year)
        #   Internal ID and status
        self.dataElement._ID = hashlib.sha256((title.contents[0]+authors+cjname+str(year)).encode('utf-8')).hexdigest()
        self.dataElement._TIME = time.time()
        self.dataElement._STATUS = 5

        self.dataElement.URL = url
        self.conn.execute(self.dataElement.insert_sql())

    def get_elements(self, url):
        soup = self.get_soup(url)
        content = soup.find_all('div', id="content")[0]
        return content.find('dl').find_all('dt', class_='ptitle')


if __name__ == '__main__':
    p = CVFCrawler('CVPR2019', log_level=5)
    p.update('http://openaccess.thecvf.com/CVPR2019.py')