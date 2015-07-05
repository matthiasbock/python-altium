#!/usr/bin/python

from pyAltium import *

print "Generating schematic..."

schematic = SchematicDocument()

filename = "demo-schematic.json"
print "Saving as \""+filename+"\" ..."
open(filename,'w').write( schematic.__dict__() )

print "done."
