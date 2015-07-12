#!/usr/bin/python

from common import *
from BinarySubRecord import *
from PcbLib_Arc   import Arc
from PcbLib_Pad   import Pad
from PcbLib_Track import Track
from PcbLib_Fill  import Fill

#
# A PCB library contains PCB footprint definitions.
# The data of a footprint is a serialization of records.
# Records are apparently always binary-encoded
# but may contain text-based SubRecords ("|"-separated list of key=value pairs).
#
# The following record types are recognized:
#
class RecordType:
    Arc         = 1 # binary
    Pad         = 2 # binary
    Track       = 4 # binary
    Fill        = 6 # binary
    Body3D      = 12 # binary with text-based SubRecord

#
# A footprint as it is stored in a PcbLib:
# subfolder with footprint's name
# file "Data" in the subfolder contains the footprint composing records
#
class Footprint:
    
    # read Data from OleFile
    def __init__(self, stream):
        self.stream = str(stream)
        self.size = len(self.stream)

        self.records = []        
        self.parse()
    
    #    
    # begin parsing by parsing the footprint's name
    # then proceed with parsing all records
    #
    def parse(self):

        # first entry is the footprint's name
        header = SubRecord(self.stream)
        self.name = SubRecord_String(header)
        #print "Footprint name: "+self.name
    
        cursor = header.length
    
        # parse all records
        while cursor < self.size:
            record = self.parseRecord(self.stream[cursor:])
            if record is None:
                return
            self.records.append(record)
            cursor += record.length
    
    #
    # parse a record from the stream
    # and add it to object's list of records
    #
    def parseRecord(self, buffer):

        # The first byte defines the type of the record that follows.  
        recordType = ord(buffer[0])
    
        if recordType == RecordType.Arc:
            #print "Record type: Arc"
            arc = Arc(buffer)
            return arc
    
        if recordType == RecordType.Pad:
            #print "Record type: Pad"
            pad = Pad(buffer)
            return pad
    
        elif recordType == RecordType.Track:
            #print "Record type: Track/Line"
            track = Track(buffer)
            return track
    
        elif recordType == 5:
            print "Record type: Unrecognized."
            return None
    
        elif recordType == RecordType.Fill:
            #print "Record type: Fill"
            fill = Fill(buffer)
            return fill
    
        elif recordType == RecordType.Body3D:
            #print "Record type: 3D Body"
            #print "Specifies record length. Continuing."
            
            subrecord = SubRecord(buffer[1:])
            # plus type byte
            subrecord.length += 1
            return subrecord        
    
        else:
            print "Error: Record type unrecognized: "+str(recordType)
            print "Unable to derminine record length. Parser aborting."
            print "Please report an issue on https://github.com/matthiasbock/python-altium"
            return None
