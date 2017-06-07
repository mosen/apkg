# Converted from bomutils
# Copyright (C) 2013 Fabian Renn - fabian.renn (at) gmail.com

from ctypes import Structure, POINTER, c_char, c_uint32, c_uint8, c_uint16, c_char_p
from enum import IntEnum
import zlib


class BOMHeader(Structure):
    _fields_ = [
        ("magic", c_char * 8),
        ("version", c_uint32),
        ("numberOfBlocks", c_uint32),
        ("indexOffset", c_uint32),
        ("indexLength", c_uint32),
        ("varsOffset", c_uint32),
        ("varsLength", c_uint32),
    ]


class BOMPointer(Structure):
    _fields_ = [
        ("address", c_uint32),
        ("length", c_uint32),
    ]


class BOMBlockTable(Structure):
    _fields_ = [
        ("numberOfBlockTablePointers", c_uint32),
        ("blockPointers", POINTER(BOMPointer)),
    ]


class BOMFreeList(Structure):
    _fields_ = [
        ("numberOfFreeListPointers", c_uint32),
        ("freelistPointers", POINTER(BOMPointer)),
    ]


class BOMInfoEntry(Structure):
    _fields_ = [
        ("unknown0", c_uint32),
        ("unknown1", c_uint32),
        ("unknown2", c_uint32),
        ("unknown3", c_uint32),
    ]


class BOMInfo(Structure):
    _fields_ = [
        ("version", c_uint32),
        ("numberOfPaths", c_uint32),
        ("numberOfInfoEntries", c_uint32),
        ("entries", POINTER(BOMInfoEntry)),
    ]


class BOMTree(Structure):
    _fields_ = [
        ("tree", c_char * 4),
        ("version", c_uint32),
        ("child", c_uint32),
        ("blockSize", c_uint32),
        ("pathCount", c_uint32),
        ("unknown3", c_uint8),
    ]


class BOMVIndex(Structure):
    _fields_ = [
        ("unknown0", c_uint32),
        ("indexToVTree", c_uint32),
        ("unknown2", c_uint32),
        ("unknown3", c_uint8),
    ]


class BOMVar(Structure):
    _fields_ = [
        ("index", c_uint32),
        ("length", c_uint8),
        ("name", c_char_p),
    ]


class BOMVars(Structure):
    _fields_ = [
        ("count", c_uint32),
        ("first", POINTER(BOMVar)),
    ]


class BOMPathIndices(Structure):
    _fields_ = [
        ("index0", c_uint32),
        ("index1", c_uint32),
    ]


class BOMPaths(Structure):
    _fields_ = [
        ("isLeaf", c_uint16),
        ("count", c_uint16),
        ("forward", c_uint32),
        ("backward", c_uint32),
        ("indices", POINTER(BOMPathIndices)),
    ]


class BOMItemType(IntEnum):
    File = 1
    Directory = 2
    Link = 3
    Device = 4


class BOMPathInfo2(Structure):
    _fields_ = [
        ("type", c_uint8),  # BOMItemType
        ("unknown0", c_uint8),
        ("architecture", c_uint16),
        ("mode", c_uint16),
        ("user", c_uint32),
        ("group", c_uint32),
        ("modtime", c_uint32),
        ("size", c_uint32),
        ("unknown1", c_uint8),
        ("checksum", c_uint32),  # union with device type
        ("linkNameLength", c_uint32),
        ("linkName", POINTER(c_char)),
    ]


class BOMPathInfo1(Structure):
    _fields_ = [
        ("id", c_uint32),
        ("index", POINTER(BOMPathInfo2)),
    ]


class BOMFile(Structure):
    _fields_ = [
        ("parent", c_uint32),
        ("name", c_char_p),
    ]
