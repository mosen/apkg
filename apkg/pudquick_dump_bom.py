# Python routines for parsing bom files
#
# Examples so far:
#
# dump_bom(filename) - prints diagnostic structure information about bom file (including path list)

from .bom_ctypes import *


def structRead(f_in, classType, advance=True):
    tmp = classType()
    # get how many bytes to read
    sz = sizeof(tmp)
    # read in those many bytes
    bytes = f_in.read(sz)
    # do we have to back up?
    if (not advance):
        f_in.seek(-1 * sz, 1)
    memmove(addressof(tmp), bytes, sz)
    return tmp


def bom_file(f, addr):
    # Get current position
    a = f.tell()
    f.seek(addr)
    out = structRead(f, BOMFile)
    # Now to get the name
    name = ''
    c = f.read(1)
    while c != '\x00':
        name += c
        c = f.read(1)
    # Jump back
    f.seek(a)
    # Return results
    out.name = name
    return out


def print_paths(f, table, child_id):
    f.seek(table.pointers[child_id].address)
    paths = structRead(f, BOMPaths)
    print("\npath id=", child_id)
    print("paths->isLeaf =", paths.isLeaf)
    print("paths->count =", paths.count)
    print("paths->forward =", paths.forward)
    print("paths->backward =", paths.backward)
    paths.indices = []
    for i in range(paths.count):
        j = structRead(f, BOMPathIndices)
        paths.indices.append(j)
        ptr = table.pointers[j.index1]
        b_file = bom_file(f, ptr.address)
        print("path->indices[%s].index0 =" % i, j.index0)
        print("path->indices[%s].index1.parent =" % i, b_file.parent)
        print("path->indices[%s].index1.name =" % i, b_file.name)
    if (paths.isLeaf == 0):
        print_paths(f, table, paths.indices[0].index0)
    if (paths.forward):
        print_paths(f, table, paths.forward)


def print_tree(tree, f, table):
    print("tree->tree =", tree.tree)
    print("tree->version =", tree.version)
    print("tree->child =", tree.child)
    print("tree->blockSize =", tree.blockSize)
    print("tree->pathCount =", tree.pathCount)
    print("tree->unknown3 =", tree.unknown3)
    print_paths(f, table, tree.child)


def dump_bom(filename):
    f = open(filename, 'rb')
    # Load the header
    header = structRead(f, BOMHeader)
    # Next is to load the BOMBlockTable
    f.seek(header.indexOffset)
    table = structRead(f, BOMBlockTable)
    # Now to build up the list of table pointers
    table.pointers = []
    numberOfNonNullEntries = 0
    for i in range(table.numberOfBlockTablePointers):
        p = structRead(f, BOMPointer)
        table.pointers.append(p)
        if p.address != 0:
            numberOfNonNullEntries += 1
    print("Header\n---")
    print("magic =", header.magic)
    print("version =", header.version)
    print("numberOfBlocks =", header.numberOfBlocks)
    print("indexOffset =", header.indexOffset)
    print("indexLength =", header.indexLength)
    print("varsOffset =", header.varsOffset)
    print("varsLength =", header.varsLength)
    print("calculated number of blocks =", numberOfNonNullEntries)
    print("\nIndex Table\n---")
    print("numberOfBlockTableEntries =", table.numberOfBlockTablePointers)
    # Now to build up the table of free list pointers
    free_list_pos = header.indexOffset + sizeof(c_uint32) + (table.numberOfBlockTablePointers * sizeof(BOMPointer))
    f.seek(free_list_pos)
    free_list = structRead(f, BOMFreeList)
    free_list.pointers = []
    for i in range(free_list.numberOfFreeListPointers):
        p = structRead(f, BOMPointer)
        free_list.pointers.append(p)
    print("\nFree List\n---")
    print("numberOfFreeListPointers =", free_list.numberOfFreeListPointers)
    # Time to read the vars
    f.seek(header.varsOffset)
    variables = structRead(f, BOMVars)
    variables.var_list = []
    total_length = 0
    total_length += sizeof(c_uint32)
    var_count = variables.count
    variables.vars = []
    # should now be right up against the first BOMVar
    for i in range(var_count):
        v = structRead(f, BOMVar)
        total_length += sizeof(BOMVar)
        total_length += v.length
        v.name = f.read(v.length)
        variables.vars.append(v)
    print("\nVariables\n---")
    print("vars->count =", var_count)
    print("calculated length =", total_length)
    print('"' + '","'.join([v.name for v in variables.vars]) + '"')
    # Parse the vars
    for v in variables.vars:
        ptr = table.pointers[v.index]
        print("\n" + v.name, "\n---")
        if v.name in ["Paths", "HLIndex", "Size64"]:
            f.seek(ptr.address)
            tree = structRead(f, BOMTree)
            print_tree(tree, f, table)
        elif v.name == "BomInfo":
            f.seek(ptr.address)
            info = structRead(f, BOMInfo)
            info.entries = []
            print("info->version =", info.version)
            print("info->numberOfPaths =", info.numberOfPaths)
            print("info->numberOfInfoEntries =", info.numberOfInfoEntries)
            for i in range(info.numberOfInfoEntries):
                e = structRead(f, BOMInfoEntry)
                info.entries.append(e)
                print("info->entries[%s].unknown0 =" % i, e.unknown0)
                print("info->entries[%s].unknown1 =" % i, e.unknown1)
                print("info->entries[%s].unknown2 =" % i, e.unknown2)
                print("info->entries[%s].unknown3 =" % i, e.unknown3)
        elif v.name == "VIndex":
            f.seek(ptr.address)
            vindex = structRead(f, BOMVIndex)
            print("vindex->unknown0 =", vindex.unknown0)
            print("vindex->indexToVTree =", vindex.indexToVTree)
            print("vindex->unknown2 =", vindex.unknown2)
            print("vindex->unknown3 =", vindex.unknown3)
            print("")
            v_ptr = table.pointers[vindex.indexToVTree]
            f.seek(v_ptr.address)
            tree = structRead(f, BOMTree)
            print_tree(tree, f, table)
    f.close()

if __name__ == '__main__':
    dump_bom('./simple.bom')