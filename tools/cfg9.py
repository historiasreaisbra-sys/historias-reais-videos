DIA = 9
PALAVRA = "SINAL"
WORDS = "words9"
DIR = "/home/claude/v1/d9"
SC = [
 (0.0, 9.37, "masks", 1.0, 1.18, 0, 0.15),
 (9.37, 10.71, "hill", 1.0, 1.08, 0, 0),
 (10.71, 13.66, "kite", 1.0, 1.12, 0, -0.2),
 (13.66, 16.11, "bench", 1.0, 1.12, 0.2, 0),
 (16.11, 18.77, "shoes", 1.0, 1.12, 0, 0.2),
 (18.77, 24.21, "note", 1.0, 1.16, 0, 0),
 (24.21, 26.59, "caps", 1.0, 1.12, 0, 0),
 (26.59, 31.03, "masks", 1.1, 1.22, 0.2, 0),
 (31.03, 33.79, "car", 1.0, 1.12, -0.2, 0),
 (33.79, 40.19, "morgue", 1.0, 1.15, 0, 0.1),
 (40.19, 43.75, "sky", 1.0, 1.15, 0, 0),
 (43.75, 48.13, "hill", 1.08, 1.2, 0.2, 0),
 (48.13, 50.58, "note", 1.1, 1.2, 0, 0.2),
 (50.58, 99, "masks", 1.05, 1.18, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 9.37:
        H(im, "MORRO DE NITERÓI", t, 2.0, y=340, color=R.WHITE, size=104)
        S(im, "AGUARDAR SINAL", t, 7.87, 820, color=R.RED, angle=-7, size=110)
    elif t < 10.71:
        H(im, "AGOSTO DE 1966", t, 9.37, y=250, color=R.YEL, size=110)
    elif t < 13.66:
        H(im, "UM MENINO SOLTANDO PIPA", t, 10.71, y=250, color=R.WHITE, size=82)
    elif t < 16.11:
        H(im, "TÉCNICOS EM ELETRÔNICA", t, 13.66, y=250, color=R.WHITE, size=84)
    elif t < 18.77:
        H(im, "TERNO E CAPA DE CHUVA", t, 16.11, y=250, color=R.WHITE, size=86)
    elif t < 24.21:
        H(im, "O BILHETE:", t, 18.77, y=250, color=R.YEL, size=120)
        H(im, "16H30: LOCAL DETERMINADO", t, 21.45, y=390, color=R.WHITE, size=78)
    elif t < 26.59:
        H(im, "18H30:", t, 24.21, y=250, color=R.YEL, size=120)
        S(im, "INGERIR CÁPSULAS", t, 25.18, 820, color=R.RED, angle=-6, size=100)
    elif t < 31.03:
        H(im, "PROTEGER METAIS", t, 27.64, y=250, color=R.WHITE, size=104)
        S(im, "AGUARDAR SINAL", t, 28.86, 820, color=R.RED, angle=-7, size=110)
    elif t < 33.79:
        H(im, "NENHUM FERIMENTO", t, 31.03, y=250, color=R.WHITE, size=100)
        H(im, "NENHUMA LUTA", t, 32.27, y=370, color=R.YEL, size=100)
    elif t < 40.19:
        H(im, "CAUSA DA MORTE", t, 33.79, y=250, color=R.WHITE, size=110)
        S(im, "NUNCA DESCOBERTA", t, 34.9, 820, color=R.RED, angle=-6, size=100)
    elif t < 43.75:
        H(im, "ESPÍRITOS?", t, 40.19, y=250, color=R.WHITE, size=110)
        H(im, "EXTRATERRESTRES?", t, 41.68, y=370, color=R.YEL, size=100)
        H(im, "CRIME?", t, 43.08, y=490, color=R.RED, size=110)
    elif t < 48.13:
        H(im, "QUASE 60 ANOS DEPOIS", t, 43.75, y=250, color=R.WHITE, size=92)
        S(im, "NINGUÉM SABE", t, 45.67, 820, color=R.YEL, angle=-6, size=110)
    elif t < 50.58:
        H(im, "FONTE:", t, 48.13, y=250, color=R.WHITE, size=100)
        H(im, "POLÍCIA DO RIO · LINHA DIRETA", t, 48.71, y=370, color=R.YEL, size=66)
    else:
        H(im, "QUE SINAL?", t, 50.58, y=260, color=R.YEL, size=140)
        H(im, "AMANHÃ ÀS 18H", t, 53.11, y=420, color=R.WHITE, size=96)
