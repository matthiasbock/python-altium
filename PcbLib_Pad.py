#!/usr/bin/python

# https://docs.python.org/2/library/struct.html#format-characters
from struct import unpack

#
# A class for the pads that can be used to draw a footprint
# in a footprint library (PcbLib)
#
class Pad:
    
    #
    # Parse pad properties from binary string
    # e.g. as read from a PcbLib file
    #
    def __init__(self, data):

        # Record Type = Pad
        assert ord(data[0]) == 0x0C
        
        # 0x00
        # 11x 0xFF
        cursor = 12

        # helper function to unpack signed 32-bit integers
        def signed32():
            i = unpack('<i',data[cursor:cursor+4])
            cursor += 4
            return i

        # Location
        self.X = signed32()
        self.Y = signed32()

        # Size and Shape        
        self.XSize_Top = signed32()
        self.YSize_Top = signed32()
        self.XSize_Middle = signed32()
        self.YSize_Middle = signed32()
        self.XSize_Bottom = signed32()
        self.YSize_Bottom = signed32()

        # Hole Size
        self.HoleSize = signed32()
        

    #
    # Export pin properties as binary string
    # e.g. for writing it into a PcbLib file
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        
