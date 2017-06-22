from ctypes import BigEndianStructure, c_char, c_uint8, c_uint16, c_uint32, sizeof, memmove, addressof


class BOMHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("magic", c_char * 8),
                ("version", c_uint32),
                ("numberOfBlocks", c_uint32),
                ("indexOffset", c_uint32),
                ("indexLength", c_uint32),
                ("varsOffset", c_uint32),
                ("varsLength", c_uint32)]


class BOMPointer(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("address", c_uint32),
                ("length", c_uint32)]


class BOMBlockTable(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("numberOfBlockTablePointers", c_uint32)]


class BOMFreeList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("numberOfFreeListPointers", c_uint32)]


class BOMVars(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("count", c_uint32)]


class BOMVar(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("index", c_uint32),
                ("length", c_uint8)]


class BOMInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("version", c_uint32),
                ("numberOfPaths", c_uint32),
                ("numberOfInfoEntries", c_uint32)]


class BOMInfoEntry(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("unknown0", c_uint32),
                ("unknown1", c_uint32),
                ("unknown2", c_uint32),
                ("unknown3", c_uint32)]


class BOMTree(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("tree", c_char * 4),
                ("version", c_uint32),
                ("child", c_uint32),
                ("blockSize", c_uint32),
                ("pathCount", c_uint32),
                ("unknown3", c_uint8)]


class BOMPaths(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("isLeaf", c_uint16),
                ("count", c_uint16),
                ("forward", c_uint32),
                ("backward", c_uint32)]


class BOMPathIndices(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("index0", c_uint32),
                ("index1", c_uint32)]


class BOMFile(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("parent", c_uint32)]


class BOMVIndex(BigEndianStructure):
    _pack_ = 1
    _fields_ = [("unknown0", c_uint32),
                ("indexToVTree", c_uint32),
                ("unknown2", c_uint32),
                ("unknown3", c_uint8)]

