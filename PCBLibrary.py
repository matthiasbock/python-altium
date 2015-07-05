#!/usr/bin/python

class PCBLibrary:

    def __init__(self):
        # nop
        self.components = []

    def append(self, c):
        if not c in self.components:
            self.components.append(c)

    def exportPcbLib(self):
        ole = "begin PcbLib\n"
        for component in self.components:
            ole += component.exportPcbLib 
        return ole
