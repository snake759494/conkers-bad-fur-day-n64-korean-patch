import pickle,struct
B=pickle.load(open('all8.pkl','rb'))
def istext(s):
    s=s.rstrip(b'\x00')
    if len(s)<2: return False
    ok=sum((32<=c<127) or c in (10,) or c>=0xa1 for c in s)
    return ok==len(s) and sum(65<=(c|32)<=122 for c in s)>=len(s)*0.4
tot=0;nf=0;files={}
for o,t in B:
    if len(t)<16: continue
    first=struct.unpack('>I',t[:4])[0]
    if first%8 or first<8 or first>len(t) : continue
    n=first//8; ents=[struct.unpack('>II',t[i*8:i*8+8]) for i in range(n)]
    # validate contiguity
    pos=first; ok=True
    for off,sz in ents:
        if off!=pos: ok=False;break
        pos=off+((sz&0xffffff)+7&~7)
    if not ok: continue
    texts=[(i,t[off:off+(sz&0xffffff)]) for i,(off,sz) in enumerate(ents) if istext(t[off:off+(sz&0xffffff)])]
    if texts:
        files[o]=(ents,texts); nf+=1; tot+=sum(len(x) for _,x in texts)
print(nf,tot)
pickle.dump(files,open('lvltext.pkl','wb'))
k=sorted(files)
print([hex(x) for x in k[:5]],[hex(x) for x in k[-5:]])
for o in k[:3]:
    for i,s in files[o][1]: print(hex(o),i,hex(files[o][0][i][1]),s)
