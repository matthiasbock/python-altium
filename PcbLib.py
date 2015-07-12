#!/usr/bin/python

from olefile import OleFileIO

from common import getU32
from BinarySubRecord import *
from PcbLib_TOC import TOC
from PcbLib_Footprint import Footprint

#
# A PCB library (PcbLib) stores PCB components' footprints 
#
class PcbLib:
    
    #
    # Open and parse PcbLib file
    #
    def __init__(self, filename):

        self.OleFile = OleFileIO(filename)

        # TOC = Table Of Contents
        # A list of the footprints contained in this PcbLib can be found here:
        #self.TOC = TOC( self.readStream("Library/ComponentParamsTOC/Data") )
        # not always present

        #
        # Parse library parameters
        # Library/Data contains a list of parameters (string: "|"-separated key-value pairs)
        # followed by the count and names of footprints in the library
        #
        buffer = self.readStream("Library/Data")

        # Properties
        print "Library properties:"
        length = getU32(buffer)
        header = buffer[4:4+length-1] # also cut away the string's null terminator
        properties = header.strip('|').split('|')
        self.Properties = {}
        for prop in properties:
            x = prop.split('=')
            key = x[0]
            if len(x) > 1:
                value = x[1]
            else:
                value = ""
            self.Properties[key] = value
        print self.Properties
        
        # Footprint list
        cursor = 4+length
        count = getU32(buffer[cursor:])
        cursor += 4
        print "Footprints in library: "+str(count)
        footprints = []
        for i in range(count):
            subrecord = SubRecord(buffer[cursor:])
            name = SubRecord_String(subrecord)
            print " * "+name
            footprints.append(name)
            cursor += subrecord.length

        # Parse all the footprints
        self.Footprints = []
        for footprint in footprints:
            print "Parsing "+footprint+" ..."
            self.Footprints.append(
                    Footprint(self.readStream(footprint+"/Data"))
                )
                
        # Create a dictionary of footprints to access them by name
        self.FootprintsByName = {}
        for footprint in self.Footprints:
            self.FootprintsByName[footprint.name] = footprint
        #print self.FootprintsByName

    #
    # Read file from OLE container and return it's contents
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
