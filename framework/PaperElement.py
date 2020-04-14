# coding: utf-8

"""
General Paper Elements for SQL Databases

Fangrui Liu @ UBC
mpskex@github

Under GPLv3 License
"""

from .DataElement import DataElement

class PaperElement(DataElement):
    """
    Paper Element
    """
    def __init__(self):
        """
        'id':           Identifier of the record
        'Title':        Title of the paper
        'Authors':      Authors of the paper, depends on the website's setting 
                        TODO:   Double checking the authors with different sources
        'Abstract':     Abstract
        'DOI':          DOI URL, parsed using the prefix `doi.org`
        'URL':          Alternate URL for the paper
        'PDF':          TODO:   Download the avaliable PDF from arXiv or open access
        'CJName':       Conference or Journal name
        'Year':         Year of publish
        '_STATUS':      Status of current record:   0 - FULL [1-5] Different Stage
                        0   FULL Record
                        1   Maintenance Scheduled: Update required
                        2   without PDF
                        3   Adding Abstract/Keywords and Double-checked Authors (with arXiv)
                        4   Adding DOI and Alternate URL
                        5   Title & CJName & Year Only
        '_TIME':        Timestamp of the snapshot
        """
        super(PaperElement, self).__init__()
        self.keyMap = {
            '_ID':
                self.keyElement('text', 'NULL', True),
            'Title': 
                self.keyElement('text', 'NULL', False),
            'Authors': 
                self.keyElement('text', 'NULL', False),
            'Abstract': 
                self.keyElement('text', 'NULL', False),
            'Keywords':
                self.keyElement('text', 'NULL', False),
            'DOI': 
                self.keyElement('text', 'NULL', False), 
            'URL': 
                self.keyElement('text', 'NULL', False), 
            'PDF': 
                self.keyElement('text', 'NULL', False), 
            'CJName': 
                self.keyElement('text', 'NULL', False),
            'Year': 
                self.keyElement('int', 'NULL', False),
            '_STATUS': 
                self.keyElement('int', 'NULL', False),
            '_TIME': 
                self.keyElement('int', 'NULL', False)
            }
        self.clear()

    def __initpara__(self):
        self.table = 'PAPERS'


    def init_sql(self):
        create_sql = 'CREATE TABLE IF NOT EXISTS &table (&attrs@types, PRIMARY KEY (&primkeys))'
        return self.translate(create_sql)


    def insert_sql(self):
        insert_sql = 'REPLACE INTO &table (&attrs) VALUES (&attrsH#values)'
        return self.translate(insert_sql)



if __name__ == '__main__':
    elem = PaperElement()
    elem.Title = 'ANY TITLE'
    print(elem.init_sql())
    print(elem.insert_sql())