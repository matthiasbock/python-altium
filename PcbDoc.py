#!/usr/bin/python

from olefile import OleFileIO

from common import *
from BinarySubRecord import *

from json import dumps


#
# A PCB document (PcbDoc) stores the spatial arrangement of components
# as well as the conductor routes and shapes, which interconnect them 
#
class PcbDoc:
    
    #
    # Open and parse
    #
    def __init__(self, filename):
 
        self.OleFile = OleFileIO(filename)

        # Components
        self.Components = self.parseComponents(self.readStream("Components6/Data"))
        manifest = getU32(self.readStream("Components6/Header"))
        counted = len(self.Components)
        if manifest != counted:
            print "Warning: Header disagrees about component count, says there are "+str(manifest)+", but we counted "+str(counted)+"."


    #
    # Read a file from OLE container and return it's contents
    #
    def readStream(self, path):
        f = self.OleFile.openstream(path)
        c = True
        buffer = ""
        while c:
            c = f.read(1)
            if c:
                buffer += c
        f.close()
        return buffer


    #
    # Parse all components from list
    #
    def parseComponents(self, buffer):

        result = []
        cursor = 0

        while cursor < len(buffer):
            length = getU32(buffer[cursor:cursor+4])
            component = parseKeyValueString(buffer[cursor+4:cursor+length])
            #print dumps(component, sort_keys=True, indent=4)
            result.append(component)
            cursor += length+4

        return result
