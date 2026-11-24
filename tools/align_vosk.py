"""Alinhamento forçado grátis com Vosk (modelo pt offline) + texto exato do roteiro.
uso: python3 align_vosk.py audio.wav texto.txt saida_words.py
"""
import sys, json, re, wave, subprocess, unicodedata, difflib
from vosk import Model, KaldiRecognizer, SetLogLevel
SetLogLevel(-1)
audio, txtf, out = sys.argv[1:4]
words = open(txtf, encoding="utf-8").read().split()

def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", w)

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", "/tmp/_a16.wav"], check=True)
wf = wave.open("/tmp/_a16.wav", "rb")
rec = KaldiRecognizer(Model("/opt/vosk/vosk-model-small-pt-0.3"), 16000)
rec.SetWords(True)
hyp = []
while True:
    data = wf.readframes(4000)
    if not data: break
    if rec.AcceptWaveform(data): hyp += json.loads(rec.Result()).get("result", [])
hyp += json.loads(rec.FinalResult()).get("result", [])
H = [norm(h["word"]) for h in hyp]
S = [norm(w) for w in words]

# casa palavras do roteiro com as reconhecidas
sm = difflib.SequenceMatcher(None, S, H, autojunk=False)
anchor = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n): anchor[a + k] = (hyp[b + k]["start"], hyp[b + k]["end"])
# casamento aproximado nas trocas (palavras parecidas)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "replace":
        for i in range(i1, i2):
            best, bj = 0, None
            for j in range(j1, j2):
                r = difflib.SequenceMatcher(None, S[i], H[j]).ratio()
                if r > best: best, bj = r, j
            if bj is not None and best >= 0.6: anchor[i] = (hyp[bj]["start"], hyp[bj]["end"])

# interpola palavras sem âncora (números falados por extenso etc.) pelo tamanho
dur = wf.getnframes() / 16000
W = [None] * len(words); i = 0
while i < len(words):
    if i in anchor:
        W[i] = (words[i], round(anchor[i][0], 3), round(anchor[i][1], 3)); i += 1; continue
    j = i
    while j < len(words) and j not in anchor: j += 1
    t0 = anchor[i - 1][1] if i > 0 and (i - 1) in anchor else (W[i - 1][2] if i > 0 else 0.1)
    t1 = anchor[j][0] if j < len(words) else dur - 0.1
    L = [len(w) + 1 for w in words[i:j]]; T = sum(L); t = t0
    for k, l in zip(range(i, j), L):
        dt = (t1 - t0) * l / T; W[k] = (words[k], round(t, 3), round(t + dt * 0.95, 3)); t += dt
    i = j
open(out, "w").write("W = " + repr(W) + "\n")
print(f"{len(hyp)} reconhecidas, {len(anchor)}/{len(words)} ancoradas, fim {W[-1][2]:.2f}/{dur:.2f}s")
