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

from SchLib import *
from SchLib_PinProperties import *

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
        # print binary record as hex chars
        for i in range(len(data)):
            print str(i).zfill(2),
        print ""
        for i in range(len(data)):
            print hex(ord(data[i]))[2:].upper().zfill(2),
        print ""

        # extract record type        
        binaryType = ord(data[0])
        
        # evaluate record type
        if binaryType == RecordType.Pin:
            parsed = PinProperties(data)

        else:
            print "Record of unsupported type:",

            # kind of a switch-case statement
            def printUnsupported(s):
                print s
            {
                Bezier              : printUnsupported("Bezier"),
                Polyline            : printUnsupported("Polyline"),
                Polygon             : printUnsupported("Polygon"),
                Ellipse             : printUnsupported("Ellipse"),
                RoundRectangle      : printUnsupported("Round Rectangle"),
                EllipticalArc       : printUnsupported("Elliptical Arc"),
                Arc                 : printUnsupported("Arc"),
                Line                : printUnsupported("Line"),
                Rectangle           : printUnsupported("Rectangle")
            }[binaryType]()

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
    