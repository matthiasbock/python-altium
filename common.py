#!/usr/bin/python

# https://docs.python.org/2/library/struct.html#format-characters
from struct import unpack

# read two bytes and
# interpret as little-endian 16-bit word
def readShort(f):
    (h,) = unpack('<H', f.read(2))
    return h

# read four bytes from buffer and
# return as unsigned little-endian 32-bit word
def getU32(buffer):
    (word,) = unpack('<I', buffer[:4])
    return word

#
# accept string, without preceeding 4 bytes of string length
#  |a=b|c=d|0x00 ...(trailing bytes ignored)
#
# return dictionary
#  { "a": "b", "c": "d" } 
#
def parseKeyValueString(s):

    properties = s.strip('|').split('|')
    result = {}

    for prop in properties:
        x = prop.split('=')
        key = x[0]
        if len(x) > 1:
            value = x[1]
        else:
            value = ""
        result[key] = value
        
    return result