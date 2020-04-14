# coding: utf-8

from .DataCrawler import DataCrawler
from .CitationElement import CitationElement

class CitationCrawler(DataCrawler):
    """
    This module will Crawl the citation and create the corresponding table
    """
    def __init__(self, name, log_level=1):
        super(CitationCrawler, self).__init__(self, name=name, dataElement=CitationElement, log_level=log_level)

    def iteration(self):
        pass

    def update(self):
        pass


