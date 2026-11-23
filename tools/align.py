"""Alinhamento gratuito (sem STT): usa as pausas do áudio + o texto exato do roteiro.
uso: python3 align.py audio.wav texto.txt saida_words.py
"""
import sys, re, subprocess, numpy as np

audio, txtf, out = sys.argv[1:4]
text = open(txtf, encoding="utf-8").read().strip()
words = text.split()

# --- segmentos de fala pelas pausas
log = subprocess.run(["ffmpeg", "-i", audio, "-af", "silencedetect=noise=-35dB:d=0.16", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio],
                           capture_output=True, text=True).stdout)
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
sil = list(zip(ss, se + [dur] * (len(ss) - len(se))))
segs, cur = [], 0.0
for a, b in sil:
    if a - cur > 0.08: segs.append((cur, a))
    cur = b
if dur - cur > 0.08: segs.append((cur, dur))

# --- unidades = palavras; quebra de segmento preferencialmente após pontuação
phr = [[w] for w in words]
plen = [len(w) + 1 for w in words]
punct = [w[-1] in ".,:?!;" for w in words]
S, P = len(segs), len(phr)
tot_time = sum(b - a for a, b in segs); rate = sum(plen) / tot_time
INF = 1e18
dp = np.full((S + 1, P + 1), INF); bk = np.zeros((S + 1, P + 1), int); dp[0][0] = 0
cum = np.concatenate([[0], np.cumsum(plen)])
for i in range(1, S + 1):
    d = segs[i - 1][1] - segs[i - 1][0]
    for j in range(1, P + 1):
        pen = 0.0 if (punct[j - 1] or j == P) else 0.6
        for k in range(max(0, j - 45), j):
            if dp[i - 1][k] >= INF: continue
            c = cum[j] - cum[k]
            cost = dp[i - 1][k] + (c / rate - d) ** 2 + pen
            if cost < dp[i][j]: dp[i][j] = cost; bk[i][j] = k
    for j in range(0, P + 1):
        v = dp[i - 1][j] + 2 * d ** 2 + 1.0
        if v < dp[i][j]: dp[i][j] = v; bk[i][j] = -1 - j
assign = []; j = P
for i in range(S, 0, -1):
    k = bk[i][j]
    if k < 0: j = -1 - k; continue
    assign.append((i - 1, k, j)); j = k
assign.reverse()

W = []
for si, k, j in assign:
    a, b = segs[si]; ws = [w for p in phr[k:j] for w in p]
    lens = [len(w) + 1 for w in ws]; T = sum(lens); t = a
    for w, L in zip(ws, lens):
        dt = (b - a) * L / T; W.append((w, round(t, 3), round(t + dt * 0.92, 3))); t += dt
assert len(W) == len(words), (len(W), len(words))
open(out, "w").write("W = " + repr(W) + "\n")
print(f"{len(segs)} segmentos, {P} frases, fim {W[-1][2]:.2f}s / {dur:.2f}s")
