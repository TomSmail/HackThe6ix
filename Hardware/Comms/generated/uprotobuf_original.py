try: import ustruct as struct
except ImportError: import struct

class UnknownTypeException(Exception): pass
class ValueNotSetException(Exception): pass

def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)
    return _partial

def enum(*sequential, **named):
    def isValid(cls, type):
        return type in cls.reverse_mapping

    enums=dict(((x,i) for i,x in enumerate(sequential)), **named)   
    enums['reverse_mapping']=dict((value,key) for key,value in enums.items())
    enums['isValid']=classmethod(isValid)
    return type('Enum', (object,), enums)

WireType=enum(Invalid=-1, Bit64=1, Bit32=5)
FieldType=enum(Invalid=-1, Optional=1, Required=2, Repeated=3)

class VarType(object):
    def __init__(self, id=None, data=None, subType=-1, fieldType=-1, **kwargs):
        self._id=id
        self._data=data
        self._value=[] if fieldType is FieldType.Repeated else None
        self._subType=subType
        self._fieldType=fieldType

    def reset(self):
        self._data=None
        self._value=[] if self._fieldType is FieldType.Repeated else None

    def isValid(self):
        if not self._fieldType==FieldType.Required: return True
        return self._data!=None and self._value not in (None, [])

    @property
    def id(self): return self._id

    @staticmethod
    def type(): return WireType.Invalid

    def data(self): return self._data

    def setData(self, data):
        if self._data==data: return 
        self._data=data

    def value(self): return self._value

    def setValue(self, value):
        if self._value==value: return
        self._value=value       

    def __repr__(self):
        return "{}({}: {})".format(self.__class__.__name__, self._id, self._value)

    @staticmethod
    def encodeZigZag(n, bits=32): return (n<<1)^(n>>(bits-1))

    @staticmethod
    def decodeZigZag(n): return (n>>1)^-(n&1)


FixedSubType=enum(
    Double=3,
)

class Fixed(VarType):
    def __init__(self, id=None, data=None, subType=-1, fieldType=-1, **kwargs):
        super().__init__(id,data,subType,fieldType,**kwargs)
        if subType==FixedSubType.Float: self._fmt='<f'
        elif subType==FixedSubType.Double: self._fmt='<d'
        elif subType in (FixedSubType.Fixed32, FixedSubType.SignedFixed32): self._fmt="<i"
        elif subType in (FixedSubType.Fixed64, FixedSubType.SignedFixed64): self._fmt="<q"

    def type(self):
        if self._subType in (FixedSubType.Fixed64, FixedSubType.SignedFixed64, FixedSubType.Double):
            return WireType.Bit64
        else: return WireType.Bit32

    def setData(self, data):
        if self._data==data: return
        self._data=data

        value=self.decodeFixed(self._data, self._fmt)
        if self._fieldType==FieldType.Repeated:
            self._value.append(value)
        else: self._value=value

    def setValue(self, value):
        if self._value==value: return
        self._value=value

        data=bytes([(self._id<<3)|self.type()])
        self._data=data+self.encodeFixed(value,self._fmt)

    @staticmethod
    def encodeFixed(n, fmt='<f'): return struct.pack(fmt,n)

    @staticmethod
    def decodeFixed(n, fmt='<f'): return struct.unpack(fmt,n)[0]

class Message(object):
    def __init__(self):

        self._fieldsLUT={}
        self._fields={}
        for field in self._proto_fields:
            if field['type'] in (WireType.Bit32, WireType.Bit64): clazz=Fixed
            else: raise UnknownTypeException

            self._fieldsLUT[field['id']]=field['name']
            self._fields[field['name']]=clazz(**field)

            name=field["name"]
            setattr(self.__class__, field['name'], property(partial(self.__get,name), partial(self.__set,name)))

        self.fields=self._fields

    @staticmethod
    def __get(name, instance):
        return instance._fields[name]

    @staticmethod
    def __set(name, instance, value):
        instance._fields[name].setValue(value)

    def __iter__(self):
       return iter(self._fields.keys())

    def reset(self):
        for field in self.values(): field.reset()

    def isValid(self):
        for field in self.values():
            if not field.isValid():
                print("Field {} is not valid!".format(field.id))
                return False
        else: return True

    def keys(self): return self._fields.keys()

    def values(self): return self._fields.values()

    def items(self): return self._fields.items()

    def serialize(self):
        data=b''
        for i in range(1,1+len(self._fieldsLUT)):
            name=self._fieldsLUT[i]
            d=self._fields[name].data()
            if d is not None: data+=d
        return data

    def parse(self, msg):
        self.reset()
        i=0
        while i<len(msg):
            byte=msg[i]           
            type=byte&0x7
            if not WireType.isValid(type):
                i+=1
                continue

            id=byte>>3
            name=self._fieldsLUT[id]
            data=None

            if type in (WireType.Bit32, WireType.Bit64):
                length=4 if type==WireType.Bit32 else 8

                i+=1
                data=msg[i:i+length]
                i+=length

            else: raise UnknownTypeException

            if name not in self._fields: continue
            self._fields[name].setData(data)
        return self.isValid()
        