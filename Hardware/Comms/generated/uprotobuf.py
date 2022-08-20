try: import ustruct as struct
except ImportError: import struct

import functions.partial
#import VarType
#import Fixed
i#mport Message

class UnknownTypeException(Exception): pass
class ValueNotSetException(Exception): pass

WireType=enum(Invalid=-1, Bit64=1, Bit32=5)
FieldType=enum(Invalid=-1, Optional=1, Required=2, Repeated=3)

