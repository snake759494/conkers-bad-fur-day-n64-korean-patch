import struct,zlib,pickle,re,sys
from pack import Table,rz,unrz,pad8
from asm import A
import codepatch,mkfont
SRC="../Conker's Bad Fur Day (USA).z64"
OUT="../Conker's Bad Fur Day (Korean).z64"
rom=bytearray(open(SRC,'rb').read())
TBL=0xAB1950
# ---------- translations ----------
order=pickle.load(open('tr/order.pkl','rb'))
ko={}
for k in range(4):
    for l in open('tr/ko_%d.txt'%k,encoding='utf-8'):
        l=l.rstrip('\n')
        if l.strip(): i,t=l.split('\t',1); ko[int(i)]=t
extra=[]  # other strings (menus) appended later
def collect_chars(texts):
    s=set()
    for t in texts:
        for c in re.sub(r'\{..\}','',t):
            if '\uac00'<=c<='\ud7a3': s.add(c)
    return sorted(s)
import kextra
sys.path.insert(0,'tr'); import ko_extra
allk=list(ko.values())+kextra.all_strings()+list(ko_extra.X.values())
CHARS=collect_chars(allk); CMAP={c:i for i,c in enumerate(CHARS)}
assert len(CHARS)<2048
def enc(t):
    t=re.sub(r'\s*\|\s*','|',t.strip())
    out=bytearray(); i=0
    while i<len(t):
        c=t[i]
        if t.startswith('{',i) and t[i+3:i+4]=='}': out.append(int(t[i+1:i+3],16)); i+=4; continue
        if c=='/': out.append(10)
        elif c=='|': out.append(0xbd)
        elif c in CMAP: k=CMAP[c]; out+=bytes([0x80+(k>>6),0xc0+(k&63)])
        elif 32<=ord(c)<127: out.append(ord(c))
        else: raise ValueError((c,t))
        i+=1
    return bytes(out)
KO={order[i]:enc(t) for i,t in ko.items()}
import importlib.util,sys
sys.path.insert(0,'tr'); import ko_extra
for k,v in ko_extra.X.items(): KO[k]=enc(v)
# ---------- level text (segment 6) ----------
def seginfo(i):
    o,s=struct.unpack('>II',rom[TBL+i*8:TBL+i*8+8]); return TBL+o,s
def istext(s):
    s=s.rstrip(b'\x00')
    if len(s)<2: return False
    ok=sum((32<=c<127) or c==10 or c>=0xa1 for c in s)
    return ok==len(s) and sum(65<=(c|32)<=122 for c in s)>=len(s)*0.4
def patch_levelfile(raw):
    T=Table(raw); ch=0
    for k,it in enumerate(T.items):
        key=it.rstrip(b'\x00')
        if key in KO:
            if True:
                T.items[k]=KO[key]+b'\x00'; ch+=1
    return T.build() if ch else None, ch
def rebuild_segment(si):
    b,s=seginfo(si); seg=bytes(rom[b:b+s]); S=Table(seg,0x7fffffff); total=0
    for ci,cont in enumerate(S.items):
        if len(cont)<8: continue
        try: C=Table(cont)
        except Exception: continue
        changed=False
        for fi,(off,c) in enumerate(C.e):
            if not (c>>24)&0x10: continue
            blob=C.items[fi]
            try: raw=unrz(blob)
            except Exception: continue
            try: new,n=patch_levelfile(raw)
            except Exception: continue
            if new: C.items[fi]=rz(new); changed=True; total+=n
        if changed: S.items[ci]=C.build()
    news=S.build()
    print('seg',si,'strings',total,'size',hex(len(news)),'orig',hex(s))
    return b,s,news
FREE=[0x3F8B800]
def place(si,b,s,news):
    if len(news)<=s:
        rom[b:b+len(news)]=news; rom[b+len(news):b+s]=bytes(s-len(news))
    else:
        nb=FREE[0]; FREE[0]=(nb+len(news)+15)&~15
        rom[nb:nb+len(news)]=news; struct.pack_into('>I',rom,TBL+si*8,nb-TBL)
        v=struct.unpack('>I',rom[TBL+si*8+4:TBL+si*8+8])[0]
        struct.pack_into('>I',rom,TBL+si*8+4,(v&0x80000000)|len(news)); print('relocated seg',si,hex(nb))
for si in (6,26):
    b,s,news=rebuild_segment(si); place(si,b,s,news)
struct.pack_into('>I',rom,TBL+6*8+4,(struct.unpack('>I',rom[TBL+6*8+4:TBL+6*8+8])[0]&0x80000000)|len(news)) if False else None
place(28,*kextra.patch(rom,enc,seginfo))
# ---------- font blob ----------
FROM=(FREE[0]+0xfff)&~0xfff
font=b''.join(mkfont.glyph_bytes(mkfont.render(c)) for c in CHARS)
font=pad8(font)
assert FROM+len(font)<=0x4000000
rom[FROM:FROM+len(font)]=font
print('glyphs',len(CHARS),'font bytes',hex(len(font)))
# ---------- init loader ----------
a=A(0x100226a0)
a.move('s0','ra')
a.lui('a1',FROM>>16); a.ori('a1','a1',FROM&0xffff)
a.lui('a2',0x8040); a.ori('a2','a2',0x1000)
a.lui('a3',len(font)>>16); a.ori('a3','a3',len(font)&0xffff)
a.jal(0x10023850); a.move('a0','zero')
a.L('w'); a.jal(0x100262c0); a.nop(); a.andi('v0','v0',3); a.bnez('v0','w'); a.nop()
a.lui('at',0x8004); a.sb('zero',-0x5a90,'at'); a.sb('zero',-0x5a8f,'at')
a.jr('s0'); a.nop()
ld=a.bytes(); assert len(ld)<=80, len(ld)
def ioff(v): return v-0x10001000+0x1000
rom[ioff(0x100226a0):ioff(0x100226a0)+len(ld)]=ld
h=A(0x100044ec); h.jal(0x100226a0); h.nop(); h.nop(); h.nop()
rom[ioff(0x100044ec):ioff(0x100044ec)+16]=h.bytes()
# ---------- code hooks ----------
rom=codepatch.patch_code(bytes(rom))
# ---------- crc ----------
import crc6105
crc6105.fix(rom)
open(OUT,'wb').write(rom); print('written',OUT)
