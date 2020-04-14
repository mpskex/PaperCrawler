# coding: utf-8

from .DataElement import DataElement


class CitationElement(DataElement):

    def __init__(self):
        super(DataElement, self).__init__()
        self.keyMap = {
            '_ID':
                self.keyElement('text', 'NULL', True),
            'ChildID':
                self.keyElement('text', 'NULL', False),
            'ParentID':
                self.keyElement('text', 'NULL', False),
            '_STATUS':
                self.keyElement('int', 'NULL', False),
            '_TIME':
                self.keyElement('int', 'NULL', False)
        }
        self.clear()

    def __initpara__(self):
        self.table = 'CITATIONS'