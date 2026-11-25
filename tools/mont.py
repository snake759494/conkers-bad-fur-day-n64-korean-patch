import sys,glob,re,os
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]),key=lambda f:int(re.findall(r'\d+',os.path.basename(f))[-1]))
ims=[Image.open(f).convert('RGB') for f in fs]
w,h=ims[0].size; cols=4; rows=(len(ims)+cols-1)//cols
M=Image.new('RGB',(w*cols,h*rows))
for i,im in enumerate(ims): M.paste(im.resize((w,h)),((i%cols)*w,(i//cols)*h))
M.save(sys.argv[2]); print([os.path.basename(f) for f in fs])
