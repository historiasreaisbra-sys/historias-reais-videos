"""Encurta pausas longas (> cap) e aplica atempo. uso: tighten.py in.wav out.wav cap tempo"""
import sys, re, subprocess, numpy as np
from scipy.io import wavfile
src, dst, cap, tempo = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
log = subprocess.run(["ffmpeg", "-i", src, "-af", "silencedetect=noise=-35dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
subprocess.run(["ffmpeg","-y","-v","error","-i",src,"/tmp/_src.wav"],check=True); sr, x = wavfile.read("/tmp/_src.wav")
keep = np.ones(len(x), bool)
for a, b in zip(ss, se):
    if b - a > cap:
        cut0 = a + cap / 2; cut1 = b - cap / 2
        keep[int(cut0 * sr):int(cut1 * sr)] = False
y = x[keep]
wavfile.write("/tmp/_tight.wav", sr, y)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "/tmp/_tight.wav", "-af", f"atempo={tempo}", "-ar", "48000", dst], check=True)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout)
print(dst, round(len(x) / sr, 2), "->", round(d, 2))
