#!/usr/bin/python

#
# A schematic library contains schematic symbols definitions.
# The data of a symbol definition is a serialized bunch of data records.
# Each record has a certain type,
# the following types are recognized:
#
class RecordType:
    SchematicComponent  = 1 # ?
    Pin                 = 2
    # ?                 = 3
    Label               = 4
    Bezier              = 5
    Polyline            = 6
    Polygon             = 7
    Ellipse             = 8
    # ?                 = 9
    RoundRectangle      = 10
    EllipticalArc       = 11
    Arc                 = 12
    Line                = 13
    Rectangle           = 14
    SheetSymbol         = 15
    # ?                 = 16
    PowerObject         = 17
    Port                = 18
    # ?                 = 19,20,21
    NoErc               = 22
    # ?                 = 23,24
    NetLabel            = 25
    # ?                 = 26
    Wire                = 27
    TextFrame           = 28
    Junction            = 29
    Image               = 30
    Sheet               = 31
    SheetName           = 32
    SheetFileName       = 33
    Designator          = 34
    # ?                 = 35,36,37,38,39,40
    Parameter           = 41

# IEEE symbols ?
