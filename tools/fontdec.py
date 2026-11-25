from PIL import Image
r=open('ram_g1.bin','rb').read()
m=r[0xCBBD0:0xCBBD0+95*4]
def glyph(g):
    w,h=m[g*4],m[g*4+1]; st=(w+7)&~7
    t=bytearray(r[0xC68B0+g*224:0xC68B0+g*224+224])
    px=[[0]*w for _ in range(h)]
    for y in range(h):
        row=t[y*st:(y+1)*st]
        if y&1: row=b''.join(row[i+4:i+8]+row[i:i+4] for i in range(0,st,8))
        for x in range(w): px[y][x]=row[x]
    return px
if __name__=='__main__':
    im=Image.new('L',(20*18,5*18))
    for g in range(95):
        for y,rw in enumerate(glyph(g)):
            for x,v in enumerate(rw): im.putpixel(((g%20)*18+x,(g//20)*18+y),v)
    im.resize((im.width*3,im.height*3),0).save('shots/font.png')
