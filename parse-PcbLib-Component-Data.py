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
from PcbLib_Pad import *

#
# parse one record from buffer
#
def readRecord(buffer):

    recordType = ord(buffer[0])
    print "Record type: "+str(recordType)

    if recordType == PcbComponent_RecordType.Pad:
        pad = Pad(buffer)
        return pad

    else:
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
    print "Name: "+name

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
