#!/usr/bin/python

mm  = 1
mil = 2.54

"""Signal types for a pin"""
class PinElectrical:
    INPUT = "0"
    IO = "1"
    OUTPUT = "2"
    OPEN_COLLECTOR = "3"
    PASSIVE = "4"
    HI_Z = "5"
    OPEN_EMITTER = "6"
    POWER = "7"

"""Symbols for remote connections to common rails"""
class PowerObjectStyle:
    ARROW = "1"
    BAR = "2"
    GND = "4"

class ParameterReadOnlyState:
    NAME = "1"

"""Preset sheet sizes"""
class SheetStyle:
    A4 = "0"
    A3 = "1"
    A = "5"

