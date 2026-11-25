from PIL import Image,ImageDraw,ImageFont
import sys
FONT='galmuri/Galmuri11-Bold.ttf'
W,H=12,13
TOP=1
def render(ch,size=12):
    f=ImageFont.truetype(FONT,size)
    im=Image.new('L',(W,H),0); dr=ImageDraw.Draw(im); dr.fontmode='1'
    bb=dr.textbbox((0,0),'한',font=f)
    dr.text(((W-(bb[2]-bb[0]))//2-bb[0],TOP-bb[1]),ch,font=f,fill=255)
    return im
def glyph_bytes(im):
    px=im.load(); out=bytearray(224)
    for y in range(H):
        row=bytearray(16)
        for x in range(W): row[x]=min(255,int(px[x,y]*1.15))
        if y&1: row=row[4:8]+row[0:4]+row[12:16]+row[8:12]
        out[y*16:y*16+16]=row
    return bytes(out)
if __name__=='__main__':
    s=sys.argv[1]
    ims=[render(c) for c in s]
    M=Image.new('L',(14*len(s),14))
    for i,im in enumerate(ims): M.paste(im,(i*14+1,1))
    M.resize((M.width*4,M.height*4),0).save('shots/kfont.png')
