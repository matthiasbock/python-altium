#!/usr/bin/python

#
# A PCB library contains PCB footprint definitions.
# The data of a definition is a serialization of records.
# Records are apparently always binary-encoded
# but may contain text-based SubRecords ("|"-separated list of key=value pairs).
#
# The following record types are recognized:
#
class PcbComponent_RecordType:
    Arc         = 1 # binary
    Pad         = 2 # binary
    Track       = 4 # binary
    Fill        = 6 # binary
    Body3D      = 12 # binary with text-based SubRecord
