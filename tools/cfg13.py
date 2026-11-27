DIA = 13
PALAVRA = "QUATRO"
WORDS = "words13"
DIR = "/home/claude/v1/d13"
SC = [
 (0.0, 8.7, "hook", 1.0, 1.2, 0, 0.1),
 (8.7, 10.9, "departure", 1.0, 1.12, 0, 0),
 (10.9, 13.2, "islands", 1.0, 1.14, 0, 0),
 (13.2, 15.5, "storm", 1.0, 1.15, 0, 0),
 (15.5, 19.6, "plane", 1.0, 1.15, -0.2, 0),
 (19.6, 21.5, "dusk", 1.0, 1.1, 0, 0),
 (21.5, 24.2, "villagers", 1.0, 1.14, 0, 0),
 (24.2, 29.7, "hands", 1.0, 1.18, 0, 0.1),
 (29.7, 32.9, "empty", 1.0, 1.15, 0, 0),
 (32.9, 35.5, "night", 1.0, 1.14, 0, 0),
 (35.5, 38.5, "hands", 1.14, 1.26, 0.2, 0),
 (38.5, 41.8, "dusk", 1.1, 1.2, 0, 0),
 (41.8, 44.7, "islands", 1.12, 1.24, 0.2, 0),
 (44.7, 99, "hook", 1.06, 1.2, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 8.7:
        H(im, "5.400 KM DE CASA", t, 2.0, y=340, color=R.WHITE, size=110)
        S(im, "VIAGEM DE 1 HORA", t, 5.8, 820, color=R.RED, angle=-6, size=100)
    elif t < 10.9:
        H(im, "9 NUM BARCO DE 6 M", t, 8.7, y=250, color=R.WHITE, size=100)
    elif t < 13.2:
        H(im, "MICRONÉSIA", t, 10.9, y=250, color=R.YEL, size=130)
    elif t < 15.5:
        H(im, "TEMPESTADE", t, 13.2, y=250, color=R.WHITE, size=130)
    elif t < 19.6:
        H(im, "10 DIAS DE BUSCA", t, 15.5, y=250, color=R.WHITE, size=108)
        S(im, "NADA", t, 18.8, 820, color=R.RED, angle=-7, size=150)
    elif t < 21.5:
        H(im, "3 MESES DEPOIS", t, 19.6, y=250, color=R.YEL, size=116)
    elif t < 24.2:
        H(im, "KIRIBATI", t, 21.5, y=250, color=R.WHITE, size=140)
    elif t < 29.7:
        H(im, "5 SOBREVIVENTES", t, 24.2, y=250, color=R.WHITE, size=106)
        S(im, "2 CRIANÇAS", t, 25.8, 820, color=R.YEL, angle=-6, size=120)
    elif t < 32.9:
        H(im, "4 NÃO ESTAVAM MAIS", t, 29.7, y=250, color=R.WHITE, size=96)
        S(im, "A BORDO", t, 32.0, 820, color=R.RED, angle=-7, size=130)
    elif t < 35.5:
        H(im, "NINGUÉM SABE", t, 32.9, y=250, color=R.YEL, size=116)
    elif t < 41.8:
        H(im, "SILÊNCIO", t, 35.5, y=250, color=R.WHITE, size=130)
        S(im, "3 MESES NO OCEANO", t, 39.3, 820, color=R.RED, angle=-6, size=96)
    elif t < 44.7:
        H(im, "FONTE:", t, 41.8, y=250, color=R.WHITE, size=100)
        H(im, "ABC AUSTRÁLIA · EL MUNDO", t, 42.3, y=370, color=R.YEL, size=72)
    else:
        H(im, "E OS OUTROS 4?", t, 44.7, y=260, color=R.YEL, size=110)
        H(im, "AMANHÃ ÀS 18H", t, 48.0, y=410, color=R.WHITE, size=96)
