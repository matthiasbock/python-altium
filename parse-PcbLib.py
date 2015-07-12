#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# This script takes a *.PcbLib file as argument
# which it opens and attempts to parse all PCB Footprints from it.
#

from PcbLib import PcbLib

if __name__ == '__main__':

    # which file do you wish to read?
    from sys import argv
    filename = "Data"
    if len(argv) > 1:
        filename = argv[1]

    # parse...
    print "Parsing "+filename+" ..."
    lib = PcbLib(filename)

    # write an SVG
    print "Export first footprint to PcbLib.svg ..."
    f = open('PcbLib.svg','w')
    footprint = lib.Footprints[1]
    f.write('\
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
   viewBox="-2000 -1000 4000 2000">\n')
    for record in footprint.records:
        f.write(record.__svg__()+'\n')
    f.write('</svg>\n')
    f.close()
