DIA = 15
PALAVRA = "QUARTO"
WORDS = "words15"
DIR = "/home/claude/v1/d15"
# v2: voz Algenib (AI Studio), O Exorcista na 1a frase, menina de costas como capa/1o quadro e no loop final
SC = [
 (0.0, 2.5, "girl", 1.0, 1.10, 0, -0.2),
 (2.5, 6.3, "hook", 1.0, 1.22, 0, -0.1),
 (6.3, 8.19, "room", 1.0, 1.14, 0, 0.1),
 (8.19, 10.38, "girl", 1.08, 1.22, 0, -0.3),
 (10.38, 13.59, "priest", 1.0, 1.15, 0.2, 0),
 (13.59, 16.86, "cross", 1.0, 1.16, -0.2, 0.1),
 (16.86, 21.0, "room", 1.05, 1.2, -0.2, 0.2),
 (21.0, 23.16, "camera", 1.0, 1.14, 0.2, 0),
 (23.16, 30.83, "studio", 1.0, 1.15, -0.2, 0),
 (30.83, 35.75, "camera", 1.1, 1.22, 0.3, 0.2),
 (35.75, 38.8, "ruins", 1.0, 1.15, 0.2, 0),
 (38.8, 41.81, "cross", 1.1, 1.22, 0, -0.2),
 (41.81, 44.24, "priest", 1.05, 1.18, -0.2, 0),
 (44.24, 46.73, "studio", 1.0, 1.15, 0.2, 0.1),
 (46.73, 50.03, "ruins", 1.08, 1.2, -0.2, 0),
 (50.03, 99.0, "girl", 1.0, 1.15, 0, -0.1),
]
def overlays(im, t, R):
    raw = t
    t = t if t < 26.62 else (26.62 if t < 29.82 else t - 3.1999999999999997)
    H, S = R.headline, R.stamp
    if t < 6.3:
        H(im, "O EXORCISTA · 1973", t, 2.0, y=340, color=R.WHITE, size=100)
        S(im, "A CASA QUEIMOU", t, 3.2, 820, color=R.RED, angle=-7, size=120)
    elif t < 8.19:
        H(im, "SÓ UM QUARTO SOBROU", t, 6.3, y=250, color=R.YEL, size=96)
    elif t < 10.38:
        H(im, "O QUARTO DA MENINA", t, 8.19, y=250, color=R.WHITE, size=96)
    elif t < 13.59:
        H(im, "O DIRETOR CHAMA UM PADRE", t, 10.38, y=250, color=R.WHITE, size=84)
        S(im, "BENZER O SET", t, 11.5, 820, color=R.RED, angle=-6, size=110)
    elif t < 16.86:
        H(im, "RECUSOU O EXORCISMO", t, 13.59, y=250, color=R.WHITE, size=96)
    elif t < 23.16:
        H(im, "O FRIO ERA REAL", t, 16.86, y=250, color=R.WHITE, size=110)
        S(im, "−29 °C", t, 18.93, 820, color=R.YEL, angle=-6, size=150)
    elif t < 27.63:
        H(im, "ELLEN BURSTYN", t, 23.16, y=250, color=R.WHITE, size=110)
        S(im, "GRITO REAL", t, 24.8, 820, color=R.RED, angle=-7, size=120)
    elif t < 32.55:
        H(im, "COLUNA FERIDA", t, 27.63, y=250, color=R.WHITE, size=110)
    elif t < 38.61:
        H(im, "9 MORTES?", t, 32.55, y=250, color=R.WHITE, size=130)
        S(im, "RELATO, NÃO CONFIRMADO", t, 36.0, 820, color=R.YEL, angle=-5, size=76)
    elif t < 43.53:
        H(im, "QUEM ESPALHOU A MALDIÇÃO?", t, 38.61, y=250, color=R.WHITE, size=80)
        S(im, "O PRÓPRIO DIRETOR", t, 41.2, 820, color=R.RED, angle=-6, size=100)
    elif t < 46.83:
        H(im, "FONTE:", t, 43.53, y=250, color=R.WHITE, size=100)
        H(im, "BRITANNICA · SYFY", t, 44.4, y=370, color=R.YEL, size=70)
    else:
        H(im, "VOCÊ ENTRARIA?", t, 46.83, y=260, color=R.YEL, size=110)
        H(im, "AMANHÃ ÀS 18H", t, 49.2, y=410, color=R.WHITE, size=96)
    if 26.62 <= raw < 29.82:
        H(im, "O GRITO FICOU NO FILME", raw, 26.62 + 0.3, y=370, color=R.YEL, size=80)
