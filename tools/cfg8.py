DIA = 8
PALAVRA = "HERÓI"
WORDS = "words8"
DIR = "/home/claude/v1/d8"
SC = [
 (0.0, 7.13, "hook", 1.0, 1.16, 0, 0.1),
 (7.13, 13.88, "cockpit", 1.0, 1.15, 0.2, 0),
 (13.89, 16.77, "hands", 1.0, 1.12, 0, 0.2),
 (16.77, 20.16, "spin", 1.0, 1.18, 0, -0.2),
 (20.16, 22.46, "fighter", 1.0, 1.14, 0.2, 0),
 (22.46, 27.30, "fuel", 1.0, 1.16, 0, 0),
 (27.34, 30.31, "runway", 1.0, 1.14, -0.2, 0),
 (30.31, 33.74, "stairs", 1.0, 1.14, 0, 0.2),
 (33.74, 38.6, "police", 1.0, 1.16, 0.2, 0),
 (38.6, 40.57, "stairs", 1.12, 1.22, 0, -0.2),
 (40.57, 43.05, "seats", 1.0, 1.12, 0, 0),
 (43.05, 46.25, "cockpit", 1.1, 1.2, -0.2, 0),
 (46.25, 99, "hook", 1.06, 1.18, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 7.13:
        H(im, "PARTE 2", t, 2.0, y=340, color=R.YEL, size=140)
        S(im, "VOO 375", t, 3.2, 820, color=R.RED, angle=-7, size=130)
    elif t < 13.88:
        H(im, "PERTO DE GOIÂNIA", t, 7.57, y=250, color=R.WHITE, size=104)
        S(im, "DE CABEÇA PRA BAIXO", t, 12.42, 820, color=R.RED, angle=-6, size=92)
    elif t < 16.77:
        H(im, "PARA DESEQUILIBRAR", t, 13.88, y=250, color=R.WHITE, size=96)
        H(im, "O SEQUESTRADOR", t, 14.6, y=370, color=R.YEL, size=96)
    elif t < 20.16:
        H(im, "PARAFUSO", t, 17.5, y=250, color=R.WHITE, size=130)
        S(im, "QUASE QUEDA LIVRE", t, 18.6, 820, color=R.RED, angle=-6, size=100)
    elif t < 22.46:
        H(im, "UM CAÇA DA FAB", t, 20.16, y=250, color=R.WHITE, size=110)
        H(im, "ASSISTE A TUDO", t, 21.5, y=370, color=R.YEL, size=100)
    elif t < 27.34:
        H(im, "COMBUSTÍVEL", t, 22.46, y=250, color=R.WHITE, size=120)
        S(im, "NÃO CHEGA A BRASÍLIA", t, 25.23, 820, color=R.RED, angle=-6, size=88)
    elif t < 30.31:
        H(im, "POUSO EM GOIÂNIA", t, 27.34, y=250, color=R.WHITE, size=104)
    elif t < 33.74:
        H(im, "AINDA ARMADO", t, 30.31, y=250, color=R.WHITE, size=110)
        S(im, "TRIPULAÇÃO REFÉM", t, 31.9, 820, color=R.RED, angle=-6, size=100)
    elif t < 38.6:
        H(im, "COMANDANTE DE ESCUDO", t, 33.74, y=250, color=R.WHITE, size=88)
        S(im, "3 TIROS DA PF", t, 36.54, 820, color=R.RED, angle=-7, size=120)
    elif t < 40.57:
        H(im, "MORRE 2 DIAS DEPOIS", t, 38.6, y=250, color=R.WHITE, size=96)
    elif t < 43.05:
        H(im, "98 PASSAGEIROS", t, 40.57, y=250, color=R.WHITE, size=110)
        S(im, "SOBREVIVERAM", t, 41.6, 820, color=R.YEL, angle=-6, size=110)
    elif t < 46.25:
        H(im, "FONTE:", t, 43.05, y=250, color=R.WHITE, size=100)
        H(im, "NAT GEO BRASIL · JORNAL OPÇÃO", t, 43.66, y=370, color=R.YEL, size=66)
    else:
        H(im, "HERÓI?", t, 46.25, y=260, color=R.YEL, size=150)
        H(im, "AMANHÃ ÀS 18H", t, 49.7, y=430, color=R.WHITE, size=96)
