#coding: utf-8

import os
from bs4 import BeautifulSoup
import requests
import sqlite3
from .PaperElement import PaperElement


"""
General Paper Crawler

Fangrui Liu @ UBC
mpskex@github

Under GPLv3 License
"""

class PaperCrawler():
    def __init__(self, name, log_level=1):
        """
        url:        target web url
        name:       name for the associate files
        log_level:  1 - CRITICAL => 5 - VERBOSE
        """
        self.name = name
        self.log_level = log_level
        self.paperElement = PaperElement()

        if os.path.isfile(self.name+'.db'):
            self.conn = sqlite3.connect(self.name+'.db')
            if self.log_level >= 3:
                print('[*]\tSuccessfully Opened Database: ', self.name + '.db')
        else:
            self.conn = sqlite3.connect(self.name+'.db')
            self.initialize()

    def initialize(self):
        # Create table
        sql = self.paperElement.init_sql()
        if self.log_level >= 5:
            print('[*]\t Executing SQL: ', sql)
        self.conn.execute(sql) 
        self.paperElement.clear()
        self.conn.commit()
        if self.log_level >= 3:
            print('[*]\tSuccessfully Initialized Database: ', self.name + '.db')
        

    def get(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            if self.log_level >= 3:
                print('[*]\tSuccessfully Fetched URL: ', url)
            return r
        elif r.status_code == 404:
            print('[!]\tURL Doesn\'t Exist!')
            raise FileNotFoundError('[!]\tURL `'+url+'` Doesn\'t Exist!')
        else:
            print('[!]\tURL Returned Status Code: \n', r.status_code)
            raise ValueError('No valid webpage to fetch')

    def dump(self, text, name='Dumped'):
        with open(name+'.html', 'w') as f:
            f.write(text)
            if self.log_level >= 3:
                print('[*]\tSuccessfully Dumped to file: ', self.name+'.html')
            f.close()

    def iteration(self, article, cjname, year=2020):
        #   Get Title
        cite = article.find('cite', class_='data', itemprop='headline')
        title = cite.find('span', class_='title', itemprop='name').contents[0]
        authors = cite.find_all('span', itemprop='author')
        authors = ', '.join(map(lambda a: a.find('span', itemprop='name').contents[0], authors))
        if self.log_level >=2:
            print("[*]\tAdding %s Authors: %s at %s in year %i" % (title, authors, cjname, int(year)))
        self.paperElement.Title = title
        self.paperElement.Authors = authors
        self.paperElement.CJName = cjname
        self.paperElement.Year = int(year)

        nav = article.find('nav', class_='publ')
        for url in nav.find_all('a', itemprop="url"):
            if 'doi.org' in url:
                if self.log_level >= 4:
                    print('[*]\tAdding Attribute DOI=`'+url['href']+'` to Title `'+title+'`')
                self.paperElement.DOI = url['href']
            elif 'dblp.org' not in url:
                if self.log_level >= 4:
                    print('[*]\tAdding Attribute URL=`'+url['href']+'` to Title `'+title+'`')
                self.paperElement.URL = url['href']
        self.conn.execute(self.paperElement.insert_sql())

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
    p = PaperCrawler('CVPR2019', log_level=5)
    p.update('https://dblp.org/db/conf/cvpr/cvpr2019.html')