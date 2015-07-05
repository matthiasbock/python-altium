#!/usr/bin/python

# Schematic object record types
# A schematic is a hierarchical tree of records
# Each record has a key-value pair indicating it's record type
class RecordType:
    DESIGN_ITEM = "1"
    PIN = "2"
    LABEL = "4"
    BEZIER = "5"
    POLYLINE = "6"
    POLYGON = "7"
    ELLIPSE = "8"
    ROUND_RECTANGLE = "10"
    ELLIPTICAL_ARC = "11"
    ARC = "12"
    LINE = "13"
    RECTANGLE = "14"
    SHEET_SYMBOL = "15"
    POWER_OBJECT = "17"
    PORT = "18"
    NO_ERC = "22"
    NET_LABEL = "25"
    WIRE = "27"
    TEXT_FRAME = "28"
    JUNCTION = "29"
    IMAGE = "30"
    SHEET = "31"
    SHEET_NAME = "32"
    SHEET_FILE_NAME = "33"
    DESIGNATOR = "34"
    PARAMETER = "41"


# default values for all sorts of possible records
RecordDefaults = {}

RecordDefaults[Record.SHEET] =
    {
        RECORD: "31",
        TEMPLATEFILENAME: "C:\\Users\\Public\\Documents\\Altium\\AD13\\Templates\\A4.SchDot",
        SHOWTEMPLATEGRAPHICS: "T",
        CUSTOMY: "800",
        CUSTOMX: "1000",
        SNAPGRIDSIZE: "10",
        BORDERON: "T",
        SHEETNUMBERSPACESIZE: "4",
        SYSTEMFONT: "1",
        HOTSPOTGRIDON: "T",
        HOTSPOTGRIDSIZE: "19",
        HOTSPOTGRIDSIZE_FRAC: "68504",
        VISIBLEGRIDON: "T",
        VISIBLEGRIDSIZE: "19",
        VISIBLEGRIDSIZE_FRAC: "68504",
        DISPLAY_UNIT: "0",
        ISBOC: "T",
        SHEETSTYLE: "1",
        FONTIDCOUNT: "4",
        FONTNAME1: "Times New Roman",
        FONTNAME2: "Times New Roman",
        FONTNAME3: "Times New Roman",
        FONTNAME4: "Times New Roman",
        AREACOLOR: "16317695",
        BOLD4: "T",
        SIZE1: "10",
        SIZE2: "12",
        SIZE3: "10",
        SIZE4: "15",
        USEMBCS: "T",
        ITALIC3: "T",
        ITALIC4: "T",
        children: []
    }
