#!/usr/bin/python

from struct import unpack

#
# Text records are immediately followed by a string
# The records appear to only contain properties, e.g. a Font name
# but the length field of the record does not include the string after the record
#
from BinarySubRecord import *

FontType_TrueType = 0
FontType_Stroke   = 1
FontType_BarCode  = 2

# parse
class SubRecord_Text:
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
        self.X = signed32()
        self.Y = signed32()
        self.Height = signed32()
        
        # Width? not there

        self.FontType = ord(data[cursor])
        cursor += 1

        # unknown purpose: 0x00
        cursor += 1
        
        # may start/end earlier
        self.Rotation = float64()
        
        self.unknownx = signed32()        

        # 32 bytes somehow with a Font name
        cursor += 29
        
        self.unknown4 = signed32()

        # 00 04
        cursor += 2

        # another 5 signed-32 of unknown purpose
        for i in range(5):
            self.__dict__["unknown"+str(i+5)] = signed32()
        
        # 0x00...
        cursor += 17
        
        # another signed32
        self.unknown10 = signed32()
        
        # 0x00...
        cursor += 9

        # debug
        print self.__dict__
       
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
# A class for the Text elements
# you can put in a footprint
#
class Text:
    
    #
    # Parse properties from binary string
    # e.g. as read from a PcbLib file
    #
    def __init__(self, data):

        # Record Type = Fill
        assert ord(data[0]) == 5
        
        prop = SubRecord(data[1:])
        self.Properties = SubRecord_Text(prop)
        
        text = SubRecord(data[1+prop.length:])
        self.Text = SubRecord_String(text)
        print self.Text
        
        # No bytes unaccounted for
        self.length = 1 + prop.length + text.length

    #
    # Export pin properties as binary string
    # e.g. for writing it into a PcbLib file
    #
    def __str__(self):
        return ''

    #
    # Interface for Scalable Vector Graphics output
    # http://www.w3schools.com/svg/svg_text.asp
    #
    def __svg__(self):
        return '<text x="'+str(self.Properties.X/10000)+'" y="'+str(self.Properties.Y/10000)+'" font-size="'+str(self.Properties.Height/10000)+'px" fill="green">'+self.Text+'</text>'
