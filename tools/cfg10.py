DIA = 10
PALAVRA = "DESLIGO"
WORDS = "words10"
DIR = "/home/claude/v1/d10"
SC = [
 (0.0, 11.40, "hook", 1.0, 1.18, 0, 0.15),
 (11.40, 13.38, "town", 1.0, 1.1, 0, 0),
 (13.38, 16.17, "call", 1.0, 1.14, 0, 0),
 (16.17, 21.21, "kitchen", 1.0, 1.16, 0.2, 0),
 (21.21, 25.47, "hang", 1.0, 1.15, 0, 0),
 (25.47, 31.44, "scam", 1.0, 1.16, -0.2, 0),
 (31.44, 38.22, "dispatch", 1.0, 1.15, 0.2, 0),
 (38.22, 40.7, "swat", 1.0, 1.12, 0, 0.2),
 (40.7, 42.24, "living", 1.0, 1.1, 0, 0),
 (42.24, 44.94, "door", 1.0, 1.14, 0, 0),
 (44.94, 48.42, "town", 1.1, 1.2, 0.2, 0),
 (48.42, 99, "hook", 1.06, 1.18, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 11.40:
        H(im, "RECUSOU O GOLPE", t, 2.0, y=340, color=R.WHITE, size=106)
        S(im, "POLÍCIA ARMADA", t, 5.19, 820, color=R.RED, angle=-7, size=110)
    elif t < 13.38:
        H(im, "CANADÁ", t, 11.40, y=250, color=R.YEL, size=140)
    elif t < 16.17:
        H(im, '"SETOR DE FRAUDES"', t, 13.38, y=250, color=R.WHITE, size=100)
    elif t < 21.21:
        H(im, "CARTÃO NO SEU NOME?", t, 16.17, y=250, color=R.WHITE, size=96)
        S(im, "BAIXE O APLICATIVO", t, 18.68, 820, color=R.RED, angle=-6, size=96)
    elif t < 25.47:
        H(im, "ELA DESCONFIA", t, 21.21, y=250, color=R.WHITE, size=110)
        S(im, "LIGA PARA O BANCO", t, 22.59, 820, color=R.YEL, angle=-6, size=100)
    elif t < 31.44:
        H(im, "GOLPISTA FURIOSO", t, 25.47, y=250, color=R.WHITE, size=104)
        S(im, "SURPRESA LÁ FORA", t, 28.65, 820, color=R.RED, angle=-6, size=100)
    elif t < 38.22:
        H(im, "DENÚNCIA FALSA", t, 31.44, y=250, color=R.WHITE, size=110)
        S(im, "3 ARMADOS + REFÉM", t, 34.11, 820, color=R.RED, angle=-6, size=100)
    elif t < 40.7:
        H(im, "POLICIAIS ARMADOS", t, 38.22, y=250, color=R.WHITE, size=100)
    elif t < 42.24:
        H(im, "SÓ ELA. SOZINHA.", t, 40.7, y=250, color=R.YEL, size=110)
    elif t < 44.94:
        H(im, "O NOME DISSO:", t, 42.24, y=250, color=R.WHITE, size=110)
        S(im, "SWATTING", t, 43.89, 820, color=R.RED, angle=-7, size=140)
    elif t < 48.42:
        H(im, "FONTE:", t, 44.94, y=250, color=R.WHITE, size=100)
        H(im, "POLÍCIA MONTADA · GLOBAL NEWS", t, 45.66, y=370, color=R.YEL, size=64)
    else:
        H(im, "VOCÊ DESLIGARIA?", t, 48.42, y=260, color=R.YEL, size=110)
        H(im, "AMANHÃ ÀS 18H", t, 51.60, y=410, color=R.WHITE, size=96)
