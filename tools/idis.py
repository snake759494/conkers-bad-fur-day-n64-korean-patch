import capstone,sys
md=capstone.Cs(capstone.CS_ARCH_MIPS,capstone.CS_MODE_MIPS64+capstone.CS_MODE_BIG_ENDIAN)
d=open("../Conker's Bad Fur Day (USA).z64",'rb').read()
a=int(sys.argv[1],16); n=int(sys.argv[2])
off=a-0x10001000+0x1000
for i in md.disasm(d[off:off+n*4],a): print(hex(i.address),i.mnemonic,i.op_str)
