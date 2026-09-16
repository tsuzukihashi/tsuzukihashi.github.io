#!/usr/bin/env python3
"""ChatGPTで描いてもらったキャラを、サイトで使える形に整える。

    python3 docs/character/import_generated.py ~/Downloads

やること
  1. クリームの背景を抜いて、黒＋アルファのPNGにする。目は穴として残るので
     置いた場所の背景色がそのまま透ける
  2. 余白を切り詰める
  3. 目と目の間隔を測って、全ポーズで頭の大きさを揃える。出したままだと
     1枚ごとに縮尺がぶれて、並べたときに大きさがちぐはぐになる
  4. assets/images/ に書き出す

目が見つからない絵（横向きで目が重なっている等）は縮尺を揃えられないので、
名前を出して報告する。その絵だけ手で倍率を決める。
"""
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "assets", "images")

# 出力時の目と目の間隔（px）。元絵の character-peek.png がこの値だったので合わせる
TARGET_EYE_SPAN = 49.0
INK = (20, 17, 12)

# 目以外の穴（足の隙間など）を目と取り違える絵がある。並べて見て決めた手当て。
# 自動で出した倍率に、さらにこれを掛ける
SCALE_FIX = {
    "character-surprised.png": 2.00,   # 見開いた目が大きく、間隔を測り違える
    "character-hang.png": 0.72,
    "character-run.png": 0.80,
    "character-tiny.png": 1.15,
}


def cutout(path):
    """クリーム地の絵を、黒＋アルファに変える。明るいほど透明"""
    im = Image.open(path).convert("L")
    a = 255 - np.array(im).astype(np.int16)
    # 背景のわずかな濁りを切り、線の縁のなめらかさは残す
    a = np.clip((a - 26) * (255 / (255 - 26)), 0, 255).astype(np.uint8)
    h, w = a.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[:, :] = INK
    return Image.fromarray(np.dstack([rgb, a]), "RGBA")


def eye_span(rgba):
    """体に空いた穴＝目 を探して、2つの中心の距離を返す。見つからなければ None"""
    a = np.array(rgba)[:, :, 3]
    solid = a > 128
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

    holes = (~solid) & (~outside)
    if not holes.any():
        return None

    label = np.zeros_like(holes, dtype=np.int32)
    n = 0
    spots = []
    for y in range(h):
        for x in range(w):
            if holes[y, x] and label[y, x] == 0:
                n += 1
                label[y, x] = n
                q = deque([(y, x)])
                px = []
                while q:
                    cy, cx = q.popleft()
                    px.append((cy, cx))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and holes[ny, nx] and label[ny, nx] == 0:
                            label[ny, nx] = n
                            q.append((ny, nx))
                if len(px) >= 40:          # 小さなゴミは拾わない
                    ys = [p[0] for p in px]
                    xs = [p[1] for p in px]
                    spots.append((sum(xs) / len(xs), sum(ys) / len(ys), len(px)))

    if len(spots) < 2:
        return None
    # 面積の大きい2つを目とみなす
    spots.sort(key=lambda s: -s[2])
    (x1, y1, _), (x2, y2, _) = spots[0], spots[1]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def main():
    src_dir = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Downloads")
    names = sorted(f for f in os.listdir(src_dir)
                   if f.startswith("character-") and f.endswith(".png"))
    if not names:
        print(f"{src_dir} に character-*.png が無い")
        return

    unknown = []
    for name in names:
        path = os.path.join(src_dir, name)
        img = cutout(path)
        box = img.getbbox()
        if not box:
            print(f"  {name}: 中身が無い"); continue
        img = img.crop(box)

        span = eye_span(img)
        if span and span > 8:
            k = TARGET_EYE_SPAN / span * SCALE_FIX.get(name, 1.0)
            img = img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))),
                             Image.LANCZOS)
            img = img.crop(img.getbbox())
            note = f"目の間隔 {span:.0f}px → ×{k:.2f}"
        else:
            unknown.append(name)
            note = "目が見つからない。縮尺は未調整"

        out = os.path.join(OUT, name)
        img.save(out)
        print(f"  {name}  {img.width}x{img.height}  {note}")

    if unknown:
        print("\n縮尺を揃えられなかった絵:", ", ".join(unknown))


if __name__ == "__main__":
    main()
