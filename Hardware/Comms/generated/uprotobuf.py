a='utf8'
Z='{}({}: {})'
Y=int
X=property
W=enumerate
V=dict
U=Exception
P='<f'
O=True
N=range
K=bytes
J=len
E=staticmethod
C=None
try:import ustruct as H
except ImportError:import struct as H
class L(U):0
class b(U):0
def M(func,*B,**C):
	def A(*D,**E):A=C.copy();A.update(E);return func(*B+D,**A)
	return A
def G(*B,**C):
	def D(cls,type):return type in cls.reverse_mapping
	A=V(((C,A)for(A,C)in W(B)),**C);A['reverse_mapping']=V(((C,B)for(B,C)in A.items()));A['isValid']=classmethod(D);return type('Enum',(object,),A)
A=G(Invalid=-1,Varint=0,Bit64=1,Length=2,Bit32=5)
F=G(Invalid=-1,Optional=1,Required=2,Repeated=3)
class I:
	def __init__(A,id=C,data=C,subType=-1,fieldType=-1,**D):B=fieldType;A._id=id;A._data=data;A._value=[]if B is F.Repeated else C;A._subType=subType;A._fieldType=B
	def reset(A):A._data=C;A._value=[]if A._fieldType is F.Repeated else C
	def isValid(A):
		if not A._fieldType==F.Required:return O
		return A._data!=C and A._value not in(C,[])
	@X
	def id(self):return self._id
	@E
	def type():return A.Invalid
	def data(A):return A._data
	def setData(A,data):
		if A._data==data:return
		A._data=data
	def value(A):return A._value
	def setValue(A,value):
		B=value
		if A._value==B:return
		A._value=B
	def __repr__(A):return Z.format(A.__class__.__name__,A._id,A._value)
	@E
	def encodeZigZag(n,bits=32):return n<<1^n>>bits-1
	@E
	def decodeZigZag(n):return n>>1^-(n&1)
B=G(Int32=1,Int64=2,UInt32=3,UInt64=4,SInt32=5,SInt64=6,Bool=7,Enum=8)
class Q(I):
	def __init__(D,id=C,data=C,subType=-1,fieldType=-1,**C):
		A=subType;super().__init__(id,data,A,fieldType,**C)
		if A==B.Enum:D._enum=C['enum']
	@E
	def type():return A.Varint
	def setData(A,data):
		if A._data==data:return
		A._data=data;C=0
		for (D,E) in W(A._data):C|=(E&127)<<D*7
		if A._subType in(B.SInt32,B.SInt64):C=A.decodeZigZag(C)
		elif A._subType==B.Bool:C=bool(C)
		if A._fieldType==F.Repeated:A._value.append(C)
		else:A._value=C
	def setValue(D,value):
		C=value
		if D._value==C:return
		D._value=C
		if D._subType in(B.SInt32,B.SInt64):C=D.encodeZigZag(C,32 if D._subType==B.SInt32 else 64)
		E=[D._id<<3|A.Varint]
		if D._subType in(B.Int32,B.UInt32,B.SInt32):E.append(C&127|128);C=C>>7;E.append(C&127)
		elif D._subType in(B.Int64,B.UInt64,B.SInt64,B.Enum):
			for F in N(4):
				E.append(C&127);C=C>>7
				if C==0:break
			for F in N(1,J(E)-1):E[F]|=128
		elif D._subType==B.Bool:E.append(Y(C))
		D._data=K(E)
	def __repr__(A):
		if A._subType!=B.Enum:return super().__repr__()
		D=A._enum.reverse_mapping.get(A._value,C);return Z.format(A.__class__.__name__,A._id,D)
R=G(String=1,Message=2,Group=3,Bytes=4)
class S(I):
	@E
	def type():return A.Length
	def setData(A,data):
		if A._data==data:return
		A._data=data
		if A._subType==R.String:B=A._data.decode(a)
		if A._fieldType==F.Repeated:A._value.append(B)
		else:A._value=B
	def setValue(A,value):
		B=value
		if A._value==B:return
		A._value=B;C=[A._id<<3|A.type()];C.append(J(B));A._data=K(C)+K(B,a)
D=G(Fixed64=1,SignedFixed64=2,Double=3,Fixed32=4,SignedFixed32=5,Float=6)
class T(I):
	def __init__(B,id=C,data=C,subType=-1,fieldType=-1,**C):
		A=subType;super().__init__(id,data,A,fieldType,**C)
		if A==D.Float:B._fmt=P
		elif A==D.Double:B._fmt='<d'
		elif A in(D.Fixed32,D.SignedFixed32):B._fmt='<i'
		elif A in(D.Fixed64,D.SignedFixed64):B._fmt='<q'
	def type(B):
		if B._subType in(D.Fixed64,D.SignedFixed64,D.Double):return A.Bit64
		else:return A.Bit32
	def setData(A,data):
		if A._data==data:return
		A._data=data;B=A.decodeFixed(A._data,A._fmt)
		if A._fieldType==F.Repeated:A._value.append(B)
		else:A._value=B
	def setValue(A,value):
		B=value
		if A._value==B:return
		A._value=B;C=K([A._id<<3|A.type()]);A._data=C+A.encodeFixed(B,A._fmt)
	@E
	def encodeFixed(n,fmt=P):return H.pack(fmt,n)
	@E
	def decodeFixed(n,fmt=P):return H.unpack(fmt,n)[0]
class c:
	def __init__(B):
		G='type';E='name';B._fieldsLUT={};B._fields={}
		for C in B._proto_fields:
			if C[G]==A.Varint:D=Q
			elif C[G]==A.Length:D=S
			elif C[G]in(A.Bit32,A.Bit64):D=T
			else:raise L
			B._fieldsLUT[C['id']]=C[E];B._fields[C[E]]=D(**C);F=C[E];setattr(B.__class__,C[E],X(M(B.__get,F),M(B.__set,F)))
		B.fields=B._fields
	@E
	def __get(name,instance):return instance._fields[name]
	@E
	def __set(name,instance,value):instance._fields[name].setValue(value)
	def __iter__(A):return iter(A._fields.keys())
	def reset(A):
		for B in A.values():B.reset()
	def isValid(B):
		for A in B.values():
			if not A.isValid():print('Field {} is not valid!'.format(A.id));return False
		else:return O
	def keys(A):return A._fields.keys()
	def values(A):return A._fields.values()
	def items(A):return A._fields.items()
	def serialize(A):
		B=b''
		for E in N(1,1+J(A._fieldsLUT)):
			F=A._fieldsLUT[E];D=A._fields[F].data()
			if D is not C:B+=D
		return B
	def parse(E,msg):
		D=msg;E.reset();B=0
		while B<J(D):
			H=D[B];type=H&7
			if not A.isValid(type):B+=1;continue
			id=H>>3;I=E._fieldsLUT[id];F=C
			if type==A.Varint:
				F=[]
				while O:
					B+=1;F.append(D[B])
					if not D[B]&128:break
				B+=1
			elif type in(A.Bit32,A.Bit64,A.Length):
				if type==A.Length:B+=1;G=Y(D[B])
				else:G=4 if type==A.Bit32 else 8
				B+=1;F=D[B:B+G];B+=G
			else:raise L
			if I not in E._fields:continue
			E._fields[I].setData(F)
		return E.isValid()