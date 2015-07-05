
#
# Class for parsing Altium SchDoc files
# previously converted to JSON by java-altium
#

from SchematicDocumentRecordDefaults import *

class SchematicRecord:
    
    # initialize with default parameters or given dictionary
    def __init__(self, Type, Dict):
        if Dict is None:
            if Type is None:
                Type = RecordType.SHEET
            self.values = RecordDefaults[Type]
        else:
            self.values = Dict
            self.values.RECORD = Type

    # dict(schematic) returns dictionary
    def __dict__(self):
        return self.values


# basically just a wrapper for the above
# since a schematic is just a record of record type 1
class SchematicDocument:
    def __init__(self, Dict):
        SchematicRecord.__init__(self, RecordType.SHEET, Dict)
