#!/usr/bin/python

from common import getU32

#
# A PcbLib file contains a file "Library/ComponentParamsTOC/Data"
# which holds a list of the footprints in that library
#
class TOC:
    
    #
    # Parse Table Of Contents
    #
    def __init__(self, buffer):

        # first four bytes are total string length
        # last byte is 0x00
        assert getU32(buffer)+4 == len(buffer) 
        buffer = buffer[4:-1]
        
        entries = buffer.replace('\x0D\x0A','\n').strip().split('\n')
        self.footprints = []
        
        for entry in entries:
            properties = {}
            subentries = entry.split('|')
            for subentry in subentries:
                x = subentry.split('=')
                key = x[0]
                if len(x) > 1:
                    value = "".join(x[1:])
                else:
                    value = ""
                properties[key] = value
            self.footprints.append(properties)

        #print self.footprints
