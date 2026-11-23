import json, base64, sys, os
from PIL import Image
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
d = json.load(open(src)); ims = []
for k, v in sorted(d.items()):
    p = f"{outdir}/{k}.jpg"; open(p, "wb").write(base64.b64decode(v["data"]))
    ims.append(Image.open(p).convert("RGB").resize((192, 344)))
cols = 6; rows = -(-len(ims) // cols)
s = Image.new("RGB", (192 * cols, 344 * rows))
for i, im in enumerate(ims): s.paste(im, ((i % cols) * 192, (i // cols) * 344))
s.save(f"{outdir}/sheet.jpg"); print(len(ims))
