#!/usr/bin/env python3
"""名刺に使う部品を作る。

    python3 docs/meishi/build_parts.py

- キャラの PNG（300px 前後）は印刷には粗いので、potrace で輪郭にして SVG にする
- サイトへの QR を SVG で作る
出力は docs/meishi/parts/。
"""
import os
import subprocess
import tempfile

import qrcode
import qrcode.image.svg
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "docs", "meishi", "parts")
INK = "#14110c"
POSES = ["peek", "wave", "cheer", "wink", "think"]


def trace(pose):
    src = os.path.join(REPO, "assets", "images", f"character-{pose}.png")
    im = Image.open(src).convert("RGBA")
    a = im.split()[3]
    # 4倍に拡大してから二値化すると、輪郭がなめらかになる
    a = a.resize((a.width * 4, a.height * 4), Image.LANCZOS)
    bw = a.point(lambda v: 0 if v > 127 else 255, "1")
    with tempfile.TemporaryDirectory() as d:
        bmp = os.path.join(d, "in.bmp")
        bw.save(bmp)
        out = os.path.join(OUT, f"character-{pose}.svg")
        subprocess.run(["potrace", bmp, "-s", "-o", out, "--color", INK,
                        "-t", "8", "-a", "1.1", "-O", "0.4"], check=True)


def qr(url, name):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage,
                      error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    path = os.path.join(OUT, name)
    img.save(path)
    # 色を墨にそろえる
    s = open(path).read().replace('fill="#000000"', f'fill="{INK}"')
    open(path, "w").write(s)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in POSES:
        trace(p)
    qr("https://tsuzukit.com/", "qr-site.svg")
    qr("https://tsuzukit.com/contact/", "qr-contact.svg")  # 裏のお仕事の相談の欄
    print("ok", sorted(os.listdir(OUT)))
