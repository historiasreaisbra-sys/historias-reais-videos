import sys, glob
from PIL import Image
fs = sorted(glob.glob(sys.argv[1] + "/s_*.jpg")); W = 300; H = 533
s = Image.new("RGB", (W * len(fs), H))
for i, f in enumerate(fs): s.paste(Image.open(f).resize((W, H)), (i * W, 0))
s.save(sys.argv[2])
