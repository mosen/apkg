import argparse
import logging
from struct import calcsize
from io import BytesIO
from .bom import BOMHeader, BOM_HEADER_FORMAT, read_namedtuple_struct, BOMBlockTable, BOM_BLOCK_TABLE_FORMAT, \
    BOM_POINTER_FORMAT, BOMPointer, BOM_VARS_FORMAT, BOMVars, BOM_VAR_FORMAT, BOMVar

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='test dumpbom implementation')
    parser.add_argument('bom', help='Path to BOMStore')

    args = parser.parse_args()

    print(args.bom)

    with open(args.bom, 'rb') as fd:
        buf = fd.read()

    print("file_length = ", len(buf))
    print("Header:")
    print("-" * 20)

    bio = BytesIO(buf)

    header = read_namedtuple_struct(bio, BOM_HEADER_FORMAT, BOMHeader)

    bio.seek(header.indexOffset)
    block_table = read_namedtuple_struct(bio, BOM_BLOCK_TABLE_FORMAT, BOMBlockTable)

    block_table_pointer_count = block_table.numberOfBlockTablePointers
    pointers = []
    non_null_entries = 0
    for i in range(0, block_table_pointer_count):
        bio.seek(block_table.blockPointers + i * calcsize(BOM_POINTER_FORMAT))
        ptr = read_namedtuple_struct(bio, BOM_POINTER_FORMAT, BOMPointer)
        if ptr.address != 0:
            non_null_entries = non_null_entries + 1
        pointers.append(ptr)

    print(len(pointers))
    print(non_null_entries)

    print("magic = ", header.magic)
    print("version = ", header.version)
    print("numberOfBlocks = ", header.numberOfBlocks)
    print("indexOffset = ", header.indexOffset)
    print("indexLength = ", header.indexLength)
    print("varsOffset =", header.varsOffset)
    print("varsLength =", header.varsLength)

    print("(calculated number of blocks = ", ")")

    print("Variables:")
    print("-" * 20)

    bio.seek(header.varsOffset)
    bomvars = read_namedtuple_struct(bio, BOM_VARS_FORMAT, BOMVars)
    print(bomvars)

    first = bomvars.first
    bio.seek(first)
    total_length = 0
    total_length = total_length + calcsize('I')

    for i in range(0, bomvars.count):
        bv = read_namedtuple_struct(bio, BOM_VAR_FORMAT, BOMVar)
        total_length = total_length + calcsize('I')
        total_length = total_length + bv.length + 1
        bio.seek(first + total_length)

    print("vars->count =", bomvars.count)
    print(total_length)
