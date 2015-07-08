#!/usr/bin/python

from struct import unpack

# Arcs are binary-encoded records
# and consist of one SubRecord
from BinarySubRecord import *

# parse an arc
class SubRecord_Arc:
    def __init__(self, subrecord):
        
        # get data from subrecord
        data = subrecord.content

        # first 13 bytes are of unknown purpose
        self.common = SubRecord_Common(data)
        global cursor
        cursor = self.common.length #13

        # helper function to unpack signed 32-bit integers
        def signed32():
            global cursor
            (i,) = unpack('<i',data[cursor:cursor+4])
            cursor += 4
            return i        

        # parse away...        
        self.CenterX = signed32()
        self.CenterY = signed32()
        self.Radius  = signed32()
        
        # 16 bytes of unknown purpose
        cursor += 16
        
        self.Width = signed32()

        # debug
        print self.__dict__

        # 11 more bytes of unknown purpose
        
        #
        # Arc properties yet unaccounted for:
        #
        # Start Angle
        # End Angle
        # Layer:                 multiple choice
        # Net:                   multiple choice
        # Locked:                true/false
        # Keepout:               true/false
        # Solder Mask Expansion: multiple choice
        # Paste Mask Expansion:  multiple choide
        #

#
# A class for the line = tracks that can be used to draw a footprint
# in a footprint library (PcbLib)
#
class Arc:
    #
    # Parse properties from binary string
    # e.g. as read from a PcbLib file
    #
    def __init__(self, data):

        # Record Type = Arc
        assert ord(data[0]) == 1
        
        subrecord = SubRecord(data[1:])
        self.Properties = SubRecord_Arc(subrecord)
        
        # No bytes unaccounted for.
        self.length = 1+subrecord.length

    #
    # Export pin properties as binary string
    # e.g. for writing it into a PcbLib file
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        