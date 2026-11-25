from asm import A
BASE=0x151FA140; CUR=0xff0; KFONT=0x80401000; SLOT=0x5D; TEXOFF=SLOT*0xE0
C40=0x15042c40
def build():
    a=A(BASE)
    # KMAP_D: draw. a0=byte t7=ptr, caller frame sp
    a.L('KMAP_D')
    a.andi('t0','a0',0xff); a.slti('at','t0',0x80); a.bnez('at','ORIG'); a.nop()
    a.slti('at','t0',0xa0); a.beqz('at','ORIG'); a.nop()
    a.lbu('t1',1,'t7')
    a.lw('t2',0x90,'sp'); a.addiu('t2','t2',1); a.sw('t2',0x90,'sp')
    a.lw('t2',0x168,'sp'); a.addiu('t2','t2',1); a.sw('t2',0x168,'sp')
    a.j('COMMON'); a.nop()
    # KMAP_M: measure. a0=byte s2=ptr
    a.L('KMAP_M')
    a.andi('t0','a0',0xff); a.slti('at','t0',0x80); a.bnez('at','ORIG'); a.nop()
    a.slti('at','t0',0xa0); a.beqz('at','ORIG'); a.nop()
    a.lbu('t1',1,'s2'); a.addiu('s2','s2',1)
    a.L('COMMON')
    a.addiu('t0','t0',-0x80); a.sll('t0','t0',6); a.addiu('t1','t1',-0xc0); a.or_('t0','t0','t1')
    a.lui('at',0x8040); a.sw('t0',CUR,'at')
    a.lui('at',0x8008); a.lw('t1',0x5994,'at'); a.lui('t2',0x0d0c); a.sw('t2',SLOT*4,'t1')
    a.jr('ra'); a.addiu('v0','zero',SLOT)
    a.L('ORIG'); a.j(C40); a.nop()
    # KTEX: reached by j from 0x15042458; must do lw t9,(a2) and return to 0x15042460
    a.L('KTEX')
    a.lw('t9',0,'a2'); a.ori('at','zero',TEXOFF); a.bne('a3','at','KRET'); a.nop()
    a.lui('at',0x8040); a.lw('t9',CUR,'at')
    a.sll('at','t9',5); a.sll('t9','t9',8); a.subu('t9','t9','at')
    a.lui('at',(KFONT-TEXOFF+0x8000)>>16); a.addiu('at','at',(KFONT-TEXOFF)&0xffff); a.addu('t9','t9','at')
    a.L('KRET'); a.j(0x15042460); a.nop()
    code=a.bytes(); assert len(code)<0xe00
    return code,a.lab
if __name__=='__main__':
    c,l=build(); print(len(c),{k:hex(v) for k,v in l.items()})
