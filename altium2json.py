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

set_debug_mode(True)

def read(section):
    global ole

    stream = ole.openstream(section)
    
    # start with an empty list of objects
    objects = []
    while True:
        # first four bytes indicate object length
        length = stream.read(4)
        if not length:
            break
        # interpret as little endian integer (32bit)
        (length,) = struct.unpack("<I", length)
        
        # read specified number of bytes without null terminator
        properties = stream.read(length - 1)
        obj = {}
        for property in properties.split(b"|"):
            if not property:
                # Most (but not all) property lists are
                # prefixed with a pipe "|",
                # so ignore an empty property before the prefix
                continue
            
            if len(property) > 0 and property[0].isalpha():
                values = property.split(b"=", 1)
                (name, value) = (values[0], "=".join(values[1:]))
                if name == "UNIQUEID":
                    # strip trailing 0x00s, that for some reason appear sometimes 
                    value = value[:8]
                if value.isalpha():
                    obj[name] = value.replace(chr(0x00),'').decode('ascii')

#       print obj
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
    global ole
    parser = ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    # open file by filename

    result = {}

    ole = OleFileIO(args.file)
    content = ole.listdir()
    print "File contents:"
    print content

    objects = read("FileHeader")
    result["FileHeader"] = objects
    for doc in content:
        if len(doc) > 1:
            path = "/".join(doc)
            print path
            if not doc[0] in result:
                result[doc[0]] = {}
            result[doc[0]][doc[1]] = read(path)
        else:
            result[doc[0]] = read(doc)

    print json_dumps(result, indent=4)


if __name__ == "__main__":
    main()
