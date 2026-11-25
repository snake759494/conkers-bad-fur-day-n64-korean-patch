import struct
R={n:i for i,n in enumerate('zero at v0 v1 a0 a1 a2 a3 t0 t1 t2 t3 t4 t5 t6 t7 s0 s1 s2 s3 s4 s5 s6 s7 t8 t9 k0 k1 gp sp fp ra'.split())}
class A:
    def __init__(s,base): s.base=base; s.w=[]; s.lab={}; s.fix=[]
    @property
    def pc(s): return s.base+4*len(s.w)
    def L(s,n): s.lab[n]=s.pc
    def i(s,op,rs,rt,imm): s.w.append((op<<26)|(R[rs]<<21)|(R[rt]<<16)|(imm&0xffff))
    def r(s,fn,rs,rt,rd,sa=0): s.w.append((R[rs]<<21)|(R[rt]<<16)|(R[rd]<<11)|(sa<<6)|fn)
    def addiu(s,t,a,imm): s.i(9,a,t,imm)
    def ori(s,t,a,imm): s.i(13,a,t,imm)
    def andi(s,t,a,imm): s.i(12,a,t,imm)
    def slti(s,t,a,imm): s.i(10,a,t,imm)
    def lui(s,t,imm): s.i(15,'zero',t,imm)
    def lw(s,t,off,b): s.i(0x23,b,t,off)
    def lbu(s,t,off,b): s.i(0x24,b,t,off)
    def sw(s,t,off,b): s.i(0x2b,b,t,off)
    def sb(s,t,off,b): s.i(0x28,b,t,off)
    def addu(s,d,a,b): s.r(0x21,a,b,d)
    def subu(s,d,a,b): s.r(0x23,a,b,d)
    def or_(s,d,a,b): s.r(0x25,a,b,d)
    def sll(s,d,t,sa): s.r(0,'zero',t,d,sa)
    def jr(s,a): s.r(8,a,'zero','zero')
    def nop(s): s.w.append(0)
    def move(s,d,a): s.addu(d,a,'zero')
    def j(s,t): s.fix.append((len(s.w),'j',t)); s.w.append(0x08000000)
    def jal(s,t): s.fix.append((len(s.w),'jal',t)); s.w.append(0x0C000000)
    def br(s,op,a,b,t): s.fix.append((len(s.w),'b',t)); s.w.append((op<<26)|(R[a]<<21)|(R[b]<<16))
    def beq(s,a,b,t): s.br(4,a,b,t)
    def bne(s,a,b,t): s.br(5,a,b,t)
    def beqz(s,a,t): s.br(4,a,'zero',t)
    def bnez(s,a,t): s.br(5,a,'zero',t)
    def bytes(s):
        w=list(s.w)
        for idx,k,t in s.fix:
            ta=s.lab[t] if isinstance(t,str) else t
            if k in('j','jal'): w[idx]|=(ta>>2)&0x3ffffff
            else:
                off=(ta-(s.base+4*idx+4))>>2; w[idx]|=off&0xffff
        return b''.join(struct.pack('>I',x) for x in w)
