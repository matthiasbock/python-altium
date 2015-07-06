#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# This script is a development "bench"
# for the attempt to parse also the binary content
# of the PcbLib files.
#

from os.path import getsize

from PcbLib import *
from PcbLib_Pad import *

from common import *

#
# In contrast to a SchLib file, in a PcbLib file the records
# do not have a length byte preceeding them, but inside them: first four bytes after record type.
#

def readHeader(f):
    # length: length of name + <length> byte
    f.read(2)

    # discard two bytes (0x 00 00)
    f.read(2)
    
    # 1 byte: length of name
    length = ord(f.read(1))
    Name = ""
    for i in range(length):
        Name += f.read(1)
    print "Name: "+Name+" (length "+str(length)+")"

# read one record from file
def readRecord(f):

    recordType = ord(f.read(1))
    print "Record type: "+str(recordType)    

    if recordType == 1:
        f.read(4)

    elif recordType == 5:
        f.read(18)
        
    elif recordType == PcbComponent_RecordType.Designator:
        length = readWord(f)
        print "Record length: "+str(length)
        ll = ord(f.read(1))
        assert ll == length-1
        value = f.read(ll)
        print "Designator: "+value

    elif recordType == PcbComponent_RecordType.Pad:
        
        
    else:    
        length = readWord(f)
        print "Record length: "+str(length)

    if False:
        # print binary record as hex chars
        for i in range(len(data)):
            print str(i).zfill(2),
        print ""
        for i in range(len(data)):
            print hex(ord(data[i]))[2:].upper().zfill(2),
        print ""
        for i in range(len(data)):
            s = "  "
            if da   ta[i].isalpha():
                s = " "+data[i]
            print s,
        print ""

    return


if __name__ == '__main__':
    from sys import argv
    filename = "Data"
    if len(argv) > 1:
        filename = argv[1]
    size = getsize(filename)

    f = open(filename,"r")
    readHeader(f)
    while (f.tell() < (size-1)):
        readRecord(f)
    f.close()
