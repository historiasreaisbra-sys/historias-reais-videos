DIA = 11
PALAVRA = "SASHA"
WORDS = "words11"
DIR = "/home/claude/v1/d11"
SC = [
 (0.0, 6.3, "hook", 1.0, 1.16, 0, 0.15),
 (6.3, 11.2, "aerial", 1.0, 1.18, 0, 0),
 (11.2, 14.0, "harbor", 1.0, 1.12, 0, 0),
 (14.0, 16.9, "radio", 1.0, 1.14, 0, 0),
 (16.9, 20.6, "beacon", 1.0, 1.14, 0.2, 0),
 (20.6, 23.2, "aerial", 1.12, 1.25, 0, 0),
 (23.2, 25.8, "cargo", 1.0, 1.14, 0, 0),
 (25.8, 28.7, "cargo", 1.14, 1.26, 0.2, 0.1),
 (28.7, 31.4, "flare", 1.0, 1.15, 0, -0.2),
 (31.4, 33.6, "rescue", 1.0, 1.12, 0, 0),
 (33.6, 34.9, "sunset", 1.0, 1.08, 0, 0),
 (34.9, 38.2, "sleep", 1.0, 1.15, 0, 0.1),
 (38.2, 41.2, "harbor", 1.1, 1.2, 0.2, 0),
 (41.2, 45.0, "sleep", 1.12, 1.24, 0, -0.1),
 (45.0, 99, "hook", 1.06, 1.18, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 6.3:
        H(im, "68 DIAS SEM SINAL", t, 2.0, y=340, color=R.WHITE, size=106)
    elif t < 11.2:
        H(im, "86 ANOS", t, 6.3, y=250, color=R.YEL, size=140)
        S(im, "+ CADELA DE 1 OLHO", t, 9.4, 820, color=R.RED, angle=-6, size=96)
    elif t < 14.0:
        H(im, "SOZINHO DO OREGON", t, 11.2, y=250, color=R.WHITE, size=100)
    elif t < 16.9:
        H(im, "20 DE AGOSTO", t, 14.0, y=250, color=R.YEL, size=110)
        S(im, "RÁDIO MUDO", t, 15.2, 820, color=R.RED, angle=-7, size=120)
    elif t < 20.6:
        H(im, "FIM DE OUTUBRO", t, 16.9, y=250, color=R.WHITE, size=110)
        S(im, "SINAL DE EMERGÊNCIA", t, 18.8, 820, color=R.RED, angle=-6, size=92)
    elif t < 23.2:
        H(im, "400 MILHAS DE SAN DIEGO", t, 20.6, y=250, color=R.YEL, size=84)
    elif t < 25.8:
        H(im, "MAR BRAVO", t, 23.2, y=250, color=R.WHITE, size=130)
    elif t < 28.7:
        H(im, "NENHUMA REAÇÃO", t, 25.8, y=250, color=R.WHITE, size=106)
        S(im, "2 HORAS", t, 27.3, 820, color=R.RED, angle=-7, size=140)
    elif t < 31.4:
        H(im, "UM SINALIZADOR!", t, 28.7, y=250, color=R.YEL, size=110)
    elif t < 33.6:
        H(im, "RESGATE: 14 HORAS", t, 31.4, y=250, color=R.WHITE, size=104)
    elif t < 34.9:
        H(im, "PERDEU O BARCO", t, 33.6, y=250, color=R.WHITE, size=108)
    elif t < 38.2:
        H(im, "NÃO LARGAVA A GUIA", t, 34.9, y=250, color=R.YEL, size=98)
    elif t < 41.2:
        H(im, "FONTE:", t, 38.2, y=250, color=R.WHITE, size=100)
        H(im, "GUARDA COSTEIRA DOS EUA", t, 38.9, y=370, color=R.YEL, size=70)
    else:
        H(im, "VOCÊ SOLTARIA?", t, 41.2, y=260, color=R.YEL, size=110)
        H(im, "AMANHÃ ÀS 18H", t, 45.0, y=410, color=R.WHITE, size=96)
