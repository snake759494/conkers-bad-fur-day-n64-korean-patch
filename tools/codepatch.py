import struct,zlib
from asm import A
from pack import rz
import kcode
KEY=0x8039CCCA
def patch_code(rom):
    g=bytearray(rom[0x42450:0x19EA88])
    offs=[];i=1
    while True:
        v=struct.unpack('>I',g[i*4:i*4+4])[0]; i+=1
        if v==0: break
        offs.append(v^KEY)
    nent=i  # words incl terminator
    chunks=[bytearray(zlib.decompressobj(-15).decompress(bytes(g[a+4:b]))) for a,b in zip(offs,offs[1:])]
    code=bytearray(b''.join(chunks))
    VB=0x15000000
    def put(addr,data): code[addr-VB:addr-VB+len(data)]=data
    def word(x): return struct.pack('>I',x)
    hk,lab=kcode.build()
    # extend last page
    end=kcode.BASE-VB
    if len(code)<end+len(hk): code+=bytes(end+len(hk)-len(code))
    put(kcode.BASE,hk)
    put(0x15041bd8,word(0x0C000000|((lab['KMAP_D']>>2)&0x3ffffff)))
    put(0x15042968,word(0x0C000000|((lab['KMAP_M']>>2)&0x3ffffff)))
    put(0x15042458,word(0x08000000|((lab['KTEX']>>2)&0x3ffffff)))
    # rechunk
    new=[bytes(code[k:k+4096]) for k in range(0,len(code),4096)]
    assert len(new)==len(chunks)
    out=bytearray(g[:offs[0]]); pos=offs[0]; noffs=[]
    for k,(c,old) in enumerate(zip(new,chunks)):
        noffs.append(pos)
        if c==bytes(old): blob=bytes(g[offs[k]:offs[k+1]])
        else: blob=rz(c)
        out+=blob; pos+=len(blob)
    noffs.append(pos)
    datapos=struct.unpack('>I',g[:4])[0]
    assert pos<=datapos,(hex(pos),hex(datapos))
    out+=bytes(datapos-pos) if False else b''
    # pad with original padding zeros up to data
    out+=bytes(datapos-len(out)); out+=g[datapos:]
    for k,o in enumerate(noffs): out[4+k*4:8+k*4]=struct.pack('>I',o^KEY)
    assert len(out)==len(g)
    r=bytearray(rom); r[0x42450:0x19EA88]=out
    print('code end',hex(pos),'limit',hex(datapos))
    return r
