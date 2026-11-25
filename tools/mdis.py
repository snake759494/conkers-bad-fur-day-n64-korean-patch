import capstone,sys
c=open('code.bin','rb').read()
md=capstone.Cs(capstone.CS_ARCH_MIPS,capstone.CS_MODE_MIPS64+capstone.CS_MODE_BIG_ENDIAN)
a=int(sys.argv[1],16); n=int(sys.argv[2])
off=a-0x15000000
for i in md.disasm(c[off:off+n*4],a): print(hex(i.address),i.mnemonic,i.op_str)
