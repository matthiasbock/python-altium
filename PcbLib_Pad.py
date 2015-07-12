#!/usr/bin/python

from struct import unpack
from binascii import hexlify

# A pad is binary-encoded and consists of 6 entries of type subrecord.
from BinarySubRecord import *

# parse a Size and Shape subrecord
class SubRecord_SizeAndShape:
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
        
        # debug
        #print self.__dict__
        #print hexlify(data)
        
        # 19 bytes of unknown purpose
        cursor += 19

        # more bytes of unknown purpose        
        self.unknown1 = signed32()
        
        cursor += 2
        
        self.unknown2 = signed32()
        self.unknown3 = signed32()
        self.unknown4 = signed32()

        cursor += 4        
        
        self.unknown5 = signed32()

        # 26 more bytes of unknown purpose following

#
# A class for the pads that can be used to draw a footprint
# in a footprint library (PcbLib)
#
class Pad:
    
    #
    # Parse pad properties from binary string
    # e.g. as read from a PcbLib file
    #
    # The record length is dynamic, so parsers need to invoke getLength() afterwards.
    #
    def __init__(self, data):

        # Record Type = Pad
        assert ord(data[0]) == 2
        cursor = 1

        # Six subrecords:
        # Designator (string)
        # unknown (binary)
        # unknown (string)
        # unknown (binary)
        # Size and Shape struct
        # Offset from Hole Center struct
        
        subrecord = SubRecord(data[cursor:])
        cursor += subrecord.length
        self.Designator = SubRecord_String(subrecord)

        self.unknown1 = SubRecord(data[cursor:])
        cursor += self.unknown1.length

        self.unknown2 = SubRecord(data[cursor:])
        cursor += self.unknown2.length

        self.unknown3 = SubRecord(data[cursor:])
        cursor += self.unknown3.length

        subrecord = SubRecord(data[cursor:])
        cursor += subrecord.length
        self.SizeAndShape = SubRecord_SizeAndShape(subrecord)

        subrecord = SubRecord(data[cursor:])
        cursor += subrecord.length
        #self.OffsetFromHoleCenter = SubRecord_OffsetFromHoleCenter(subrecord)

        # last position of cursor equals total length of record
        self.length = cursor

    #
    # Export pin properties as binary string
    # e.g. for writing it into a PcbLib file
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        

    #
    # Interface for Scalable Vector Graphics output
    # http://www.w3schools.com/svg/svg_ellipse.asp
    #
    def __svg__(self):
        p = self.SizeAndShape
        return '<ellipse cx="'+str(p.X/10000)+'" cy="'+str(p.Y/10000)+'" rx="'+str(p.XSize_Top/20000)+'" ry="'+str(p.YSize_Top/20000)+'" style="fill:yellow;stroke:purple;stroke-width:2" />'
        
