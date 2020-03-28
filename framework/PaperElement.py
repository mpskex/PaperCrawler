# coding: utf-8

"""
General Paper Elements for SQL Databases

Fangrui Liu @ UBC
mpskex@github

Under GPLv3 License
"""

import re
import collections

class PaperElement():

    def __init__(self):
        """
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
        self.keyElement = collections.namedtuple('Attribute', ['type', 'value', 'is_prim'])
        self.keyMap = {
            'Title': 
                self.keyElement('text', 'NULL', True),
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
                self.keyElement('text', 'NULL', True), 
            'Year': 
                self.keyElement('int', 'NULL', True),
            '_STATUS': 
                self.keyElement('int', 'NULL', False),
            '_TIME': 
                self.keyElement('int', 'NULL', False)
            }
        self.primkeys = []
        self.clear()

        """
        keywords: ['attrs', 'type', 'primkeys', 'values']
        @ -     use space to concatenate
        ^ -     used for assign value
        # -     used for tighly glue those two
        """
        self.sepMap = {
            '@': ' ',
            '^': '=',
            '#': '',
        }
        self.table = 'PAPERS'
        self.mainkeys = ['attrs', 'attrsH', 'primkeys', 'table']
        self.keywords = ['attrs', 'attrsH', 'primkeys', 'table', 'types', 'values']
        self.pattern = re.compile(r'&[a-zA-Z]+(\B|(@|\^|#)[a-zA-Z]+)*')

    def clear(self):
        for key in self.keyMap.keys():
            setattr(self, key, self.keyMap[key].value)
            if self.keyMap[key].is_prim:
                self.primkeys.append(key)

    def concatenate(self, lists, content, sep):
        for idxm in range(len(content)):
            if 'H' in content[idxm] and idxm != len(content)-1:
                del(lists[idxm])
                del(sep[idxm])
        if len(sep) == 0 and type(lists[0]) is str:
            return lists
        else:
            assert len(lists) == len(sep) + 1
            result = lists[0]
            for idxs, s in enumerate(sep):
                result = list(map(lambda x, y: self.sepMap[s].join([x, y]), result, lists[idxs+1]))
            return result


    def translate(self, _str):
        _iter = self.pattern.finditer(_str)
        for i in _iter:
            matched = i.group(0)
            content = re.split(r'\W+', matched.split('&')[-1])
            content_woH = list(map(lambda x: x.split('H')[0], content))
            sep = re.findall(r'\W', matched.split('&')[-1])
            if content[0] not in self.mainkeys:
                raise KeyError("First Element" + content[0] + " in Pattern Must Be Attributes")
            else:
                if content_woH[0] == 'attrs':
                    selected = self.keyMap.keys()
                elif content_woH[0] == 'primkeys':
                    selected = self.primkeys
                elif content_woH[0] == 'table':
                    selected = self.table

            result = [selected]
            if len(content) > 0:
                for c in content_woH[1:]:
                    sub_result = []
                    assert c in self.keywords
                    if c == 'types':
                        sub_result = map(lambda x: self.keyMap[x].type, selected)
                    elif c == 'values':
                        def __assmeble__(input, selected):
                            _type = getattr(self.keyMap[selected], 'type')
                            if getattr(self, selected) == 'NULL' or _type in ['int', 'real']:
                                return str(input)
                            elif _type in ['text']:
                                return "'" + input.replace("'", "''") + "'"
                            else:
                                raise TypeError("Type `"+_type+"is not supported yet!")
                        sub_result = map(lambda x: __assmeble__(getattr(self, x), x), selected)
                    result.append(sub_result)
                result = self.concatenate(result, content, sep)
            _str = _str.replace(matched, ', '.join(result), 1)
        return _str


    def init_sql(self):
        create_sql = 'CREATE TABLE &table (&attrs@types, PRIMARY KEY (&primkeys))'
        return self.translate(create_sql)

    def insert_sql(self):
        insert_sql = 'INSERT INTO &table (&attrs) VALUES (&attrsH#values)'
        return self.translate(insert_sql)

if __name__ == '__main__':
    elem = PaperElement()
    elem.Title = 'ANY TITLE'
    print(elem.init_sql())
    print(elem.insert_sql())