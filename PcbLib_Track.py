#!/usr/bin/python

from struct import unpack

# Tracks are binary-encoded records
# and consist of one SubRecord
from BinarySubRecord import *

# parse a track
class SubRecord_Track:
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
        self.X1 = signed32()
        self.Y1 = signed32()
        self.X2 = signed32()
        self.Y2 = signed32()

        self.Width = signed32()

        # debug
        #print self.__dict__

        # 12 more bytes of unknown purpose
        
        #
        # Properties yet unaccounted for:
        #
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
class Track:
    
    #
    # Parse properties from binary string
    # e.g. as read from a PcbLib file
    #
    def __init__(self, data):

        # Record Type = Track
        assert ord(data[0]) == 4
        
        subrecord = SubRecord(data[1:])
        self.Properties = SubRecord_Track(subrecord)
        
        # No bytes unaccounted for.
        self.length = 1+subrecord.length

    #
    # Export pin properties as binary string
    # e.g. for writing it into a PcbLib file
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result

    #
    # Interface for Scalable Vector Graphics output
    # http://www.w3schools.com/svg/svg_line.asp
    #        
    def __svg__(self):
        return '<line x1="'+str(self.Properties.X1/10000)+'" y1="'+str(self.Properties.Y1/10000)+'" x2="'+str(self.Properties.X2/10000)+'" y2="'+str(self.Properties.Y2/10000)+'" style="stroke:rgb(255,0,0);stroke-width:2" />'

        