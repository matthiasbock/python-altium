#!/usr/bin/python

from struct import unpack

# Fills (filled rectangles) are binary-encoded records
# with at least one SubRecord
from BinarySubRecord import *

# parse
class SubRecord_Fill:
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

        # helper function to unpack little-endian 64-bit floats (doubles)
        def float64():
            global cursor
            (f,) = unpack('<d', data[cursor:cursor+8])
            cursor += 8
            return f

        # parse away...        
        self.X1 = signed32()
        self.Y1 = signed32()
        self.X2 = signed32()
        self.Y2 = signed32()

        self.Rotation = float64()

        # debug
        #print self.__dict__

        # 9 more bytes of unknown purpose
        
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
# A class for the fill elements tat can be used to draw a footprint
# in a footprint library (PcbLib)
#
class Fill:
    
    #
    # Parse properties from binary string
    # e.g. as read from a PcbLib file
    #
    def __init__(self, data):

        # Record Type = Fill
        assert ord(data[0]) == 6
        
        subrecord = SubRecord(data[1:])
        self.Properties = SubRecord_Fill(subrecord)
        
        # No bytes unaccounted for
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
    # http://www.w3schools.com/svg/svg_rect.asp
    #
    def __svg__(self):
        return '<rect x="'+str(self.Properties.X1/10000)+'" y="'+str(self.Properties.Y1/10000)+'" width="'+str((self.Properties.X2-self.Properties.X1)/10000)+'" height="'+str((self.Properties.Y2-self.Properties.Y1)/10000)+'" style="stroke:rgb(255,0,0);stroke-width:2" />'
