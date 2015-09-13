#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# This script takes a *.PcbDoc file as argument
# which it opens and attempts to parse.
#

from PcbDoc import PcbDoc
from json import dumps

# which file do you wish to read?
from sys import argv
filename = ""
if len(argv) > 1:
    filename = argv[1]

# parse...
print "Parsing "+filename+" ..."
pcb = PcbDoc(filename)

# export JSON
filename = "export.json"
print "Exporting "+filename+" ..."
open(filename, "w").write( dumps(pcb.Components, sort_keys=True, indent=4) )

# export SVG
filename = "export.svg"
print "Exporting "+filename+" ..."

result = '\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\
<svg\n\
   xmlns:dc="http://purl.org/dc/elements/1.1/"\n\
   xmlns:cc="http://creativecommons.org/ns#"\n\
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\
   xmlns:svg="http://www.w3.org/2000/svg"\n\
   xmlns="http://www.w3.org/2000/svg"\n\
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n\
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n\
   id="svg1"\n\
   version="1.1"\
   width="100%"\n\
   height="100%"\n\
   background="black"\n\
   viewBox="2000 4000 4000 4000">\n'

for component in pcb.Components:
    if "X" in component.keys():
        x = component["X"].replace('mil','')
    else:
        continue
    if "Y" in component.keys():
        y = component["Y"].replace('mil','')
    else:
        continue
    height = "10"
    if "HEIGHT" in component.keys():
        height = component["HEIGHT"].replace('mil','')
    width = height
    designator = ""
    if "SOURCEDESIGNATOR" in component.keys():
        designator = component["SOURCEDESIGNATOR"]
    result += '<rect x="'+x+'" y="'+y+'" width="'+width+'" height="'+height+'" style="stroke:rgb(255,0,0);fill:rgba(0,200,0,0.1);stroke-width:2" />\n'
    result += '<text x="'+x+'" y="'+y+'" style="fill:yellow;font-size:20px;">'+designator+'</text>\n'

result += '</svg>\n'

open(filename, "w").write(result)
