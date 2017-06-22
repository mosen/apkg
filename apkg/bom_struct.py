from struct import *
from collections import namedtuple
from enum import IntEnum

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
BOMPathInfo2 = namedtuple(
    'BOMPathInfo2',
    'type unknown0 architecture mode user group modtime size unknown1 checksum linkNameLength linkName')

BOM_PATH_INFO1_FORMAT = '>II'
BOMPathInfo1 = namedtuple('BOMPathInfo1', 'id index')

BOM_FILE_FORMAT = '>II'
BOMFile = namedtuple('BOMFile', 'parent name')


def read_namedtuple_struct(fileobj, format_string: str, nt):
    raw_bytes = fileobj.read(calcsize(format_string))
    return nt._make(unpack(format_string, raw_bytes))

