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

    # export all footprints as SVG
    print "Exporting "+str(len(lib.Footprints))+" footprints to SVG ..."
    for footprint in lib.Footprints:
        print " * "+footprint.name
        f = open(footprint.name+'.svg','w')
        f.write( footprint.__svg__() )
        f.close()

    