#!/usr/bin/python

class PCBLibrary:

    def __init__(self):
        # nop
        self.components = []

    def append(self, c):
        if not c in self.components:
            self.components.append(c)

    def savePcbLib(self, filename):
        # create OLE archive
        f = open(filename,'w')
        f.write('test')
        f.close

