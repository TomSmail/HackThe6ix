from uprotobuf import *


class LocationrequestMessage(Message):
    _proto_fields=[
    ]

class LocationresponseMessage(Message):
    _proto_fields=[
        dict(name='lat', type=WireType.Bit64, subType=FixedSubType.Double, fieldType=FieldType.Optional, id=1),
        dict(name='lon', type=WireType.Bit64, subType=FixedSubType.Double, fieldType=FieldType.Optional, id=2),
    ]

class InsecticiderequestMessage(Message):
    _proto_fields=[
        dict(name='onOrOff', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
    ]

class InsecticideresponseMessage(Message):
    _proto_fields=[
        dict(name='successful', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
        dict(name='outOfJuice', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=2),
    ]
