#!/usr/bin/python

# https://docs.python.org/2/library/struct.html#format-characters
from struct import unpack

#
# The following classes represent recognized values
# for the corresponding pin property
#

class Pin_ElectricalType:
    Input           = 0
    IO              = 1
    Output          = 2
    OpenCollector   = 3
    Passive         = 4
    HiZ             = 5
    OpenEmitter     = 6
    Power           = 7

class Pin_Graphical_Orientation:
    rotate0         = 0
    rotate90        = 1
    rotate180       = 2
    rotate270       = 3

class Pin_Symbols_Inside:
    NoSymbol            = 0
    PostponedOutput     = 1
    OpenCollector       = 2
    HiZ                 = 3
    HighCurrent         = 4
    Pulse               = 5
    Schmitt             = 6
    OpenCollectorPullUp = 7
    OpenEmitter         = 8
    OpenEmitterPullUp   = 9
    ShiftLeft           = 10
    OpenOutput          = 11

class Pin_Symbols_InsideEdge:
    NoSymbol        = 0
    Clock           = 1

class Pin_Symbols_OutsideEdge:
    NoSymbol        = 0
    Dot             = 1
    ActiveLowInput  = 2
    ActiveLowOutput = 3

class Pin_Symbols_Outside:
    NoSymbol                = 0
    RightLeftSignalFlow     = 1
    AnalogSignalIn          = 2
    NotLogicConnection      = 3
    DigitalSignalIn         = 4
    LeftRightSignalFlow     = 5
    BidirectionalSignalFlow = 6

class Pin_Symbols_LineWidth:
    Smallest        = 0
    Small           = 1

#
# A class for the pin that can be placed into a schematic symbol
# in a schematic symbol library (SchLib)
#
class PinProperties:
    
    #
    # Parse pin properties from binary string
    # e.g. as read from a SchLib file
    #
    def __init__(self, data):

        # 0: 0x02 = Record Type: Pin
        assert ord(data[0]) == 0x02

        # 1-7: unknown (0x 00 00 00 00 01 00 00)
        
        #  8: Symbols -> Inside
        #  9: Symbols -> Inside Edge
        # 10: Symbols -> Outside Edge
        # 11: Symbols -> Outside
        # order may be different
        
        # 12...: Description
        self.Description = ""
        length = ord(data[12])
        cursor = 13+length
        for c in range(13,cursor):
            self.Description += data[c]
        print "Description: "+self.Description
        
        # one byte: unknown (0x01)
        cursor += 1

        # one byte: Electrical Type
        print "Electrical Type: "+str(ord(data[cursor+1]) & 0x0f)
        cursor += 1

        # 15: lower two or four bits are for pin orientation
        b = ord(data[cursor])
        self.DisplayName_Visible = (b & 0x10) > 0 # LSB of higher nibble
        self.Designator_Visible  = (b & 0x08) > 0 # MSB of lower nibble
        self.Orientation         = b & 0x07
        cursor += 1
        print "Orientation: rotate"+str(self.Orientation*90)

        # 16-17: Graphical->Length
        # The pin length is a signed? little-endian 16-bit short integer
        # e.g. 0x1400 => 0020 + "0" => 200mil
        (self.Length,) = unpack('<h', data[cursor:cursor+2])
        cursor += 2
        print "Lenth: "+str(self.Length*10)+"mil"
        
        # 18-19: X
        # 20-21: Y
        # X and Y are signed little-endian 16-bit short integers
        (self.X,self.Y) = unpack('<hh', data[cursor:cursor+4])
        cursor += 4
        print "Location: X = "+str(self.X*10)+"mil, Y = "+str(self.Y*10)+"mil"
        
        # three bytes: RGB color
        self.ColorR = ord(data[cursor])
        self.ColorG = ord(data[cursor+1])
        self.ColorB = ord(data[cursor+2])
        cursor += 3
        print "Color: #"+(hex(self.ColorR)[2:].zfill(2)+hex(self.ColorG)[2:].zfill(2)+hex(self.ColorB)[2:].zfill(2)).upper()
        
        # one byte: unknown (0x00)
        cursor += 1        
        
        # 26...: Display Name and Designator
        #cursor = 26
        strlen = ord(data[cursor])
        cursor += 1
        display_name = data[cursor:cursor+strlen]
        print "Display Name: "+display_name
        print "Display Name Visible: "+str(self.DisplayName_Visible)
        cursor += strlen

        strlen = ord(data[cursor])
        cursor += 1
        designator = data[cursor:cursor+strlen]
        print "Designator: "+designator
        print "Designator Visible: "+str(self.Designator_Visible)
        cursor += strlen

        # last three bytes: unknown

    #
    # Export pin properties as binary string
    # e.g. for writing it into a SchLib file
    # (without preceeding length)
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        
