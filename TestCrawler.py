# coding: utf-8
import sys
sys.path.append('..')
from bs4 import BeautifulSoup
from framework.CVFCrawler import CVFCrawler
from framework.PaperElement import PaperElement



class Crawler(CVFCrawler):
    def __init__(self, years, name, conferences, dataElement, log_level=1):
        super(Crawler, self).__init__(name, dataElement, log_level)
        self.years = years
        supported = ['CVPR', 'ECCV', 'ICCV', 'WACV']
        self.conferences = []
        for conf in conferences:
            if conf in supported:
                self.conferences.append(conf)
        self.base_url = 'http://openaccess.thecvf.com/$conf$year.py'


    def update_all(self):
        for conf in self.conferences:
            for year in self.years:
                self.dataElement.clear()
                url = self.base_url.replace('$year', str(year)).replace('$conf', conf)
                self.update(url)


if __name__ == '__main__':
    c = Crawler(range(2010, 2020), 'PaperDB', ['ECCV', 'CVPR', 'ICCV', 'WACV'], PaperElement(), log_level=4)
    c.update_all()
