from ctypes import sizeof, c_uint32
from .bom_struct import *

HEADER_SIZE = 512
size_of_vars = sizeof(c_uint32)


class BOMStorage(object):
    def __init__(self):
        entry_size = 0
        self._header = BOMHeader(
            magic='BOMStore',
            version=1,
            numberOfBlocks=0,
            indexOffset=(HEADER_SIZE + size_of_vars + entry_size),
        )
        self._vars = BOMVars()
        self._table = BOMBlockTable()
        self._freeList = BOMFreeList()
        