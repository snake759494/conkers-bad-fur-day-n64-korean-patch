import struct,zlib
def rz(raw):
    co=zlib.compressobj(9,zlib.DEFLATED,-15,9); return struct.pack('>I',len(raw))+co.compress(raw)+co.flush()
def unrz(b): return zlib.decompressobj(-15).decompress(b[4:])
def pad8(b): return b+b'\0'*((-len(b))%8)
class Table:
    """generic (off,flags|size) table, header size = first off"""
    def __init__(s,data,szmask=0xffffff):
        first=struct.unpack('>I',data[:4])[0]; s.n=first//8; s.e=[]
        for i in range(s.n):
            o,c=struct.unpack('>II',data[i*8:i*8+8]); s.e.append([o,c])
        s.data=data; s.m=szmask
        s.items=[data[o:o+(c&szmask)] for o,c in s.e]
    def build(s):
        pos=s.n*8; hdr=b''; body=b''
        for (o,c),it in zip(s.e,s.items):
            sz=len(it)
            hdr+=struct.pack('>II',pos,(c&~s.m)|sz if sz or (c&s.m) else c)
            body+=pad8(it); pos+=len(pad8(it))
        return hdr+body
