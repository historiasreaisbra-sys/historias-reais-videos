"""uso: python3 finish.py narr.(wav|mp3)  -> historias-reais-04-extra-signo-bilionarios.mp4"""
import sys, re, json, subprocess, os
sys.path.insert(0, '/home/claude/historias-reais-videos/tools')
os.chdir('/home/claude/video')
NARR_AUDIO = sys.argv[1]
run = lambda *a: subprocess.run(list(a), check=True)

import importlib, render as R
# 1) texto falado (números por extenso) e alinhamento por pausas
def core(w): return re.sub(r'[^\w,.]', '', w).strip('.,:?')
spoken, counts = [], []
for w in R.words:
    c = core(w); exp = R.SPOKEN.get(c)
    if exp:
        parts = exp.split(); parts[-1] += w[len(w.rstrip('.,:?')):]  # mantém pontuação
        spoken += parts; counts.append(len(parts))
    else:
        spoken.append(w); counts.append(1)
open('texto_falado.txt', 'w').write(' '.join(spoken))
run('ffmpeg', '-y', '-v', 'error', '-i', NARR_AUDIO, '-ar', '48000', '-ac', '1', 'narr.wav')
run('python3', '/home/claude/historias-reais-videos/tools/align.py', 'narr.wav', 'texto_falado.txt', 'words_al.py')
ns = {}; exec(open('words_al.py').read(), ns); WA = ns['W']
T, k = [], 0
for n in counts:
    T.append([WA[k][1], WA[k + n - 1][2]]); k += n
json.dump(T, open('timings.json', 'w'))

# 2) render com tempos reais
importlib.reload(R)
subprocess.run(['python3', 'render.py'], check=True)
NEND = R.NEND; DUR = R.TOTAL
print('narração termina em', NEND, 'vídeo', DUR)

# 3) áudio: narração -14 LUFS + trilha ~22 dB abaixo + limitador
run('ffmpeg', '-y', '-v', 'error', '-i', 'narr.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo', 'n14.wav')
run('ffmpeg', '-y', '-v', 'error', '-i', 'n14.wav', '-i', 'bed.wav', '-filter_complex',
    f'[1:a]aresample=48000,volume=-8dB,atrim=0:{DUR + 3.2}[b];[0:a]apad[n];[n][b]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[a]',
    '-map', '[a]', '-t', f'{DUR + 3.0}', 'mix.wav')

# 4) vídeo principal + título nos 2 s iniciais (1º quadro = capa no feed)
run('ffmpeg', '-y', '-v', 'error', '-i', 'video_sem_narracao.mp4', '-i', 'titulo.png', '-filter_complex',
    "[0:v][1:v]overlay=0:0:enable='lt(t,2)'[v]", '-map', '[v]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', 'main.mp4')

# 5) cartão final 3 s (endcard do kit, com "HOJE ÀS 18H")
import crescimento as C, inspect
src = inspect.getsource(C.endcard).replace("'AMANHÃ ÀS 18H'", "'HOJE ÀS 18H'")
ns2 = vars(C).copy(); exec(src, ns2)
ns2['endcard']('main.mp4', 'SIGNO', 'com o seu signo', 'O urso que destruiu carros era falso', 'cartao.png')
run('ffmpeg', '-y', '-v', 'error', '-loop', '1', '-t', '3', '-i', 'cartao.png', '-vf', 'fade=t=in:d=0.35,fade=t=out:st=2.6:d=0.4,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-r', '30', 'card.mp4')
open('list.txt', 'w').write("file 'main.mp4'\nfile 'card.mp4'\n")
run('ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'vid.mp4')

# 6) whoosh na entrada do cartão + mux
run('ffmpeg', '-y', '-v', 'error', '-i', 'mix.wav', '-i', 'whoosh.wav', '-filter_complex',
    f'[1:a]adelay={int((DUR - 0.3) * 1000)}|{int((DUR - 0.3) * 1000)}[w];[0:a][w]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]', '-map', '[a]', 'mixw.wav')
OUT = 'historias-reais-04-extra-signo-bilionarios.mp4'
run('ffmpeg', '-y', '-v', 'error', '-i', 'vid.mp4', '-i', 'mixw.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT)
print('OK', OUT)
