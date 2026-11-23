"""Render genérico no padrão Flow. Uso:
  python3 render_day.py <cfg_module> stills t1 t2 ...
  python3 render_day.py <cfg_module> chunk k N
O módulo de config (scripts/cfgN.py) define: DIA, PALAVRA, WORDS (módulo), DIR, SC, overlays(im,t,R)
"""
import os, sys, subprocess, importlib
sys.path.insert(0, "/home/claude/v1/scripts")
cfg = importlib.import_module(sys.argv[1])
W = importlib.import_module(cfg.WORDS).W
import render1b as R
from PIL import Image, ImageDraw, ImageEnhance

Wd, Ht, FPS = 1080, 1920, 30
NARR_END = W[-1][2]
TOTAL_OUT = round(NARR_END + 0.25, 2)
R.W = W; R.CHUNKS = R.build_chunks(); R.TOTAL = TOTAL_OUT
OUT = f"{cfg.DIR}/build"; os.makedirs(OUT, exist_ok=True)
IMG = f"{cfg.DIR}/img"

_cache = {}
def base(name, zoom=1.14):
    if name not in _cache:
        im = Image.open(f"{IMG}/{name}.jpg").convert("RGB")
        s = max(Wd * zoom / im.width, Ht * zoom / im.height)
        _cache[name] = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return _cache[name]

def kb(name, u, z0=1.0, z1=1.12, dx=0.0, dy=0.0):
    src = base(name); u = max(0.0, min(1.0, u)); e = u * u * (3 - 2 * u)
    z = z0 + (z1 - z0) * e; cw, ch = Wd / z, Ht / z
    cx = src.width / 2 + dx * (src.width - cw) / 2 * (2 * e - 1)
    cy = src.height / 2 + dy * (src.height - ch) / 2 * (2 * e - 1)
    return src.resize((Wd, Ht), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))

GRAD = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); _g = ImageDraw.Draw(GRAD)
for y in range(Ht):
    a = 0
    if y < 520: a = int(170 * (1 - y / 520) ** 1.4)
    if y > 1080: a = max(a, int(200 * ((y - 1080) / 840) ** 1.2))
    _g.line([(0, y), (Wd, y)], fill=(0, 0, 0, min(a, 220)))
DIM = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 70))

def ia_tag(im):
    d = ImageDraw.Draw(im); f = R.F(R.MONT, 26, 700); s = "RECONSTITUIÇÃO COM IA"
    w = d.textlength(s, font=f); x0, y0 = (Wd - w) / 2 - 18, 196
    d.rounded_rectangle((x0, y0, x0 + w + 36, y0 + 44), radius=22, fill=(0, 0, 0, 150), outline=(255, 255, 255, 90), width=2)
    d.text((x0 + 18, y0 + 8), s, font=f, fill=(235, 235, 235))

def dia_tag(im, t):
    if t >= 3.0: return
    d = ImageDraw.Draw(im); f = R.F(R.ANTON, 44); s = f"DIA {cfg.DIA}/30"
    w = d.textlength(s, font=f); x0 = (Wd - w) / 2 - 22; y0 = 256
    d.rectangle((x0, y0, x0 + w + 44, y0 + 62), fill=R.YEL)
    d.text((x0 + 22, y0 + 4), s, font=f, fill=(11, 11, 12))

def comenta_band(im, t):
    t0 = NARR_END - 3.0
    if t < t0: return
    k = R.ease((t - t0) / 0.3)
    f = R.F(R.ANTON, 92); d0 = ImageDraw.Draw(im)
    a, b = "COMENTA ", cfg.PALAVRA + " ▼"
    try: wa, wb = d0.textlength(a, font=f), d0.textlength(b, font=f)
    except Exception: wa, wb = 400, 400
    tw = wa + wb; h = 140; band = Image.new("RGBA", (int(tw + 80), h), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.rectangle((0, 0, band.width - 1, h - 1), fill=R.YEL + (255,), outline=(0, 0, 0, 255), width=8)
    bd.text((40, 12), a, font=f, fill=(11, 11, 12))
    bd.text((40 + wa, 12), b, font=f, fill=(215, 25, 42))
    sc = 0.6 + 0.4 * k; nw, nh = int(band.width * sc), int(h * sc)
    band = band.resize((nw, nh), Image.LANCZOS)
    im.paste(band, ((Wd - nw) // 2, 1160 - nh // 2), band)

def scene_img(t):
    for (t0, t1, name, z0, z1, dx, dy) in cfg.SC:
        if t < t1:
            u = (t - t0) / min(t1 - t0, 8.0)
            im = kb(name, u, z0, z1, dx=dx, dy=dy).convert("RGBA")
            im.alpha_composite(DIM); im.alpha_composite(GRAD)
            cfg.overlays(im, t, R)
            return im

def frame_out(t, fi):
    im = scene_img(t); ia_tag(im); dia_tag(im, t)
    im = R.finish(im, t, fi).convert("RGB")
    R.chrome(im, min(t, TOTAL_OUT))
    R.captions(im, t)
    im = im.convert("RGBA"); comenta_band(im, t)
    return im.convert("RGB")

def render_chunk(k, N):
    nf = round(TOTAL_OUT * FPS); per = -(-nf // N); f0, f1 = k * per, min(nf, (k + 1) * per)
    tmp, dst = f"{OUT}/c{k}.tmp.mp4", f"{OUT}/c{k}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wd}x{Ht}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for fi in range(f0, f1): p.stdin.write(frame_out(fi / FPS, fi).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, dst)
    else: raise SystemExit("chunk failed")

if __name__ == "__main__":
    if sys.argv[2] == "stills":
        for T in map(float, sys.argv[3:]): frame_out(T, int(T * FPS)).save(f"{OUT}/s_{T:05.2f}.jpg", quality=85)
    elif sys.argv[2] == "total":
        print(TOTAL_OUT)
    else:
        render_chunk(int(sys.argv[3]), int(sys.argv[4]))
