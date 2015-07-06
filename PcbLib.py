#!/usr/bin/python

#
# A PCB library contains PCB footprint definitions.
# The data of a definition is a serialized bunch of data records.
# Records of footprints are apparently all stored in binary form.
# Binary records begin with one byte representing the record type. 
# The following types are recognized:
#
class PcbComponent_RecordType:
    #unknwon = 1 # length 16
    Designator  = 2
    Pad         = 12
    Line        = 4 #?
