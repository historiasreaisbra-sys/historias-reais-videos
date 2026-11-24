"""Render do Short 'Testei o signo de 2.189 bilionários' (Histórias Reais, Dia 13/30).
Uso: python3 render.py [--frames t1,t2,...]  (gera PNGs de checagem)   |  sem args: vídeo completo.
Tempos de legenda: estimados (sem narração). Com timings.json (palavras reais) eles são substituídos."""
import sys, json, math, re, subprocess, os
import numpy as np, pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
CLEAN = False
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
def anton(s): return ImageFont.truetype(f'{F}/Anton-Regular.ttf', s)
def mont(s, w='ExtraBold'):
    f = ImageFont.truetype(f'{F}/Montserrat[wght].ttf', s); f.set_variation_by_name(w); return f

BLACK, RED, ORANGE, GOLD, YELLOW, WHITE, GREY = (8, 6, 6), (214, 40, 30), (245, 110, 20), (222, 170, 60), (255, 214, 0), (255, 255, 255), (150, 140, 135)

# ---------------- dados ----------------
d = pd.read_csv('/home/claude/bilionarios_signos.csv')
signs = d.signo.value_counts()
meds = (d.groupby('signo').finalWorth.median() / 1000).sort_values()
days = {'Áries':31,'Touro':31,'Gêmeos':32,'Câncer':31,'Leão':31,'Virgem':31,'Libra':30,'Escorpião':30,'Sagitário':30,'Capricórnio':29,'Peixes':30,'Aquário':30}
expd = {k: days[k] / sum(days.values()) * signs.sum() for k in days}
viral = [('Libra',32),('Peixes',29),('Touro',27),('Leão',24),('Áries',22),('Virgem',21),('Gêmeos',21),('Aquário',20),('Câncer',20),('Sagitário',20),('Escorpião',17),('Capricórnio',15)]

# ---------------- narração / legendas ----------------
NARR = ("Na lista da Forbes, 375 bilionários nasceram no mesmo dia. Primeiro de janeiro. "
        "Eu achei isso testando aquele vídeo que viralizou dizendo que Libra é o signo que mais faz bilionário. "
        "O ranking tinha 32 librianos no topo e Capricórnio em último, com 15. "
        "Mas era uma amostra de só 268 pessoas. "
        "Então eu peguei a lista completa. E aqueles 375? Não é destino. "
        "É a data que fica no cadastro quando ninguém sabe o aniversário. "
        "Tirei os suspeitos e sobraram 2.189 bilionários. Libra perdeu o primeiro lugar. "
        "Virgem ficou na frente, mas dentro do que o puro acaso produz. "
        "O teste estatístico não achou padrão nenhum. "
        "No dinheiro, a mesma coisa: a mediana de todo signo fica entre 2 e 2,7 bilhões de dólares. "
        "O signo dos bilionários não existe. "
        "Comenta SIGNO com o seu signo. Hoje às 18h: o urso que destruiu carros de luxo era falso.")
SPOKEN = {'375': 'trezentos e setenta e cinco', '32': 'trinta e dois', '15': 'quinze', '268': 'duzentas e sessenta e oito',
          '2.189': 'dois mil cento e oitenta e nove', '2': 'dois', '2,7': 'dois vírgula sete', '18h': 'dezoito horas', '5': 'cinco', '6': 'seis'}
words = NARR.split()
def syl(w):
    core = re.sub(r'[^\w,.]', '', w).strip('.,')
    sp = SPOKEN.get(core, core)
    return max(1, len(re.findall(r'[aeiouáéíóúâêôãõà]+', sp.lower())))
if os.path.exists('timings.json'):
    T = json.load(open('timings.json'))  # [[start,end],...] um por palavra
else:
    T, t = [], 0.35
    for w in words:
        dur = syl(w) / 5.6
        T.append([t, t + dur]); t += dur + (0.32 if w[-1] in '.?:' else 0.12 if w[-1] == ',' else 0.02)
NEND = T[-1][1]
def widx(prefix):  # índice da palavra onde a cena começa
    toks = prefix.split()
    for i in range(len(words)):
        if [re.sub(r'\W', '', x).lower() for x in words[i:i+len(toks)]] == [re.sub(r'\W', '', x).lower() for x in toks]: return i
    raise ValueError(prefix)
def ts(prefix): return T[widx(prefix)][0]
S = dict(A=0, B=ts('Eu achei isso'), C=ts('Mas era uma amostra'), D=ts('Então eu peguei'), E=ts('Tirei os suspeitos'),
         F=ts('O teste estatístico'), G=ts('No dinheiro'), H=ts('O signo dos bilionários'), I=ts('Comenta SIGNO'))
END = NEND + 0.6 + 3.0  # cartão final 3 s
TOTAL = NEND + 0.6
# grupos de legenda (3 palavras, quebra em pontuação)
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(i)
    if len(cur) == 3 or w[-1] in '.?:,': groups.append(cur); cur = []
if cur: groups.append(cur)

# ---------------- utilitários ----------------
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ctext(dr, xy, s, font, fill, stroke=0, sc=(0, 0, 0), anchor='mm'):
    dr.text(xy, s, font=font, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
def bg():
    y, x = np.mgrid[0:H, 0:W]
    g = np.exp(-(((x - W/2) / 700) ** 2 + ((y - 1950) / 650) ** 2))
    g2 = np.exp(-(((x - W/2) / 500) ** 2 + ((y + 150) / 380) ** 2)) * .35
    a = np.zeros((H, W, 3)); a[..., 0] = 8 + 120 * g + 60 * g2; a[..., 1] = 6 + 28 * g + 12 * g2; a[..., 2] = 6 + 8 * g
    return Image.fromarray(a.clip(0, 255).astype('uint8'))
BG = bg()
def keyhole(dr, cx, cy, s, col):
    dr.ellipse([cx - s, cy - s * 1.3, cx + s, cy + s * .7], fill=col)
    dr.polygon([(cx - s * .55, cy), (cx + s * .55, cy), (cx + s * .9, cy + s * 2.1), (cx - s * .9, cy + s * 2.1)], fill=col)
    dr.ellipse([cx - s * .35, cy - s * .55, cx + s * .35, cy + s * .15], fill=BLACK)
    dr.polygon([(cx - s * .18, cy), (cx + s * .18, cy), (cx + s * .3, cy + s * 1.3), (cx - s * .3, cy + s * 1.3)], fill=BLACK)
def chrome(dr, t):
    keyhole(dr, 76, 92, 16, ORANGE)
    dr.text((110, 92), 'HISTÓRIAS REAIS', font=anton(40), fill=WHITE, anchor='lm')
    dr.text((W - 36, 92), '@historiasreais.bra', font=mont(30, 'Bold'), fill=(255, 255, 255, 170), anchor='rm')
    if t < 3.0:
        a = ease(t / .3)
        dr.rounded_rectangle([36, 140, 370, 210], 10, fill=YELLOW)
        dr.text((203, 175), 'EXTRA · DIA 4/30', font=anton(46), fill=BLACK, anchor='mm')
    dr.rounded_rectangle([W - 380, 140, W - 36, 196], 8, outline=GOLD, width=3)
    dr.text((W - 208, 168), 'DADOS REAIS · FORBES', font=mont(24, 'Bold'), fill=GOLD, anchor='mm')
def tape(img, text, y, ang=-4):
    lay = Image.new('RGBA', (1500, 110), (0, 0, 0, 0)); d2 = ImageDraw.Draw(lay)
    d2.rectangle([0, 0, 1500, 110], fill=YELLOW)
    for xx in range(0, 1500, 300): d2.text((xx + 150, 55), text, font=anton(58), fill=BLACK, anchor='mm')
    lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(lay, (W // 2 - lay.width // 2, y - lay.height // 2))
def stamp(img, text, cx, cy, size, col, prog, ang=-12):
    s = 1 + 1.6 * (1 - ease(prog / .25))
    f = anton(int(size * s))
    tmp = Image.new('RGBA', (1400, 700), (0, 0, 0, 0)); d2 = ImageDraw.Draw(tmp)
    bb = d2.textbbox((700, 350), text, font=f, anchor='mm')
    d2.rounded_rectangle([bb[0] - 40, bb[1] - 30, bb[2] + 40, bb[3] + 30], 18, outline=col, width=int(14 * s))
    d2.text((700, 350), text, font=f, fill=col, anchor='mm')
    tmp = tmp.rotate(ang, resample=Image.BICUBIC)
    alpha = int(255 * min(1, prog / .15)); tmp.putalpha(tmp.getchannel('A').point(lambda v: v * alpha // 255))
    img.alpha_composite(tmp, (cx - 700, cy - 350))
def title_overlay(dr, a):
    dr.rectangle([0, 230, W, 560], fill=(0, 0, 0))
    dr.rectangle([0, 230, W, 246], fill=RED)
    f = anton(108)
    l1, l2a, l2b = 'TESTEI O SIGNO DE', '2.189', ' BILIONÁRIOS'
    ctext(dr, (W // 2, 330), l1, f, WHITE)
    w1 = dr.textlength(l2a, font=f); w2 = dr.textlength(l2b, font=f); x0 = W // 2 - (w1 + w2) / 2
    dr.text((x0, 470), l2a, font=f, fill=YELLOW, anchor='lm'); dr.text((x0 + w1, 470), l2b, font=f, fill=WHITE, anchor='lm')

# ---------------- cenas ----------------
def scene_A(img, dr, t):
    # calendário 1º JAN + contador
    cx, top = W // 2, 640 if t < 2.0 else 330
    if t >= 2.0: top = 330 + (640 - 330) * (1 - ease((t - 2.0) / .4))
    dr.rounded_rectangle([cx - 260, top, cx + 260, top + 560], 30, fill=(245, 240, 232))
    dr.rounded_rectangle([cx - 260, top, cx + 260, top + 150], 30, fill=RED); dr.rectangle([cx - 260, top + 110, cx + 260, top + 150], fill=RED)
    for k in (-150, 150): dr.rounded_rectangle([cx + k - 16, top - 40, cx + k + 16, top + 40], 10, fill=(60, 55, 50))
    ctext(dr, (cx, top + 78), 'JANEIRO', anton(80), WHITE)
    ctext(dr, (cx, top + 350), '1', anton(330), (25, 20, 20))
    if t >= 2.0:
        n = int(375 * ease((t - 2.0) / 2.0))
        ctext(dr, (cx, top + 700), f'{n}', anton(190), YELLOW, 6)
        ctext(dr, (cx, top + 830), 'BILIONÁRIOS NO MESMO DIA', mont(44), WHITE, 4)
def scene_B(img, dr, t, t0):
    p = t - t0
    ctext(dr, (W // 2, 300), 'O RANKING QUE VIRALIZOU', anton(76), WHITE)
    ctext(dr, (W // 2, 370), 'top 300 da Forbes 2022 · 268 com data', mont(32, 'SemiBold'), GREY)
    for i, (s, n) in enumerate(viral):
        a = ease((p - .15 * i) / .4)
        if a <= 0: continue
        y = 440 + i * 52; hl = s in ('Libra', 'Capricórnio')
        col = YELLOW if s == 'Libra' else RED if s == 'Capricórnio' else WHITE
        dr.text((140, y), f'{i+1}º', font=mont(36), fill=GREY, anchor='lm')
        dr.text((230, y), s, font=mont(40 if hl else 36), fill=col, anchor='lm')
        bw = int(420 * n / 32 * a)
        dr.rounded_rectangle([560, y - 16, 560 + max(bw, 8), y + 16], 6, fill=col if hl else (110, 100, 95))
        dr.text((560 + bw + 18, y), str(n), font=mont(36), fill=col, anchor='lm')
def scene_C(img, dr, t, t0):
    p = t - t0
    ctext(dr, (W // 2, 320), 'A AMOSTRA ERA PEQUENA', anton(80), WHITE)
    for k, (lab, n, col) in enumerate([('no vídeo viral', 268, RED), ('na lista completa', 2564, GOLD)]):
        a = ease((p - .3 - .8 * k) / .8); y = 520 + k * 260
        dr.text((120, y - 70), lab, font=mont(40, 'Bold'), fill=WHITE, anchor='lm')
        bw = int(820 * n / 2564 * a); dr.rounded_rectangle([120, y - 30, 120 + max(bw, 10), y + 60], 10, fill=col)
        dr.text((140 + bw, y + 15), f'{int(n * a):,}'.replace(',', '.'), font=anton(80), fill=WHITE, anchor='lm', stroke_width=3, stroke_fill=BLACK)
def scene_D(img, dr, t, t0):
    p = t - t0
    ctext(dr, (W // 2, 320), 'O MISTÉRIO DO 1º DE JANEIRO', anton(72), WHITE)
    base = 1000; cols = [('um dia\nqualquer', 7, GREY), ('1º de\njaneiro', 375, RED)]
    for k, (lab, n, col) in enumerate(cols):
        a = ease((p - .3 - .5 * k) / 1.0); x = 330 + k * 420
        hgt = int(440 * n / 375 * a)
        dr.rounded_rectangle([x - 110, base - max(hgt, 6), x + 110, base], 10, fill=col)
        dr.text((x, base - hgt - 50), f'{int(n * a) if k else n}', font=anton(90), fill=WHITE, anchor='mm')
        dr.multiline_text((x, base + 70), lab, font=mont(38, 'Bold'), fill=WHITE, anchor='mm', align='center')
    if p > 3.2: stamp(img, 'DATA DE CADASTRO', W // 2, 640, 78, YELLOW, p - 3.2, ang=-8)
def scene_E(img, dr, t, t0):
    p = t - t0
    n = int(2189 * ease(p / 1.4))
    ctext(dr, (W // 2, 320), f'{n:,}'.replace(',', '.') + ' BILIONÁRIOS', anton(86), YELLOW)
    ctext(dr, (W // 2, 392), 'contagem real × esperado pelo acaso (linha)', mont(32, 'SemiBold'), GREY)
    order = signs.index.tolist()
    for i, s in enumerate(order):
        a = ease((p - 1.0 - .08 * i) / .5)
        if a <= 0: continue
        y = 460 + i * 50; n = signs[s]
        col = GOLD if s == 'Virgem' else YELLOW if s == 'Libra' else (150, 140, 135)
        dr.text((110, y), s, font=mont(36, 'Bold'), fill=WHITE if s not in ('Virgem', 'Libra') else col, anchor='lm')
        x0 = 400; sc = 560 / 230
        dr.rounded_rectangle([x0, y - 15, x0 + int(n * sc * a), y + 15], 6, fill=col)
        ex = x0 + int(expd[s] * sc); dr.line([ex, y - 22, ex, y + 22], fill=WHITE, width=4)
        dr.text((x0 + int(n * sc * a) + 14, y), str(n), font=mont(32), fill=WHITE, anchor='lm')
def scene_F(img, dr, t, t0):
    p = t - t0
    ctext(dr, (W // 2, 320), 'QUANTO CADA SIGNO FOGE DO ACASO', anton(64), WHITE)
    crit = 2.87; cx = W // 2; sc = 150
    dr.rectangle([cx - crit * sc, 390, cx + crit * sc, 1010], fill=(40, 28, 24))
    for v in (-crit, crit): dr.line([cx + v * sc, 390, cx + v * sc, 1010], fill=ORANGE, width=5)
    dr.text((cx + crit * sc - 10, 1030), 'limite', font=mont(30, 'Bold'), fill=ORANGE, anchor='rm')
    res = {s: (signs[s] - expd[s]) / math.sqrt(expd[s]) for s in signs.index}
    for i, (s, r) in enumerate(sorted(res.items(), key=lambda x: -x[1])):
        a = ease((p - .2 - .07 * i) / .5); y = 420 + i * 49
        dr.text((cx - 470, y), s, font=mont(30, 'Bold'), fill=WHITE, anchor='lm') if False else None
        x1 = cx + r * sc * a
        dr.rounded_rectangle([min(cx, x1), y - 14, max(cx, x1), y + 14], 5, fill=GOLD if r > 0 else (140, 110, 90))
        dr.text((cx + (-20 if r > 0 else 20), y), s, font=mont(28, 'Bold'), fill=WHITE, anchor='rm' if r > 0 else 'lm')
    dr.line([cx, 390, cx, 1010], fill=WHITE, width=2)
    if p > 1.6: stamp(img, 'p = 0,37 · SEM PADRÃO', W // 2, 1110, 64, YELLOW, p - 1.6, ang=-5)
def scene_G(img, dr, t, t0):
    p = t - t0
    ctext(dr, (W // 2, 320), 'PATRIMÔNIO MEDIANO POR SIGNO', anton(70), WHITE)
    ctext(dr, (W // 2, 392), 'em bilhões de dólares', mont(32, 'SemiBold'), GREY)
    x0, x1, lo, hi = 420, 960, 1.5, 3.0
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    for v in (1.5, 2.0, 2.5, 3.0):
        dr.line([X(v), 440, X(v), 1040], fill=(60, 50, 46), width=2); dr.text((X(v), 1070), f'{v:.1f}'.replace('.', ','), font=mont(30, 'Bold'), fill=GREY, anchor='mm')
    for i, (s, m) in enumerate(meds.sort_values(ascending=False).items()):
        a = ease((p - .2 - .06 * i) / .5); y = 470 + i * 48
        dr.text((x0 - 30, y), s, font=mont(32, 'Bold'), fill=WHITE, anchor='rm')
        xx = X(lo + (m - lo) * a); dr.line([x0, y, xx, y], fill=(110, 80, 60), width=4)
        dr.ellipse([xx - 15, y - 15, xx + 15, y + 15], fill=YELLOW)
        if a >= 1: dr.text((xx + 26, y), f'{m:.1f}'.replace('.', ','), font=mont(28, 'Bold'), fill=WHITE, anchor='lm')
def scene_H(img, dr, t, t0):
    p = t - t0
    ctext(dr, (W // 2, 420), 'O SIGNO DOS', anton(110), WHITE); ctext(dr, (W // 2, 550), 'BILIONÁRIOS', anton(110), WHITE)
    stamp(img, 'NÃO EXISTE', W // 2, 790, 150, RED, p, ang=-10)
def comenta_strip(img, dr, p):
    a = ease(p / .3); y0 = 1090 + int(60 * (1 - a))
    dr.rounded_rectangle([90, y0, W - 90, y0 + 140], 18, fill=YELLOW, outline=BLACK, width=8)
    f = anton(84); a1, a2 = 'COMENTA ', 'SIGNO ▼'
    w1 = dr.textlength(a1, font=f); w2 = dr.textlength('SIGNO', font=f) + dr.textlength(' ▼', font=mont(70))
    x = W / 2 - (w1 + w2) / 2
    dr.text((x, y0 + 70), a1, font=f, fill=BLACK, anchor='lm'); dr.text((x + w1, y0 + 70), 'SIGNO', font=f, fill=RED, anchor='lm')
    dr.text((x + w1 + dr.textlength('SIGNO', font=f) + 14, y0 + 74), '▼', font=mont(64), fill=BLACK, anchor='lm')
def captions(dr, t):
    for g in groups:
        if T[g[0]][0] - .05 <= t <= T[g[-1]][1] + .25:
            f = mont(66); toks = [words[i].strip(',.:?') if words[i] not in ('2,7',) else words[i] for i in g]
            toks = [w.upper() for w in toks]
            tw = sum(dr.textlength(w, font=f) for w in toks) + 22 * (len(toks) - 1); x = W / 2 - tw / 2
            for i, w in zip(g, toks):
                on = T[i][0] <= t <= T[i][1] + .08
                dr.text((x, 1400), w, font=f, fill=YELLOW if on else WHITE, anchor='lm', stroke_width=8, stroke_fill=BLACK)
                x += dr.textlength(w, font=f) + 22
            break
def endcard(img, dr, p):
    dr.rectangle([0, 0, W, H], fill=BLACK)
    img.paste(BG, (0, 0))
    keyhole(dr, W // 2, 300, 60, ORANGE)
    ctext(dr, (W // 2, 520), 'HISTÓRIAS REAIS', anton(100), WHITE)
    comenta_strip(img, dr, 1.0)
    dr.rounded_rectangle([90, 700, W - 90, 1000], 20, outline=GOLD, width=4)
    ctext(dr, (W // 2, 775), 'AMANHÃ ÀS 18H', anton(80), YELLOW)
    ctext(dr, (W // 2, 900), 'Caso brasileiro em 2 partes', mont(50), WHITE)
    ctext(dr, (W // 2, 1320), 'SEGUE @historiasreais.bra', mont(54), WHITE)
    ctext(dr, (W // 2, 1400), '1 história real por dia até 21/12', mont(40, 'SemiBold'), GREY)

def frame(t):
    img = BG.copy().convert('RGBA'); dr = ImageDraw.Draw(img)
    keys = list(S.items())
    cur = max([k for k in keys if k[1] <= t], key=lambda k: k[1])
    k, t0 = cur
    if k in ('A',): scene_A(img, dr, t)
    elif k == 'B': scene_B(img, dr, t, t0)
    elif k == 'C': scene_C(img, dr, t, t0)
    elif k == 'D': scene_D(img, dr, t, t0)
    elif k == 'E': scene_E(img, dr, t, t0)
    elif k == 'F': scene_F(img, dr, t, t0)
    elif k == 'G': scene_G(img, dr, t, t0)
    elif k in ('H', 'I'): scene_H(img, dr, t, S['H'])
    if t >= NEND - 3.0: comenta_strip(img, dr, t - (NEND - 3.0))
    if not CLEAN: chrome(dr, t); captions(dr, t)
    # fade de entrada de cena
    fade = t - t0 if k != 'A' else 1
    if fade < .2:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - fade / .2) * .8))); img.alpha_composite(ov)
    return img

if __name__ == '__main__':
    print('duração', round(TOTAL, 1), 'narração', round(NEND, 1), {k: round(v, 1) for k, v in S.items()})
    if len(sys.argv) > 2 and sys.argv[1] == '--frames':
        for tt in sys.argv[2].split(','):
            frame(float(tt)).convert('RGB').save(f'chk_{tt}.png')
    else:
        n = int(TOTAL * FPS)
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', 'video_sem_narracao.mp4'], stdin=subprocess.PIPE)
        for i in range(n): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
        p.stdin.close(); p.wait(); print('ok')
