#!/usr/bin/python

class PinProperties:
    
    #
    # Parse pin properties from binary string
    # e.g. as read from a SchLib file
    #
    def __init__(self, data):

        # forget about the first 15,5 bytes for now

        # lower two or four bits are for pin orientation
        # 0 = 0°
        # 1 = 90°
        # 2 = 180°
        # 3 = 270°
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
    #
    def __str__(self):
        
        result = "".join([0x00 for i in range(15)])
        
        return result
        
