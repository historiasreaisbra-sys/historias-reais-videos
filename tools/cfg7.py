DIA = 7
PALAVRA = "PILOTO"
WORDS = "words7"
DIR = "/home/claude/v1/d7"
SC = [
 (0.0, 8.16, "hook", 1.0, 1.18, 0, 0.15),
 (8.16, 14.5, "runway", 1.0, 1.14, 0.25, 0),
 (14.5, 19.3, "bag", 1.0, 1.15, 0, 0.2),
 (19.3, 21.75, "cabin", 1.02, 1.14, 0, -0.2),
 (21.75, 25.9, "door", 1.0, 1.16, -0.2, 0),
 (25.9, 30.55, "xpdr", 1.0, 1.15, 0.2, 0),
 (30.55, 33.45, "seat", 1.0, 1.12, -0.2, 0),
 (33.45, 38.25, "gunback", 1.0, 1.15, 0.2, 0),
 (38.25, 39.8, "fuel", 1.05, 1.18, 0, 0),
 (39.8, 45.5, "storm", 1.0, 1.16, -0.2, 0),
 (45.5, 48.2, "runway", 1.1, 1.2, -0.3, 0),
 (48.2, 99, "hook", 1.06, 1.2, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 8.16:
        H(im, "VOO 375 · 1988", t, 2.0, y=340, color=R.WHITE, size=110)
        S(im, "ALVO: PLANALTO", t, 5.84, 820, color=R.RED, angle=-7, size=110)
    elif t < 14.5:
        H(im, "BELO HORIZONTE → RIO", t, 12.96, y=250, color=R.WHITE, size=92)
        S(im, "29/09/1988", t, 11.04, 820, color=R.YEL, angle=-6, size=120)
    elif t < 19.3:
        H(im, "TRATORISTA, 28 ANOS", t, 14.84, y=250, color=R.WHITE, size=100)
        S(im, "REVÓLVER", t, 18.52, 820, color=R.RED, angle=-7, size=130)
    elif t < 21.75:
        H(im, "CULPA O PRESIDENTE", t, 19.44, y=250, color=R.YEL, size=100)
    elif t < 25.9:
        H(im, "TIROS NA CABINE", t, 21.84, y=250, color=R.WHITE, size=110)
        S(im, "2 FERIDOS", t, 24.08, 820, color=R.RED, angle=-6, size=120)
    elif t < 30.55:
        H(im, "CMTE. FERNANDO MURILO", t, 26.24, y=250, color=R.WHITE, size=88)
        S(im, "CÓDIGO DE SEQUESTRO", t, 29.2, 820, color=R.YEL, angle=-6, size=92)
    elif t < 33.45:
        H(im, "O COPILOTO", t, 31.2, y=250, color=R.WHITE, size=120)
        S(im, "MORTO", t, 32.72, 820, color=R.RED, angle=-7, size=140)
    elif t < 38.25:
        H(im, "ARMA NO COMANDANTE", t, 34.0, y=250, color=R.WHITE, size=96)
        S(im, "DESTINO: BRASÍLIA", t, 37.48, 820, color=R.RED, angle=-6, size=100)
    elif t < 39.8:
        H(im, "COMBUSTÍVEL", t, 38.56, y=250, color=R.WHITE, size=120)
        S(im, "NÃO DÁ", t, 39.17, 820, color=R.RED, angle=-7, size=140)
    elif t < 45.5:
        H(im, "E O COMANDANTE...", t, 39.92, y=250, color=R.YEL, size=110)
        S(im, "NINGUÉM FAZ ISSO", t, 41.76, 820, color=R.RED, angle=-6, size=104)
    elif t < 48.2:
        H(im, "FONTE:", t, 45.6, y=250, color=R.WHITE, size=100)
        H(im, "NATIONAL GEOGRAPHIC BRASIL", t, 46.32, y=370, color=R.YEL, size=72)
    else:
        H(im, "PARTE 2", t, 49.52, y=250, color=R.YEL, size=150)
        H(im, "AMANHÃ ÀS 18H", t, 50.56, y=420, color=R.WHITE, size=100)
