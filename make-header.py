#!/usr/bin/python

from pyAltium import *

print "Generating library..."

# initialize new, empty library with default settings
library = PCBLibrary()

print "Generating 2x50 pin header component..."
# initialize with default values
component = PCBComponent()

for x in range(1,2):
    for y in range(1,50):
        e = Pad(-2*100*mil + x*100*mil, -25*100*mil + y*100*mil) 
        component.append(e)

library.append(component)

filename = "header.PcbLib"
print "Saving library as \""+filename+"\" ..."
library.savePcbLib(filename)

print "done."