#!/usr/bin/python

import struct
from io import SEEK_CUR
from json import dumps as json_dumps

try:
    from OleFileIO_PL import OleFileIO, set_debug_mode
except ImportError:
    # Pillow version tends to do illegal seeks with Altium files
    from PIL.OleFileIO import OleFileIO, set_debug_mode

from altium_constants import *

# set OLE parser debug mode
set_debug_mode(True)

# hierarchy of split characters:
# char 2 is the split char in key-value pairs splitted with char 1
# char 3 is the split char to use after char 2
CHR_SPLIT1 = "|"
CHR_SPLIT2 = "`"
CHR_SPLIT3 = "?"

# example:
# |2DCONFIGURATION=`RECORD=Board`CFGALL.CONFIGURATIONKIND=1`CFG2D.LAYEROPACITY.TOPLAYER=1.00?1.00?1.00?.... 

# check if string contains non-printable chars
def isPrintable(s):
    if s.isalpha() or s.find(".") > -1 or s.find(CHR_SPLIT1) > -1 or s.find(CHR_SPLIT2) > -1 or s.find(CHR_SPLIT3) > -1:
        return True
    return False

# split string into substrings
# return dictionary
def parse(properties, split_char, next_split_char):
    # start with empty result dictionary
    if split_char == CHR_SPLIT3:
        # third hierarchy depth is only a list, not a key=value pair
        obj = []
    else:
        obj = {}
    
    # properties are a split-char separated list of key=value pairs
    for property in properties.split(split_char):
        if not property:
            # Most (but not all) property lists are
            # prefixed with a pipe "|",
            # so ignore an empty property,
            # especially before the first entry
            continue
        
        # ignore empty property
        if len(property) == 0:
            continue
        
        if type(obj) is list:
            obj.append(property)
            
        elif property.find("=") > -1:
            values = property.split(b"=", 1)
            if len(values) < 2:
                values.append("")
            (name, value) = (values[0], "=".join(values[1:]))

            if name == "UNIQUEID":
                # strip trailing 0x00s, that for some reason appear sometimes (OLE parser error?) 
                value = value[:8]

            # strip chr(0)s
            value = value.replace(chr(0x00),'')
            if value.isalpha():
                # decode as ASCII (OLE parser error)
                value = value.decode('ascii')
            else:
                value = "<not printable>"
            
            # property contains a split char?
            if property.find(next_split_char) > -1:
                obj[name] = parse(value, next_split_char, CHR_SPLIT3)
            else:
                obj[name] = value
        else:
            print "Not a key=value pair:"
            print " "+property
    
    return obj

def read(section):
    # open OLE stream
    global ole
    stream = ole.openstream(section)
    
    # start with an empty list of objects
    objects = []
    while True:
        # first four bytes indicate object length
        length = stream.read(4)
        if not length:
            # end of stream
            break

        # interpret as little endian integer (32bit)
        (length,) = struct.unpack("<I", length)
        
        # read specified number of bytes without null terminator
        properties = stream.read(length - 1)
        obj = {}

        obj = parse(properties, CHR_SPLIT1, CHR_SPLIT2)        

        if obj != {}:
            objects.append(obj)
        
        # Skip over null terminator byte
        stream.seek(+1, SEEK_CUR)
 
#    print json_dumps(objects, indent=4) 
   
    return objects



from sys import stderr
import os
import os.path
from datetime import date
import contextlib
from importlib import import_module
from inspect import getdoc
from argparse import ArgumentParser

def main():
    # initialize OLE file parser
    global ole
    parser = ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    # open file by filename
    ole = OleFileIO(args.file)
    content = ole.listdir()
    print "File contents:"
    print content,"\n"

    # parse FileHeader
    objects = read("FileHeader")
    result = {}
    result["FileHeader"] = objects
    
    # parse all other contents
    for doc in content:
        if len(doc) > 1:
            path = "/".join(doc)
            print path
            if not doc[0] in result:
                result[doc[0]] = {}
            result[doc[0]][doc[1]] = read(path)
        else:
            result[doc[0]] = read(doc)

    # output parsed content as formatted JSON
    print json_dumps(result, indent=4)


if __name__ == "__main__":
    main()
