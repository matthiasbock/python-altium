#!/usr/bin/python

from struct import unpack
from binascii import hexlify

# A pad is binary-encoded and consists of 6 entries of type subrecord.
from BinarySubRecord import *

Shape_Round            = 1
Shape_Rectangular      = 2
Shape_Octagon          = 3
#Shape_RoundedRectangle = 1

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

        # helper function to unpack little-endian 64-bit floats (doubles)
        def float64():
            global cursor
            (f,) = unpack('<d', data[cursor:cursor+8])
            cursor += 8
            return f

        # Location: Refers to the center of the pad
        self.X = signed32()
        self.Y = signed32()

        # Size and Shape
        self.XSize_Top    = signed32()
        self.YSize_Top    = signed32()
        self.XSize_Middle = signed32()
        self.YSize_Middle = signed32()
        self.XSize_Bottom = signed32()
        self.YSize_Bottom = signed32()

        # Hole Size
        self.HoleSize = signed32()
        
        # Pad Shape
        self.Shape_Top    = ord(data[cursor])
        self.Shape_Middle = ord(data[cursor+1])
        self.Shape_Bottom = ord(data[cursor+2])
        cursor += 3
        
        self.Rotation = float64()
        
        # bytes of unknown purpose
        # 01 00 00 00 00 00 00 00
        cursor += 8

        # more bytes of unknown purpose        
        self.unknown1 = signed32()
        
        # 04 00
        cursor += 2
        
        self.unknown2 = signed32()
        self.unknown3 = signed32()
        self.unknown4 = signed32()

        cursor += 4        
        
        self.unknown5 = signed32()

        # debug
        #print self.__dict__
        #print hexlify(data)
        
        # 26 more bytes of unknown purpose following

#
# Sometimes this record is empty / unused and length 0
# It's used though, e.g. if the shape is "Rounded Rectangle" 
#
class SubRecord_SizeAndShapeByLayer:
    def __init__(self, subrecord):

        # assume default values
        # if subrecord is empty
        # Only 29 for Size and Shape, because Top/Middle/Bottom
        # are defined in the previous SubRecord
        self.XSize = [0 for i in range(29)]
        self.YSize = [0 for i in range(29)]
        self.Shape = [0 for i in range(29)]
        self.OffsetFromHoleCenterX = [0 for i in range(32)]
        self.OffsetFromHoleCenterY = [0 for i in range(32)]
        self.CornerRadius = [0 for i in range(32)]
        
        # get data from subrecord
        data = subrecord.content

        if len(data) == 0:
            return

        global cursor
        cursor = 0

        # helper function to unpack signed 32-bit integers
        def signed32():
            global cursor
            (i,) = unpack('<i',data[cursor:cursor+4])
            cursor += 4
            return i

        for i in range(29):
            self.XSize[i] = signed32()
        
        for i in range(29):
            self.YSize[i] = signed32()

        # 0x01
        for i in range(29):
            self.Shape[i] = ord(data[cursor])
            cursor += 1

        # bytes of unknown purpose
        # 0x00...
        cursor += 14
        
        for i in range(32):
            self.OffsetFromHoleCenterX[i] = signed32()
        
        for i in range(32):
            self.OffsetFromHoleCenterY[i] = signed32() 
        
        # 0x01
        cursor += 1

        # 0x09
        for i in range(32):
            unknown = ord(data[cursor])
            cursor += 1

        # 0x3C = 60%
        # The percentage is a fraction of the half of the width/height
        # 100% = circle
        for i in range(32):
            self.CornerRadius[i] = ord(data[cursor])
            cursor += 1

        # 0x00
        for i in range(32):
            unknown = ord(data[cursor])
            cursor += 1

        # debug
        #print self.__dict__

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
        self.SizeAndShapeByLayer = SubRecord_SizeAndShapeByLayer(subrecord)

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
    # http://www.w3schools.com/svg/svg_rect.asp
    #
    def __svg__(self):
        p = self.SizeAndShape
        q = self.SizeAndShapeByLayer

        if p.Shape_Top == Shape_Round:
            if q.CornerRadius[0] == 0:
                # Actually this is a circle if XSize==YSize
                # and a rectangle with two half circles attaches at two edges otherwise
                return '<ellipse cx="'+str((p.X+q.OffsetFromHoleCenterX[0])/10000)+'" cy="'+str((p.Y+q.OffsetFromHoleCenterY[0])/10000)+'" rx="'+str(p.XSize_Top/20000)+'" ry="'+str(p.YSize_Top/20000)+'" transform="rotate('+str(p.Rotation)+','+str(p.X/10000)+','+str(p.Y/10000)+')" style="fill:red;stroke:purple;stroke-width:5" />'

        if p.Shape_Top == Shape_Rectangular or p.Shape_Top == Shape_Round: # and CornerRadius > 0 
            x = str((p.X-(p.XSize_Top/2.)+q.OffsetFromHoleCenterX[0])/10000)
            y = str((p.Y-(p.YSize_Top/2.)+q.OffsetFromHoleCenterY[0])/10000)
            w = str(p.XSize_Top/10000.)
            h = str(p.YSize_Top/10000.)
            rx = str(q.CornerRadius[0]/2000000.*p.XSize_Top)
            ry = str(q.CornerRadius[0]/2000000.*p.YSize_Top)
            return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+rx+'" ry="'+ry+'" transform="rotate('+str(p.Rotation)+','+str(p.X/10000)+','+str(p.Y/10000)+')" style="fill:red;stroke:purple;stroke-width:5" />'
        return ''
