import pickle,json
F=pickle.load(open('lvltext.pkl','rb'))
def dec(s):
    o=''
    for c in s:
        if c==10: o+='/'
        elif c==0xbd: o+=' | '
        elif 32<=c<127: o+=chr(c)
        else: o+='{%02x}'%c
    return o
seen={};order=[]
for fo in sorted(F):
    for i,s in F[fo][1]:
        k=s.rstrip(b'\x00')
        if k not in seen: seen[k]=len(order); order.append(k)
lines=[]
for n,k in enumerate(order):
    lines.append('%04d\t%s'%(n,' '.join(dec(k).split())))
open('tr/en.txt','w',encoding='utf-8').write('\n'.join(lines))
pickle.dump(order,open('tr/order.pkl','wb'))
print(len(order))
