#!/usr/bin/python

from olefile import OleFileIO

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
        self.TOC = TOC( self.readStream("Library/ComponentParamsTOC/Data") )

        # Parse all the footprints
        self.Footprints = []
        for footprint in self.TOC.footprints:
            print footprint
            self.Footprints.append(
                    Footprint(self.readStream(footprint["Name"]+"/Data"))
                )

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
