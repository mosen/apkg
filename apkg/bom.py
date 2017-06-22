from typing import Generator
import io
from .bom_ctypes import *


def structRead(f_in, classType, advance=True):
    """Borrowed from pudquick"""
    tmp = classType()
    # get how many bytes to read
    sz = sizeof(tmp)
    # read in those many bytes
    bytes = f_in.read(sz)
    # do we have to back up?
    if not advance:
        f_in.seek(-1 * sz, 1)
    memmove(addressof(tmp), bytes, sz)
    return tmp


class BillOfMaterials(object):

    def __init__(self, path: str=None, fileobj=None):
        if fileobj is None:
            fileobj = open(path, 'rb')

        self._fileobj = fileobj
        self._header = structRead(self._fileobj, BOMHeader)
        self._fileobj.seek(self._header.indexOffset)
        self._table = structRead(self._fileobj, BOMBlockTable)
        self._parse_vars(self._header.varsOffset)

    def _parse_vars(self, offset: int):
        self._fileobj.seek(offset)
        variables = structRead(self._fileobj, BOMVars)
        variables.var_list = []
        total_length = 0
        total_length += sizeof(c_uint32)
        var_count = variables.count
        variables.vars = []
        
        for i in range(var_count):
            v = structRead(self._fileobj, BOMVar)
            total_length += sizeof(BOMVar)
            total_length += v.length
            v.name = self._fileobj.read(v.length)
            variables.vars.append(v)

        self._variables = variables

    

    @classmethod
    def is_bom(cls, fileobj):
        return fileobj.read(8) == b'BOMStore'

    @classmethod
    def load(cls, path: str = None, fileobj=None):
        if fileobj is None:
            fileobj = open(path, 'rb')
        
