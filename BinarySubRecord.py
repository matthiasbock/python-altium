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
        #print "SubRecord length: "+str(self.contentLength) 
        
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
    #print "String length: "+str(length)
    assert length == subrecord.length-5

    # skip length byte
    return subrecord.content[1:]

#
# There is a SubRecord that can be found
# in all PCB Component records so far
# but is yet of unknown purpose.
# The length appears to be always 13. 
#
class SubRecord_Common:
    
    def __init__(self, subrecord):
        
        # get data from subrecord
        #data = subrecord.content

        # First byte:
        # Line: 0x39
        # Pad SizeAndShape: 0x4A or 0x01
        # Arc:  0x21
        # 3D Body: 0x45
        
        # The remaining bytes are always the same:
        # 0x 0C 00
        # 10x 0xFF
    
        self.length = 13
