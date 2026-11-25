import sys,subprocess,numpy as np
from scipy.io import wavfile
narr,scr,out,t0=sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4])
sr=48000
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).copy()
n=load(narr); s=load(scr)
s=s/ (np.abs(s).max()+1e-9)*0.9
L=len(s); i0=int(t0*sr)
g=np.ones(len(n),dtype=np.float32)
att=int(.05*sr); rel=int(.3*sr); end=min(len(n),i0+L)
g[i0:end]=0.2
g[max(0,i0-att):i0]=np.linspace(1,0.2,min(att,i0))
g[end:end+rel]=np.linspace(0.2,1,len(g[end:end+rel]))
m=n*g
if i0+L>len(m): m=np.concatenate([m,np.zeros(i0+L-len(m),dtype=np.float32)])
m[i0:i0+L]+=s
m=m/np.abs(m).max()*0.95
wavfile.write(out,sr,(m*32767).astype(np.int16))
