#!/usr/bin/env python3
"""走っているキャラからファビコン一式を作る。

    python3 docs/character/build_favicon.py

16pxだけは目が1px未満になって顔が消えるので、この大きさ用に目の穴だけ広げる。
体の形はいじらない。32px以上は絵をそのまま縮めるだけ。
"""
import os
import subprocess
from collections import deque

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "assets", "images", "character-run.png")
ICONS = os.path.join(REPO, "assets", "icons")
CREAM = (246, 242, 234)


def eye_holes(alpha):
    """外につながっていない透明の島＝目 のマスクを返す"""
    solid = alpha > 128
    h, w = solid.shape
    outside = np.zeros_like(solid)
    q = deque()

    def push(y, x):
        if not solid[y, x] and not outside[y, x]:
            outside[y, x] = True
            q.append((y, x))

    for x in range(w):
        push(0, x)
        push(h - 1, x)
    for y in range(h):
        push(y, 0)
        push(y, w - 1)
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                push(ny, nx)
    return (~solid) & (~outside)


def widen_eyes(img, grow):
    """目の穴だけを grow px ぶん太らせる。小さく縮めても顔が残るように"""
    a = np.array(img)[:, :, 3].copy()
    holes = eye_holes(a)
    if not holes.any():
        return img
    m = holes.copy()
    for _ in range(grow):
        m = (np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1) | m)
    a[m] = 0
    out = np.array(img).copy()
    out[:, :, 3] = a
    return Image.fromarray(out, "RGBA")


def flatten(img, size, pad):
    """クリーム地に焼いて正方形にする"""
    inner = size - pad * 2
    im = img.crop(img.getbbox()).resize(
        (inner, round(inner * img.crop(img.getbbox()).height / img.crop(img.getbbox()).width))
        if img.crop(img.getbbox()).width >= img.crop(img.getbbox()).height
        else (round(inner * img.crop(img.getbbox()).width / img.crop(img.getbbox()).height), inner),
        Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), CREAM + (255,))
    canvas.alpha_composite(im, ((size - im.width) // 2, (size - im.height) // 2))
    return canvas.convert("RGB")


def main():
    src = Image.open(SRC).convert("RGBA")
    os.makedirs(ICONS, exist_ok=True)

    # 走っている絵は目が頭の右端にあり、16pxでは何をしても背景の縁に溶けて消える。
    # 穴を広げると縁が欠けて見えるだけなので、この大きさでは素のシルエットで出す。
    small = src
    flatten(small, 16, 0).save(os.path.join(ICONS, "favicon-16x16.png"))
    flatten(src, 32, 1).save(os.path.join(ICONS, "favicon-32x32.png"))
    flatten(src, 180, 14).save(os.path.join(ICONS, "apple-touch-icon.png"))

    # .ico は16/32/48をまとめる。48も目を少し広げておく
    tmp = []
    for size, img, pad in ((16, small, 0), (32, src, 1), (48, src, 2)):
        p = os.path.join(ICONS, f"_ico{size}.png")
        flatten(img, size, pad).save(p)
        tmp.append(p)
    subprocess.run(["magick"] + tmp + [os.path.join(REPO, "favicon.ico")], check=True)
    for p in tmp:
        os.remove(p)

    for f in ("favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png"):
        im = Image.open(os.path.join(ICONS, f))
        print(f"  {f}  {im.width}x{im.height}")
    print(f"  favicon.ico  16/32/48")


if __name__ == "__main__":
    main()
