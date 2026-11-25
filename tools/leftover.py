import struct,re
from pack import Table,unrz
d=open("../Conker's Bad Fur Day (Korean).z64",'rb').read()
TBL=0xAB1950
found=[]
for si in range(29):
    o,s=struct.unpack('>II',d[TBL+si*8:TBL+si*8+8]); b=TBL+o; s&=0x7fffffff
    if si in (22,23): continue
    try: S=Table(d[b:b+s],0x7fffffff)
    except Exception: continue
    for ci,c in enumerate(S.items):
        if len(c)<8: continue
        try: C=Table(c)
        except Exception: continue
        for fi,(off,cc) in enumerate(C.e):
            if not (cc>>24)&0x10: continue
            try: raw=unrz(C.items[fi])
            except Exception: continue
            for m in re.finditer(rb'[a-z][a-z \'!?,.\n]{3,}[a-z!?.]',raw):
                t=m.group()
                if t.count(b' ')>=1 and b'\n' in raw[max(0,m.start()-40):m.end()+40] :
                    found.append((si,ci,fi,t))
print(len(found))
for f in found[:80]: print(f)
print('----')
def show(si,ci,fi):
    o,s=struct.unpack('>II',d[TBL+si*8:TBL+si*8+8]); b=TBL+o
    S=Table(d[b:b+(s&0x7fffffff)],0x7fffffff); C=Table(S.items[ci]); raw=unrz(C.items[fi]); T=Table(raw)
    for k,it in enumerate(T.items):
        if re.search(rb'[a-z]{3}',it) and (b'\n' in it or b'\xbd' in it): print(si,ci,fi,k,hex(T.e[k][1]),it)
seen=set()
for si,ci,fi,t in found:
    if (si,ci,fi) not in seen: seen.add((si,ci,fi)); show(si,ci,fi)
