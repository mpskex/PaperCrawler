# coding: utf-8
import sys
sys.path.append('..')
from bs4 import BeautifulSoup
from framework.PaperCrawler import PaperCrawler
from framework.PaperElement import PaperElement

class CVPRCrawler(PaperCrawler):
    def __init__(self, years, name, log_level=1):
        super(CVPRCrawler, self).__init__(name, log_level)
        self.years = years
        self.base_url = 'https://dblp.org/db/conf/cvpr/cvpr$year.html'


    def update(self):
        for year in self.years:
            self.paperElement.clear()
            url = self.base_url.replace('$year', str(year))
            r = self.get(url)
            html_str = r.text
            soup = BeautifulSoup(html_str, 'html.parser')
            if self.log_level >= 4:
                print("[*]\tSuccessfully Parsed URL: `", url, "`")
            if self.log_level >= 5:
                self.dump(soup.prettify(), name='CVPR'+str(year))
            soup = soup.find('ul', class_='publ-list')
            articles = soup.find_all('li', class_="entry inproceedings")
            for article in articles:
                self.iteration(article, 'CVPR', year)
            self.conn.commit()


if __name__ == '__main__':
    c = CVPRCrawler(range(2010, 2020), 'CVPR', log_level=4)
    c.update()
