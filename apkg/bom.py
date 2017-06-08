# Converted from bomutils
# Copyright (C) 2013 Fabian Renn - fabian.renn (at) gmail.com

from struct import *
from collections import namedtuple

import io
from ctypes import Structure, BigEndianStructure, POINTER, c_char, c_uint32, c_uint8, c_uint16, c_char_p, sizeof
from enum import IntEnum
import zlib


BOM_HEADER_FORMAT = '>8sIIIIII'
BOMHeader = namedtuple('BOMHeader', 'magic version numberOfBlocks indexOffset indexLength varsOffset varsLength')

BOM_POINTER_FORMAT = '>II'
BOMPointer = namedtuple('BOMPointer', 'address length')

BOM_BLOCK_TABLE_FORMAT = '>II'  # second member is pointer to start of BOMPointer[]
BOMBlockTable = namedtuple('BOMBlockTable', 'numberOfBlockTablePointers blockPointers')

BOM_FREE_LIST_FORMAT = '>II'
BOMFreeList = namedtuple('BOMFreeList', 'numberOfFreeListPointers freelistPointers')


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


BOM_VAR_FORMAT = '>IB10s'
BOMVar = namedtuple('BOMVar', 'index length name')

BOM_VARS_FORMAT = '>II'
BOMVars = namedtuple('BOMVars', 'count first')


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


class BillOfMaterials(object):

    def __init__(self, path: str=None, fileobj=None):
        if fileobj is None:
            fileobj = open(path, 'rb')

        self._fileobj = fileobj
        # assert BillOfMaterials.is_bom(self._fileobj)

    @classmethod
    def is_bom(cls, fileobj):
        return fileobj.read(8) == b'BOMStore'

    def parse(self):
        self._fileobj.seek(0)
        raw_header = self._fileobj.read(calcsize(BOM_HEADER_FORMAT))
        header = BOMHeader._make(unpack(BOM_HEADER_FORMAT, raw_header))
        print(header)
        #
        print(header.magic)

        print('seek to {}'.format(header.varsOffset))
        self._fileobj.seek(header.varsOffset, 0)

        raw_vars = self._fileobj.read(calcsize(BOM_VARS_FORMAT))
        bvars = BOMVars._make(unpack(BOM_VARS_FORMAT, raw_vars))
        bvars_offset = header.varsOffset + bvars.first
        print(bvars_offset)

        for v in range(0, bvars.count):
            self._fileobj.seek(bvars_offset, 0)
            bvar_raw = self._fileobj.read(calcsize(BOM_VAR_FORMAT))
            bvar = BOMVar._make(unpack(BOM_VAR_FORMAT, bvar_raw))
            print(bvar.name)

            bvars_offset = bvars_offset + calcsize(BOM_VAR_FORMAT) + bvar.length
            # ptr += sizeof(BOMVar) + var->length;
            print(bvars_offset)