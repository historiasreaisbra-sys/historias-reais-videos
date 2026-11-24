DIA = 9
PALAVRA = "SINAL"
WORDS = "words9"
DIR = "/home/claude/v1/d9"
SC = [
 (0.0, 10.71, "masks", 1.0, 1.18, 0, 0.15),
 (10.71, 13.62, "hill", 1.0, 1.1, 0, 0),
 (13.62, 16.11, "kite", 1.0, 1.12, 0, -0.2),
 (16.11, 17.97, "bench", 1.0, 1.1, 0.2, 0),
 (17.97, 20.01, "shoes", 1.0, 1.1, 0, 0.2),
 (20.01, 23.85, "note", 1.0, 1.14, 0, 0),
 (23.85, 26.55, "caps", 1.0, 1.12, 0, 0),
 (26.55, 31.02, "masks", 1.1, 1.22, 0.2, 0),
 (31.02, 33.78, "car", 1.0, 1.12, -0.2, 0),
 (33.78, 40.14, "morgue", 1.0, 1.15, 0, 0.1),
 (40.14, 43.77, "sky", 1.0, 1.15, 0, 0),
 (43.77, 48.12, "hill", 1.08, 1.2, 0.2, 0),
 (48.12, 50.52, "note", 1.1, 1.2, 0, 0.2),
 (50.52, 99, "masks", 1.05, 1.18, 0, -0.2),
]
def overlays(im, t, R):
    H, S = R.headline, R.stamp
    if t < 10.71:
        H(im, "MORRO DE NITERÓI", t, 2.0, y=340, color=R.WHITE, size=104)
        S(im, "AGUARDAR SINAL", t, 9.33, 820, color=R.RED, angle=-7, size=110)
    elif t < 13.62:
        H(im, "AGOSTO DE 1966", t, 10.71, y=250, color=R.YEL, size=110)
    elif t < 16.11:
        H(im, "UM MENINO SOLTANDO PIPA", t, 13.62, y=250, color=R.WHITE, size=82)
    elif t < 17.97:
        H(im, "TÉCNICOS EM ELETRÔNICA", t, 16.11, y=250, color=R.WHITE, size=84)
    elif t < 20.01:
        H(im, "TERNO E CAPA DE CHUVA", t, 17.97, y=250, color=R.WHITE, size=86)
    elif t < 23.85:
        H(im, "O BILHETE:", t, 20.01, y=250, color=R.YEL, size=120)
        H(im, "16H30: LOCAL DETERMINADO", t, 21.09, y=390, color=R.WHITE, size=78)
    elif t < 26.55:
        H(im, "18H30:", t, 23.85, y=250, color=R.YEL, size=120)
        S(im, "INGERIR CÁPSULAS", t, 25.17, 820, color=R.RED, angle=-6, size=100)
    elif t < 31.02:
        H(im, "PROTEGER METAIS", t, 27.60, y=250, color=R.WHITE, size=104)
        S(im, "AGUARDAR SINAL", t, 28.83, 820, color=R.RED, angle=-7, size=110)
    elif t < 33.78:
        H(im, "NENHUM FERIMENTO", t, 31.02, y=250, color=R.WHITE, size=100)
        H(im, "NENHUMA LUTA", t, 32.25, y=370, color=R.YEL, size=100)
    elif t < 40.14:
        H(im, "CAUSA DA MORTE", t, 33.78, y=250, color=R.WHITE, size=110)
        S(im, "NUNCA DESCOBERTA", t, 34.9, 820, color=R.RED, angle=-6, size=100)
    elif t < 43.77:
        H(im, "ESPÍRITOS?", t, 40.14, y=250, color=R.WHITE, size=110)
        H(im, "EXTRATERRESTRES?", t, 41.61, y=370, color=R.YEL, size=100)
        H(im, "CRIME?", t, 43.02, y=490, color=R.RED, size=110)
    elif t < 48.12:
        H(im, "QUASE 60 ANOS DEPOIS", t, 43.77, y=250, color=R.WHITE, size=92)
        S(im, "NINGUÉM SABE", t, 45.66, 820, color=R.YEL, angle=-6, size=110)
    elif t < 50.52:
        H(im, "FONTE:", t, 48.12, y=250, color=R.WHITE, size=100)
        H(im, "POLÍCIA DO RIO · LINHA DIRETA", t, 48.72, y=370, color=R.YEL, size=66)
    else:
        H(im, "QUE SINAL?", t, 50.52, y=260, color=R.YEL, size=140)
        H(im, "AMANHÃ ÀS 18H", t, 53.10, y=420, color=R.WHITE, size=96)
