# Converted from bomutils
# Copyright (C) 2013 Fabian Renn - fabian.renn (at) gmail.com

from struct import *
from collections import namedtuple

from enum import IntEnum

import io

BOM_HEADER_FORMAT = '>8sLLLLLL'
BOMHeader = namedtuple('BOMHeader', 'magic version numberOfBlocks indexOffset indexLength varsOffset varsLength')

BOM_POINTER_FORMAT = '>II'
BOMPointer = namedtuple('BOMPointer', 'address length')

BOM_BLOCK_TABLE_FORMAT = '>II'  # second member is pointer to start of BOMPointer[]
BOMBlockTable = namedtuple('BOMBlockTable', 'numberOfBlockTablePointers blockPointers')

BOM_FREE_LIST_FORMAT = '>II'
BOMFreeList = namedtuple('BOMFreeList', 'numberOfFreeListPointers freelistPointers')

BOM_INFO_ENTRY_FORMAT = '>IIII'
BOMInfoEntry = namedtuple('BOMInfoEntry', 'unknown0 unknown1 unknown2 unknown3')

BOM_INFO_FORMAT = '>IIII'
BOMInfo = namedtuple('BOMInfo', 'version numberOfPaths numberOfInfoEntries entries')

BOM_TREE_FORMAT = '>4cIIIIB'
BOMTree = namedtuple('BOMTree', 'tree version child blockSize pathCount unknown3')

BOM_VINDEX_FORMAT = '>IIIB'
BOMVindex = namedtuple('BOMVIndex', 'unknown0 indexToVTree unknown2 unknown3')

BOM_VAR_FORMAT = '>IB'
BOMVar = namedtuple('BOMVar', 'index length')  # name member starts at end of BOMVar, goes for 'length'

BOM_VARS_FORMAT = '>LI'
BOMVars = namedtuple('BOMVars', 'count first')

BOM_PATH_INDICES_FORMAT = '>II'
BOMPathIndices = namedtuple('BOMPathIndices', 'index0 index1')

BOM_PATHS_FORMAT = '>HHIII'
BOMPaths = namedtuple('BOMPaths', 'isLeaf count forward backward indices')


class BOMItemType(IntEnum):
    File = 1
    Directory = 2
    Link = 3
    Device = 4

BOM_PATH_INFO2_FORMAT = '>BBHHIIIIBIII'
BOMPathInfo2 = namedtuple('BOMPathInfo2',
                'type unknown0 architecture mode user group modtime size unknown1 checksum linkNameLength linkName')

BOM_PATH_INFO1_FORMAT = '>II'
BOMPathInfo1 = namedtuple('BOMPathInfo1', 'id index')

BOM_FILE_FORMAT = '>II'
BOMFile = namedtuple('BOMFile', 'parent name')


def read_namedtuple_struct(fileobj, format_string, nt):
    raw_bytes = fileobj.read(calcsize(format_string))
    return nt._make(unpack(format_string, raw_bytes))


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

        header = read_namedtuple_struct(self._fileobj, BOM_HEADER_FORMAT, BOMHeader)
        print(header)

        self._fileobj.seek(header.indexOffset, io.SEEK_SET)
        block_table = read_namedtuple_struct(self._fileobj, BOM_BLOCK_TABLE_FORMAT, BOMBlockTable)
        print(block_table)

        # Read all the pointers in (number * pointer size)
        block_table_pointers = self._fileobj.read(calcsize(BOM_POINTER_FORMAT) * block_table.numberOfBlockTablePointers)

        numberOfNonNullEntries = 0
        for i in range(0, block_table.numberOfBlockTablePointers):
            ptr_offset, = unpack('>I', block_table_pointers[i*4:i*4+4])
            self._fileobj.seek(header.indexOffset + ptr_offset)
            ptr = read_namedtuple_struct(self._fileobj, BOM_POINTER_FORMAT, BOMPointer)
            if ptr.address != 0:
                numberOfNonNullEntries = numberOfNonNullEntries + 1
            
        print('non null entries', numberOfNonNullEntries)


        # print('seek to varsOffset {}'.format(header.varsOffset))
        # self._fileobj.seek(header.varsOffset, 0)
        #
        # raw_vars = self._fileobj.read(calcsize(BOM_VARS_FORMAT))
        # bvars = BOMVars._make(unpack(BOM_VARS_FORMAT, raw_vars))
        # print(bvars)
        # print('BOMVars first at ', bvars.first)
        # bvars_offset = header.varsOffset + bvars.first
        # print('BOMVars vars offset', bvars_offset)
        #
        # for v in range(0, bvars.count):
        #     self._fileobj.seek(bvars_offset, 0)
        #     print(bvars_offset)
        #     bvar_raw = self._fileobj.read(calcsize(BOM_VAR_FORMAT))
        #     bvar = BOMVar._make(unpack(BOM_VAR_FORMAT, bvar_raw))
        #     print(bvar)
        #     print('bvar length: ', bvar.length)
        #     bvar_name = self._fileobj.read(bvar.length)
        #     print(bvar_name)
        #
        #     bvars_offset = bvars_offset + calcsize(BOM_VAR_FORMAT) + (bvar.length-1)
        #     # ptr += sizeof(BOMVar) + var->length;
