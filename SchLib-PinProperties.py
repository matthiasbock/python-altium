#!/usr/bin/python

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
    NoSymbol                = 0
    PostponedOutput         = 1
    OpenCollector           = 2
    HiZ                     = 3
    HighCurrent             = 4
    Pulse                   = 5
    Schmitt                 = 6
    OpenCollectorPullUp     = 7
    OpenEmitter             = 8
    OpenEmitterPullUp       = 9
    ShiftLeft               = 10
    OpenOutput              = 11

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

        # forget about the first 15,5 bytes for now

        # lower two or four bits are for pin orientation

        self.Orientation = ord(data[15]) & 0x0f
        print "Pin orientation: "+str(self.Orientation*90)+"deg"

        # x and y are signed 16-bit shorts
        (x,y) = unpack('<hh', data[18:22])
        print "x="+str(x)+", y="+str(y)
        
        # disregard another four bytes (0x00)        
        
        # Display Name and Designator
        cursor = 22+4

        strlen = ord(data[cursor])
        cursor += 1
        display_name = data[cursor:cursor+strlen]
        print "Display Name: "+display_name
        cursor += strlen

        strlen = ord(data[cursor])
        cursor += 1
        designator = data[cursor:cursor+strlen]
        print "Designator: "+designator
        cursor += strlen

        # ...might actually also be the other way around

        # disregard three more bytes

    #
    # Export pin properties as binary string
    # e.g. for writing it into a SchLib file
    # (without preceeding length)
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        
