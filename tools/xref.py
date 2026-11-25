import struct,sys
c=open('code.bin','rb').read()
for a in sys.argv[1:]:
    t=0x0C000000|((int(a,16)>>2)&0x3ffffff)
    print(a,[hex(0x15000000+i) for i in range(0,len(c),4) if struct.unpack('>I',c[i:i+4])[0]==t])
