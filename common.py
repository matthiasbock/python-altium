#!/usr/bin/python

# https://docs.python.org/2/library/struct.html#format-characters
from struct import unpack

# read two bytes and
# interpret as little-endian 16-bit word
def readShort(f):
    (h,) = unpack('<H', f.read(2))
    return h

# read four bytes and
# interpret as little-endian 32-bit word
def readWord(f):
    (w,) = unpack('<I', f.read(4))
    return w
