#!/usr/bin/python

class PCBComponent:

    def __init__(self):
        # nop
        self.elements = []

    def append(self, e):
        if not e in self.elements:
            self.elements.append(e)

    def export(self, filename):
        # create OLE archive
        f = open(filename,'w')
        f.write('test')
        f.close

