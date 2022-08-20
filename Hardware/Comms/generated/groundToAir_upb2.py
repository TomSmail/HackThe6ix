try: import ustruct as struct
except ImportError: import struct

from functions import partial, enum
from VarType import VarType
#import Fixed
#i#mport Message

class UnknownTypeException(Exception): pass
class ValueNotSetException(Exception): pass

WireType=enum(Invalid=-1, Bit64=1, Bit32=5)
FieldType=enum(Invalid=-1, Optional=1, Required=2, Repeated=3)


# class LocationrequestMessage(Message):
#     _proto_fields=[
#     ]

class LocationresponseMessage(Message):
    _proto_fields=[
        dict(name='lat', type=WireType.Bit64, subType=FixedSubType.Double, fieldType=FieldType.Optional, id=1),
        dict(name='lon', type=WireType.Bit64, subType=FixedSubType.Double, fieldType=FieldType.Optional, id=2),
    ]

# class InsecticiderequestMessage(Message):
#     _proto_fields=[
#         dict(name='onOrOff', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
#     ]

# class InsecticideresponseMessage(Message):
#     _proto_fields=[
#         dict(name='successful', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
#         dict(name='outOfJuice', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=2),
#     ]
