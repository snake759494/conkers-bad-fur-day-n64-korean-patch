import zlib,struct
d=open("../Conker's Bad Fur Day (USA).z64",'rb').read()
g=d[0x42450:0x19EA88]
key=0x8039CCCA
offs=[];i=1
while True:
    v=struct.unpack('>I',g[i*4:i*4+4])[0]; i+=1
    if v==0: break
    offs.append(v^key)
print(len(offs),[hex(x) for x in offs[:5]],hex(offs[-1]), struct.unpack('>I',g[:4]))
out=b''
sizes=set()
for a,b in zip(offs,offs[1:]):
    c=g[a:b]; r=zlib.decompressobj(-15).decompress(c[4:]); sizes.add(len(r)); out+=r
print(len(out),sizes)
open('code.bin','wb').write(out)
dd=zlib.decompressobj(-15).decompress(g[0x145ED8+4:0x15A388])
print(hex(len(dd))); open('data.bin','wb').write(dd)
