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

    print "Parsing "+filename+" ..."

    lib = PcbLib(filename)
