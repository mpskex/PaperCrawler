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
from .DataElement import DataElement

class DataCrawler():
    def __init__(self, name, dataElement, log_level=1):
        """
        url:        target web url
        name:       name for the associate files
        log_level:  1 - CRITICAL => 5 - VERBOSE
        """
        self.name = name
        self.log_level = log_level
        assert isinstance(dataElement, DataElement)
        self.dataElement = dataElement

        if os.path.isfile(self.name+'.db'):
            self.conn = sqlite3.connect(self.name+'.db')
            if self.log_level >= 3:
                print('[*]\tSuccessfully Opened Database: ', self.name + '.db')
        else:
            self.conn = sqlite3.connect(self.name+'.db')
            self.initialize()

    def initialize(self):
        # Create table
        sql = self.dataElement.init_sql()
        if self.log_level >= 5:
            print('[*]\t Executing SQL: ', sql)
        self.conn.execute(sql)
        self.dataElement.clear()
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
            raise FileNotFoundError('URL `'+url+'` Doesn\'t Exist!')
        else:
            raise ValueError('URL Returned Status Code: '+str(r.status_code))


    def dump(self, text, name='Dumped'):
        with open(name+'.html', 'w') as f:
            f.write(text)
            if self.log_level >= 3:
                print('[*]\tSuccessfully Dumped to file: ', self.name+'.html')
            f.close()

    def get_soup(self, url):
        html_str = self.get(url).text
        if self.log_level >= 4:
            print("[*]\tSuccessfully Parsed URL: `", url, "`")
        soup = BeautifulSoup(html_str, 'html.parser')
        if self.log_level >= 5:
            self.dump(soup.prettify())
        return soup

    def get_elements(self, url):
        soup = self.get_soup(url)
        # Parsing the webpage here
        raise NotImplementedError

    def iteration(self, element, *args, **kwargs):
        # Implement this to update the database
        raise NotImplementedError

    def update(self, url):
        try:
            elements = self.get_elements(url)
            for element in elements:
                try:
                    self.iteration(element)
                except FileNotFoundError as e:
                    print('[!]Error!:\t', e)
            self.conn.commit()
        except FileNotFoundError as e:
            print('[!]Error!:\t', e)

    def __add__(self, o):
        """
        Note: Addition of Data Crawler is sequential
        :param o:
        :return:
        """
        pass


