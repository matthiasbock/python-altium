#!/usr/bin/python

# https://docs.python.org/2/library/struct.html#format-characters
from struct import unpack

#
# A class for the line = tracks that can be used to draw a footprint
# in a footprint library (PcbLib)
#
class Line:
    
    #
    # Parse properties from binary string
    # e.g. as read from a PcbLib file
    #
    def __init__(self, data):

        # Record Type = Line
        assert ord(data[0]) == 4
        cursor = 1

        # helper function to unpack signed 32-bit integers
        def signed32():
            i = unpack('<i',data[cursor:cursor+4])
            cursor += 4
            return i
        
        # four bytes content length
        contentLength = signed32()
        
        # 13 bytes of unknown purpose
        # that can also be found in Pad records
        cursor += 13
        
        self.X1 = signed32()
        self.Y1 = signed32()
        self.X2 = signed32()
        self.Y2 = signed32()
        
        self.Width = signed32()
        
        # unaccounted bytes
        cursor += 10
        
        # guessed:
        self.Net = ord(data[cursor])
        cursor += 1
        
        # guessed:
        self.Layer = ord(data[cursor])
        
        # one more byte unaccounted for

    #
    # Export pin properties as binary string
    # e.g. for writing it into a PcbLib file
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        
