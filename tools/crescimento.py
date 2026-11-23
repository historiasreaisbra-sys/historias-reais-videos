import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
K=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','fonts')+'/'
if not os.path.exists(K+'Anton-Regular.ttf'): K='/home/claude/kit/fonts/'
Y=(255,204,0); W_=(255,255,255); PURPLE=(48,18,84)
def F(name,size,w=None):
    f=ImageFont.truetype(K+name,size)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
def anton(s): return F('Anton-Regular.ttf',s)
def mont(s,w=800): return F('Montserrat[wght].ttf',s,w)
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t.replace('*',''),font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def rich(d,cx,y,line,f,stroke=6):
    # words wrapped in *..* are yellow
    parts=line.split(' '); total=d.textlength(line.replace('*',''),font=f)
    x=cx-total/2
    for i,p in enumerate(parts):
        col=Y if p.startswith('*') else W_
        t=p.strip('*')+(' ' if i<len(parts)-1 else '')
        d.text((x,y),t,font=f,fill=col,anchor='ls',stroke_width=stroke,stroke_fill=(0,0,0))
        x+=d.textlength(t,font=f)

def title_overlay(title,out):
    """Transparent 1080x1920 PNG: big title for the first 2 s (first frame = feed cover)."""
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=anton(128); lines=wrap(d,title,f,960)
    lh=150; h=lh*len(lines); y0=820-h//2
    band=Image.new('RGBA',(1080,h+120),(0,0,0,150)); im.alpha_composite(band,(0,y0-60))
    for i,l in enumerate(lines): rich(d,540,y0+i*lh+118,l,f)
    im.save(out)

def handle_patch(out):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((1040,112),'@historiasreais.bra',font=mont(38,700),fill=(235,235,235),anchor='rm',stroke_width=2,stroke_fill=(0,0,0))
    im.save(out)

def endcard(video,word,sub,teaser,out):
    subprocess.run(['ffmpeg','-y','-v','error','-sseof','-3.2','-i',video,'-frames:v','1','/tmp/_last.png'],check=True)
    bg=Image.open('/tmp/_last.png').convert('RGB').resize((1080,1920))
    bg=ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(28))).enhance(0.25)
    d=ImageDraw.Draw(bg); cx=540
    def tag(y,txt,f,bgc,fg):
        tw=d.textlength(txt,font=f); d.rectangle([cx-tw/2-26,y,cx+tw/2+26,y+f.size+26],fill=bgc)
        d.text((cx,y+13+f.size/2),txt,font=f,fill=fg,anchor='mm')
    y=380; tag(y,'COMENTA',anton(58),W_,(0,0,0)); y+=110
    fw=anton(200)
    while d.textlength(word,font=fw)>980: fw=anton(fw.size-10)
    d.text((cx,y+fw.size),word,font=fw,fill=Y,anchor='ms',stroke_width=6,stroke_fill=(0,0,0)); y+=fw.size+40
    for l in wrap(d,sub,mont(50,700),940):
        d.text((cx,y),l,font=mont(50,700),fill=W_,anchor='mt'); y+=62
    y+=60; d.line([cx-200,y,cx+200,y],fill=(120,120,120),width=3); y+=50
    tag(y,'AMANHÃ ÀS 18H',anton(50),Y,(0,0,0)); y+=105
    ft=anton(76)
    for l in wrap(d,teaser.upper(),ft,960):
        d.text((cx,y+ft.size),l,font=ft,fill=W_,anchor='ms',stroke_width=3,stroke_fill=(0,0,0)); y+=ft.size+16
    y+=40
    d.text((cx,y),'SEGUE @historiasreais.bra',font=mont(44,800),fill=Y,anchor='mt'); y+=58
    d.text((cx,y),'1 história real por dia até 21/12',font=mont(38,600),fill=(225,225,225),anchor='mt'); y+=50
    assert y<1440, y
    bg.save(out); return y

def cover(img,title,out,dia=None):
    """Capa em série: identidade do canal (preto + vermelho da fechadura + amarelo das legendas)."""
    import numpy as np
    W,H=1080,1920; RED=(214,32,39)
    yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-540)/1.0)**2+((yy-620)/1.3)**2)/1100
    g=np.clip(1-r,0,1)**2
    base=np.stack([10+70*g,6+8*g,6+8*g],-1).astype(np.uint8)
    c=Image.fromarray(base,'RGB'); d=ImageDraw.Draw(c)
    d.rectangle([0,0,W,14],fill=RED)
    src=Image.open(img).convert('RGB'); w=920; h=int(src.height*w/src.width)
    if h>1000:
        ch=int(1000*src.width/w); y0=(src.height-ch)//2; src=src.crop((0,y0,src.width,y0+ch)); h=1000
    src=src.resize((w,h)); mask=Image.new('L',(w,h),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,w,h],36,fill=255)
    top=760; c.paste(src,(80,top),mask)
    d.rounded_rectangle([80,top,80+w,top+h],36,outline=RED,width=8)
    f=anton(120)
    while len(wrap(d,title,f,960))>3: f=anton(f.size-8)
    lines=wrap(d,title,f,960); y=300
    for l in lines: rich(d,540,y+110,l,f,stroke=0); y+=int(f.size*1.12)
    # selo do canal: fechadura vermelha + HISTÓRIAS REAIS
    lab='HISTÓRIAS REAIS'; fl=anton(60); tw=d.textlength(lab,font=fl); cy=top+h+72
    kx=540-tw/2-40
    d.ellipse([kx-17,cy-30,kx+17,cy+4],fill=RED); d.polygon([(kx-12,cy-6),(kx+12,cy-6),(kx+16,cy+30),(kx-16,cy+30)],fill=RED)
    d.text((540+20,cy),lab,font=fl,fill=(255,255,255),anchor='mm')
    if dia: d.text((540,cy+70),f'DIA {dia}/30',font=mont(40,800),fill=Y,anchor='mm')
    c.save(out,quality=92)
