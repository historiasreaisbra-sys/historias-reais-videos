DIA = 12
PALAVRA = "VOZ"
WORDS = "words12"
DIR = "/home/claude/v1/d12"
SC = [
 (0.0, 7.0, "hook", 1.0, 1.16, 0, 0.15),
 (7.0, 9.5, "office", 1.0, 1.12, 0, 0),
 (9.5, 15.0, "aiwave", 1.0, 1.18, 0, 0),
 (15.0, 17.6, "email", 1.0, 1.14, 0, 0),
 (17.6, 20.6, "hook", 1.12, 1.26, 0, -0.1),
 (20.6, 23.7, "coins", 1.0, 1.15, 0, 0.2),
 (23.7, 25.6, "hospital", 1.0, 1.12, 0, 0),
 (25.6, 27.1, "transfer", 1.0, 1.1, 0, 0),
 (27.1, 29.3, "factory", 1.0, 1.12, 0.2, 0),
 (29.3, 32.6, "coins", 1.14, 1.28, 0, -0.2),
 (32.6, 36.0, "aiwave", 1.12, 1.25, 0.2, 0),
 (36.0, 39.3, "office", 1.1, 1.22, 0, 0.1),
 (39.3, 43.3, "raid", 1.0, 1.15, 0, 0),
 (43.3, 46.8, "court", 1.0, 1.14, 0, 0.1),
 (46.8, 99, "hook", 1.06, 1.18, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 7.0:
        H(im, "A VOZ DO PRESIDENTE", t, 2.0, y=340, color=R.WHITE, size=96)
        S(im, "MILHÕES TRANSFERIDOS", t, 5.2, 820, color=R.RED, angle=-6, size=88)
    elif t < 9.5:
        H(im, "ELE NUNCA LIGOU", t, 7.0, y=250, color=R.YEL, size=112)
    elif t < 15.0:
        H(im, "VOZ CLONADA POR IA", t, 9.5, y=250, color=R.WHITE, size=100)
        S(im, "3 HOMENS", t, 9.5, 820, color=R.RED, angle=-7, size=130)
    elif t < 17.6:
        H(im, "1º: E-MAIL SIGILOSO", t, 15.0, y=250, color=R.WHITE, size=96)
    elif t < 20.6:
        H(im, "2º: A LIGAÇÃO", t, 17.6, y=250, color=R.WHITE, size=112)
        S(im, "VOZ FALSA", t, 19.4, 820, color=R.RED, angle=-7, size=130)
    elif t < 23.7:
        H(im, "VIRAVA CRIPTOMOEDA", t, 20.6, y=250, color=R.YEL, size=100)
    elif t < 25.6:
        H(im, "HOSPITAIS · BANCO", t, 23.7, y=250, color=R.WHITE, size=100)
    elif t < 27.1:
        H(im, "FUNDO DE INVESTIMENTOS", t, 25.6, y=250, color=R.WHITE, size=84)
    elif t < 29.3:
        H(im, "FÁBRICA DE RAÇÃO PET", t, 27.1, y=250, color=R.YEL, size=96)
    elif t < 32.6:
        H(im, "TOTAL:", t, 29.3, y=250, color=R.WHITE, size=110)
        S(im, "US$ 129 MILHÕES", t, 29.8, 820, color=R.RED, angle=-6, size=110)
    elif t < 36.0:
        H(im, "OS APELIDOS...", t, 32.6, y=250, color=R.WHITE, size=110)
    elif t < 39.3:
        H(im, "ROCKY BALBOA", t, 36.0, y=250, color=R.YEL, size=104)
        H(im, "SUPERMAN CASH", t, 37.0, y=370, color=R.YEL, size=104)
        S(im, "FAT BOY", t, 38.3, 820, color=R.RED, angle=-7, size=130)
    elif t < 43.3:
        H(im, "OS 3 FORAM PRESOS", t, 39.3, y=250, color=R.WHITE, size=104)
        S(im, "ATÉ 20 ANOS", t, 41.2, 820, color=R.RED, angle=-6, size=120)
    elif t < 46.8:
        H(im, "FONTE:", t, 43.3, y=250, color=R.WHITE, size=100)
        H(im, "PROMOTORIA DE NY · FBI · AP", t, 43.8, y=370, color=R.YEL, size=68)
    else:
        H(im, "VOCÊ CAIRIA?", t, 46.8, y=260, color=R.YEL, size=110)
        H(im, "AMANHÃ ÀS 18H", t, 49.3, y=410, color=R.WHITE, size=96)
