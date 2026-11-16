import numpy as np, subprocess, wave
from PIL import Image, ImageDraw, ImageFont
import os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=os.path.join(ROOT,"publications","2026-11-visite-marcq")
DUR=12.0; FPS=30; SR=48000

# ---------- music (original, synthesized) ----------
rng=np.random.default_rng(7)
n=int(DUR*SR); L=np.zeros(n); R=np.zeros(n)
beat=0.75  # 80 bpm
def hz(m): return 440*2**((m-69)/12)
def add(buf,start,sig,g=1.0):
    i=int(start*SR); e=min(n,i+len(sig)); buf[i:e]+=sig[:e-i]*g
def keys(m,dur,vel=1.0):
    t=np.arange(int(dur*SR))/SR; f=hz(m)
    s=np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*4)+0.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*7)
    env=(1-np.exp(-t*200))*np.exp(-t*1.6)
    return s*env*vel*(1+0.02*np.sin(2*np.pi*4.5*t))
def bass(m,dur):
    t=np.arange(int(dur*SR))/SR; f=hz(m)
    return (np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t))*(1-np.exp(-t*120))*np.exp(-t*2.2)
def kick():
    t=np.arange(int(0.35*SR))/SR
    return np.sin(2*np.pi*(45*t+ (110/18)*(1-np.exp(-t*18))))*np.exp(-t*9)
def hat():
    t=np.arange(int(0.07*SR))/SR
    x=rng.standard_normal(len(t)); x=np.diff(x,prepend=0)
    return x*np.exp(-t*70)
def snare():
    t=np.arange(int(0.2*SR))/SR
    x=rng.standard_normal(len(t)); x=np.diff(x,prepend=0)
    return (0.6*x+0.5*np.sin(2*np.pi*190*t))*np.exp(-t*22)
chords=[([57,60,64,67],45),([53,57,60,64],41),([60,64,67,71],48),([55,59,62,66],43)]  # Am7 Fmaj7 Cmaj7 Gmaj7
mel=[76,None,72,74, 72,None,69,None, 79,None,76,74, 71,None,74,None]
for b,(ch,bs) in enumerate(chords):
    t0=b*4*beat
    for k,m in enumerate(ch):
        s=keys(m,4*beat,0.5); add(L,t0+k*0.02,s,0.9 if k%2 else 0.6); add(R,t0+k*0.02,s,0.6 if k%2 else 0.9)
    # arpeggio
    for j in range(8):
        m=ch[[0,2,1,3,2,3,1,2][j]]+12
        s=keys(m,0.6,0.28); pan=0.3+0.4*(j%2)
        add(L,t0+j*beat/2+0.005*(j%2),s,1-pan); add(R,t0+j*beat/2+0.005*(j%2),s,pan)
    for j,off in enumerate([0,1.5,2.5]):
        s=bass(bs-12 if False else bs,1.2)*0.8; add(L,t0+off*beat,s); add(R,t0+off*beat,s)
    if b>=1:
        for q in range(4):
            k=kick()*0.9; add(L,t0+q*beat,k) if q in(0,2) else None; add(R,t0+q*beat,k) if q in(0,2) else None
            if q in(1,3): s=snare()*0.22; add(L,t0+q*beat,s); add(R,t0+q*beat,s)
        for j in range(8):
            h=hat()*(0.10 if j%2 else 0.06); add(L,t0+j*beat/2+(0.03 if j%2 else 0),h,0.7); add(R,t0+j*beat/2+(0.03 if j%2 else 0),h,1.0)
for i,m in enumerate(mel):
    if m is None: continue
    s=keys(m+0,1.3,0.42); t0=i*beat
    add(L,t0,s,0.8); add(R,t0,s,0.8); add(L,t0+0.28,s,0.12); add(R,t0+0.21,s,0.2)
mix=np.stack([L,R],1)
# soft lowpass (lofi warmth)
k=np.ones(5)/5
for c in range(2): mix[:,c]=np.convolve(mix[:,c],k,mode="same")
t=np.arange(n)/SR
fade=np.minimum(1,t/0.15)*np.minimum(1,(DUR-t)/2.0)
mix*=fade[:,None]; mix=np.tanh(mix*0.9); mix/=np.abs(mix).max()/0.85
w=wave.open("/tmp/music-reel.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()

# ---------- video ----------
W,H=1080,1920
bg=(24,20,18); accent=(214,120,74); cream=(245,236,224)
src=Image.open(S+"/photo-originale.jpg").convert("RGB")
F="/usr/share/fonts/opentype/inter/"; f=lambda nme,s: ImageFont.truetype(F+nme,s)
PY=560; PW,PH=1080,810
def layer(draw_fn):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); draw_fn(ImageDraw.Draw(im)); return im
x=70
layers=[ # (start, image, slide)
 (0.3, layer(lambda d:d.text((x,255),"VISITE BUSINESS  ·  NOVEMBRE 2026",font=f("Inter-SemiBold.otf",32),fill=accent))),
 (0.8, layer(lambda d:d.text((x,315),"Autour de la table,",font=f("InterDisplay-ExtraBold.otf",92),fill=cream))),
 (1.6, layer(lambda d:d.text((x,420),"on a parlé IA.",font=f("InterDisplay-ExtraBold.otf",92),fill=accent))),
 (3.0, layer(lambda d:(d.text((x,1415),"Marcq-en-Barœul — de belles idées,",font=f("Inter-Regular.otf",38),fill=cream),
                       d.text((x,1467),"et des projets concrets à venir.",font=f("Inter-Regular.otf",38),fill=cream)))),
]
ease=lambda u: 1-(1-min(max(u,0),1))**3
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-i","/tmp/music-reel.wav","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-profile:v","high",
  "-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart","-shortest",S+"/reel-visite-marcq.mp4"],stdin=subprocess.PIPE)
N=int(DUR*FPS)
for i in range(N):
    t=i/FPS
    fr=Image.new("RGB",(W,H),bg)
    z=1.0+0.10*(t/DUR)
    cw,ch=2000/z,1500/z; cx,cy=1000,750
    ph=src.resize((PW,PH),Image.BICUBIC,box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2))
    a=ease(t/0.6)
    if a<1: ph=Image.blend(Image.new("RGB",(PW,PH),bg),ph,a)
    fr.paste(ph,(0,PY))
    d=ImageDraw.Draw(fr)
    bw=int(W*ease((t-0.2)/0.9)); d.rectangle([0,PY+PH,bw,PY+PH+10],fill=accent)
    for st,ly in layers:
        a=ease((t-st)/0.7)
        if a<=0: continue
        off=int((1-a)*30)
        l2=ly if a>=1 else Image.eval(ly.split()[3],lambda v,a=a:int(v*a))
        if a>=1: fr.paste(ly,(0,0),ly)
        else: fr.paste(ly,(0,off),l2)
    # fade out end
    fo=min(1,(DUR-t)/0.5)
    if fo<1: fr=Image.blend(Image.new("RGB",(W,H),bg),fr,max(fo,0))
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
