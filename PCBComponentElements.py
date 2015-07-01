#!/usr/bin/python

TYPE_UNDEFINED = 0
TYPE_PAD       = 1

class PCBComponentElement:
    
    def __init__(self):
        self.type = TYPE_UNDEFINED


class Pad(PCBComponentElement):
    
    def __init__(self, x, y):
        self.type = TYPE_PAD
        self.x = x
        self.y = y
