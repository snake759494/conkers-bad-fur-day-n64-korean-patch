import struct,zlib
d=open("../Conker's Bad Fur Day (USA).z64",'rb').read()
TBL=0xAB1950
def segs():
    out=[]
    for i in range(0x1d):
        o,s=struct.unpack('>II',d[TBL+i*8:TBL+i*8+8]); out.append((TBL+o,s&0x7fffffff))
    return out
def parse(base,size):
    first=struct.unpack('>I',d[base:base+4])[0]
    n=first//8; ents=[]
    for i in range(n):
        u,c=struct.unpack('>II',d[base+i*8:base+i*8+8]); ents.append((u,c))
    return ents
if __name__=='__main__':
    S=segs()
    for i,(b,s) in enumerate(S): print(i,hex(b),hex(s))
    b,s=S[6]; E=parse(b,s)
    print(len(E)); tot=0;raw=0
    for u,c in E:
        if c>>24 &0x10 and c&0xffffff:
            blob=d[b+u:b+u+(c&0xffffff)]
            r=zlib.decompressobj(-15).decompress(blob[4:])
            co=zlib.compressobj(9,zlib.DEFLATED,-15,9); z=co.compress(r)+co.flush()
            tot+=len(z)+4; raw+=len(blob)
    print(hex(raw),hex(tot))
