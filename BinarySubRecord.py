#!/usr/bin/python

from struct import *

#
# A SubRecord is something you find inside files named "Data"
# extracted from an Altium PcbLib using java-altium.
#
# Several SubRecords can be present within one record,
# e.g. Pad records consist of six SubRecords.
#
# A subrecord begins with 4 bytes representing the subrecord content length
# followed by the subrecord content.
# 
class SubRecord:

    #
    # Read in a subrecord
    #
    def __init__(self, data):
        
        # first four bytes are length
        (self.contentLength,) = unpack('<I', data[:4])
        print "SubRecord length: "+str(self.contentLength) 
        
        self.content = ""
        for i in range(self.contentLength):
            self.content += data[4+i]
    
        self.length = 4 + self.contentLength

#
# parse SubRecord as string
#
def SubRecord_String(subrecord):

    # verify string length
    length = ord(subrecord.content[0])
    print "String length: "+str(length)
    assert length == subrecord.length-5

    # skip length byte
    return subrecord.content[1:]


    
