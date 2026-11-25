import struct
M=0xffffffff
def rol(x,n): return ((x<<n)|(x>>(32-n)))&M
def calc(rom):
    seed=0xDF26F436
    t1=t2=t3=t4=t5=t6=seed
    for i in range(0x1000,0x101000,4):
        d=struct.unpack_from('>I',rom,i)[0]
        if (t6+d)&M<t6: t4=(t4+1)&M
        t6=(t6+d)&M
        t3^=d
        r=rol(d,d&0x1f)
        t5=(t5+r)&M
        if t2>d: t2^=r
        else: t2^=t6^d
        b=struct.unpack_from('>I',rom,0x40+0x0710+(i&0xff))[0]
        t1=(t1+(b^d))&M
    return (t6^t4^t3)&M,(t5^t2^t1)&M
def fix(rom):
    c1,c2=calc(rom); struct.pack_into('>II',rom,0x10,c1,c2)
if __name__=='__main__':
    r=open("../Conker's Bad Fur Day (USA).z64",'rb').read()
    print([hex(x) for x in calc(r)], r[0x10:0x18].hex())
