#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#
# This script takes a *.PcbDoc file as argument
# which it opens and attempts to parse.
#

from PcbDoc import PcbDoc

# which file do you wish to read?
from sys import argv
filename = ""
if len(argv) > 1:
    filename = argv[1]

# parse...
print "Parsing "+filename+" ..."
lib = PcbDoc(filename)
