#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# This script is a development "bench"
# for the attempt to parse also the binary content
# of (currently) the SchLib files.
#
# It does not use the OLE library
# but uses java-altium (Apache POIFS) for OLE document unpacking.  
#

# https://docs.python.org/2/library/struct.html#format-characters
from struct import unpack

from os.path import getsize

# read two bytes and
# interpret as little-endian 16-bit word
def readShort(f):
    (h,) = unpack('<H', f.read(2))
    return h

# read four bytes and
# interpret as little-endian 32-bit word
def readWord(f):
    (w,) = unpack('<I', f.read(4))
    return w

class PinProperties:
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
        
        # designator and identifier
        cursor = 22+4

        strlen = ord(data[cursor])
        cursor += 1
        identifier = data[cursor:cursor+strlen]
        print "Identifier: "+identifier
        cursor += strlen

        strlen = ord(data[cursor])
        cursor += 1
        designator = data[cursor:cursor+strlen]
        print "Designator: "+designator
        cursor += strlen

        # disregard three more bytes
     

# read one record from file
def readRecord(f, debug=True):

    # length: little-endian short
    length = readShort(f)

    # discard one byte, always 0x00
    f.read(1)
    
    # type: one byte
    # 0x00 = string
    # 0x01 = binary
    isBinary = ord(f.read(1)) == 1

    #print "Record is binary: "+str(isBinary)    
    #print "Reading record of "+str(length)+" bytes:"
    
    if length == 0:
        print "Surprinsingly the length is zero. That's probably an error."
        return

    # read <length> bytes from file        
    data = f.read(length)

    # text
    if not isBinary:
        # strip trailing 0x00 (string terminator)
        while len(data) > 0 and data[len(data)-1] == chr(0x00):
            #if debug:
                #print "Last char is 0x00 (C-style string terminator). Stripping that."
            data = data[:len(data)-1]
    else:
        # print hex chars
        for i in range(len(data)):
            print hex(ord(data[i]))[2:].upper().zfill(2),
        print ""
        
        binaryType = ord(data[0])
        
        # schematic symbol: pin
        if binaryType == 0x02:
            p = PinProperties(data)

        # pin symbol: line?
        elif binaryType == 0xD0:
            #...
            print "Sorry, this binary type is not supported yet."

    if debug:
        if data[0] == "|" and len(data) > 1:
            #print "Stripped leading '|'."
            data = data[1:]
            
            # '|'-separated list of key=value pairs
            x = data.split('|')
            
            # generate dictionary of key=value pairs
            pairs = {}
            for p in x:
                xx = p.split('=')
                pairs[xx[0]] = xx[1]

            print pairs

        if data[0].isalpha():
            print data
        else:
            print "Record is binary."

    return


if __name__ == '__main__':
    from sys import argv
    filename = "Data"
    if len(argv) > 1:
        filename = argv[1]
    size = getsize(filename)
    f = open(filename,"r")
    while (f.tell() < (size-1)):
        readRecord(f)
    f.close()
    