#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# This script is a development "bench"
# for the attempt to parse also the binary content
# of the PcbLib files.
#

from os.path import getsize

from common import *
from BinarySubRecord import *

from PcbLib import *
from PcbLib_Pad import Pad
from PcbLib_Line import Line

#
# parse one record from buffer
#
def readRecord(buffer):

    # The first byte defines the type of the record that follows.  
    recordType = ord(buffer[0])

    if recordType == PcbComponent_RecordType.Pad:
        print "Record type: Pad"
        pad = Pad(buffer)
        return pad

    elif recordType == PcbComponent_RecordType.Line:
        print "Record type: Line"
        line = Line(buffer)
        return line

    else:
        print "Error: Record type unrecognized. Please report an issue on https://github.com/matthiasbock/python-altium."
        return

#
# buffer is the content of a file named Data
# extracted from a PcbLib using java-altium
# as an array of char with length size
#
def parsePcbLibData(buffer, size):

    # first entry is the footprint's name
    header = SubRecord(buffer)
    name = SubRecord_String(header)
    print "Footprint name: "+name

    cursor = header.length

    # parse all records
    while cursor < size:
        record = readRecord(buffer[cursor:])
        cursor += record.length


if __name__ == '__main__':
    # which file do you wish to read?
    from sys import argv
    filename = "Data"
    if len(argv) > 1:
        filename = argv[1]

    # read file into buffer
    buffer = ""
    size = getsize(filename)
    f = open(filename,"r")
    for i in range(size):
        buffer += f.read(1)
    f.close()

    # parse buffer
    parsePcbLibData(buffer, size)
