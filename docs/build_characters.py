#!/usr/bin/env python3
"""キャラの表情ちがいを作る。

元絵は assets/images/character-peek.png の1枚だけ。体はそのまま使って、
目（＝黒い体に空いた2つの穴）を塞いだり彫り直したりして表情を増やす。
体を描き直していないので、どの表情も線の太さや質感が揃う。

    python3 docs/build_characters.py

出力はすべて assets/images/ に置く。元絵は書き換えない。

できる表情と、いまの置き場所

    peek       素の顔        全ページのフッター、法務ページ
    sleep      目を閉じる     収益公開の達成率バーの右端（ゴールで待ちくたびれている）
    sleep-flip 同上を反転     記事の読み終わりの区切り線（左端に置くので反転）
    wink       片目をつぶる   トップのCTA、ランキングの1位
    surprised  目を見開く     404、検索0件
    squint     目を細める     Aboutの署名の横
    look       目線を外す     経歴の数字カード
    tiny       頭と目だけ     ポートフォリオの絞り込みバー
    *-flip     左右反転       左端に置くとき用。手をかける向きが内側を向く

同じページに同じ顔を2つ置かない。反転ぶんは使っていないものも出しているので、
置き場所を変えたくなったら差し替えるだけでよい。
"""
import math
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

SRC = "assets/images/character-peek.png"
OUT = "assets/images/"


def load_alpha(path):
    im = Image.open(path).convert("LA")
    return np.array(im)[:, :, 1]


def find_eye_holes(alpha):
    """外につながっていない透明の島＝目、を探して中心と大きさを返す"""
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

    holes = (~solid) & (~outside)
    label = np.zeros_like(holes, dtype=int)
    eyes = []
    n = 0
    for y in range(h):
        for x in range(w):
            if holes[y, x] and label[y, x] == 0:
                n += 1
                label[y, x] = n
                q = deque([(y, x)])
                while q:
                    cy, cx = q.popleft()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and holes[ny, nx] and label[ny, nx] == 0:
                            label[ny, nx] = n
                            q.append((ny, nx))
    for i in range(1, n + 1):
        ys, xs = np.where(label == i)
        eyes.append({
            "cx": float(xs.mean()), "cy": float(ys.mean()),
            "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1),
        })
    eyes.sort(key=lambda e: e["cx"])   # 左の目が先
    return eyes, holes


def to_image(alpha):
    """アルファだけの配列から、黒＋アルファのPNGを作る"""
    h, w = alpha.shape
    rgb = np.zeros((h, w), dtype=np.uint8)
    return Image.merge("LA", (Image.fromarray(rgb, "L"), Image.fromarray(alpha, "L")))


def stamp(alpha, shape, cx, cy, angle_deg, value):
    """shape（Lモードのマスク）を回して指定位置に焼き込む。value=0で穴、255で塞ぐ"""
    rot = shape.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    m = np.array(rot)
    mh, mw = m.shape
    y0 = int(round(cy - mh / 2))
    x0 = int(round(cx - mw / 2))
    h, w = alpha.shape
    for y in range(mh):
        ty = y0 + y
        if not (0 <= ty < h):
            continue
        row = m[y]
        for x in range(mw):
            tx = x0 + x
            if 0 <= tx < w and row[x] > 96:
                alpha[ty, tx] = value


def closed_eye_mask(length, thickness):
    """閉じた目。上にふくらんだ弧にする。小さく表示しても閉じていると分かる太さにする"""
    pad = thickness * 2
    height = int(length * 0.62)
    img = Image.new("L", (length + pad * 2, height + pad * 2), 0)
    d = ImageDraw.Draw(img)
    d.arc([pad, pad, pad + length, pad + height], start=190, end=350, fill=255, width=thickness)
    # 弧は箱の上半分にしか描かれない。実際の弧の位置で中心を取れるよう切り詰める
    return img.crop(img.getbbox())


def ellipse_mask(w, h):
    img = Image.new("L", (w + 8, h + 8), 0)
    ImageDraw.Draw(img).ellipse([4, 4, 4 + w, 4 + h], fill=255)
    return img


def main():
    alpha0 = load_alpha(SRC)
    eyes, holes = find_eye_holes(alpha0)
    assert len(eyes) == 2, f"目が2つ見つからない: {len(eyes)}"
    left, right = eyes
    # 頭の傾き。目と目を結ぶ線から出す
    tilt = math.degrees(math.atan2(-(right["cy"] - left["cy"]), right["cx"] - left["cx"]))
    print(f"目: 左({left['cx']:.0f},{left['cy']:.0f}) 右({right['cx']:.0f},{right['cy']:.0f})  傾き {tilt:.1f}度")

    def blank():
        """目を塞いだ状態から始める"""
        a = alpha0.copy()
        a[holes] = 255
        return a

    made = []

    # 寝ている。待ちくたびれた場所に置く
    a = blank()
    lid = closed_eye_mask(38, 9)
    for e in (left, right):
        stamp(a, lid, e["cx"], e["cy"], tilt, 0)
    to_image(a).save(OUT + "character-sleep.png")
    made.append("character-sleep.png")

    # 片目をつぶる。どや顔
    a = blank()
    stamp(a, ellipse_mask(left["w"], left["h"]), left["cx"], left["cy"], tilt, 0)
    stamp(a, lid, right["cx"], right["cy"], tilt, 0)
    to_image(a).save(OUT + "character-wink.png")
    made.append("character-wink.png")

    # 目を見開く。見つからない・びっくりした場所に置く
    a = blank()
    for e in (left, right):
        stamp(a, ellipse_mask(int(e["w"] * 1.20), int(e["h"] * 1.55)), e["cx"], e["cy"], tilt, 0)
    to_image(a).save(OUT + "character-surprised.png")
    made.append("character-surprised.png")

    # 目を細める。しれっとした顔
    a = blank()
    for e in (left, right):
        stamp(a, ellipse_mask(int(e["w"] * 1.30), int(e["h"] * 0.30)), e["cx"], e["cy"], tilt, 0)
    to_image(a).save(OUT + "character-squint.png")
    made.append("character-squint.png")

    # 目線を外している。実績を並べた横などに置く
    a = blank()
    rad = math.radians(tilt)
    for e in (left, right):
        dx, dy = 9 * math.cos(rad), -9 * math.sin(rad)
        stamp(a, ellipse_mask(int(e["w"] * 0.86), int(e["h"] * 0.92)),
              e["cx"] + dx, e["cy"] + dy, tilt, 0)
    to_image(a).save(OUT + "character-look.png")
    made.append("character-look.png")

    # 左右反転。左端に置くとき用。手をかける向きが内側を向く
    for name in ("character-peek", "character-sleep", "character-wink",
                 "character-surprised", "character-squint", "character-look"):
        Image.open(OUT + name + ".png").transpose(Image.FLIP_LEFT_RIGHT).save(OUT + name + "-flip.png")
        made.append(name + "-flip.png")

    # 頭と目だけ。ちょこっとだけ出したいとき
    base = Image.open(OUT + "character-peek.png")
    top = base.crop((0, 0, base.width, int(base.height * 0.56)))
    top = top.crop(top.getbbox())
    top.save(OUT + "character-tiny.png")
    top.transpose(Image.FLIP_LEFT_RIGHT).save(OUT + "character-tiny-flip.png")
    made += ["character-tiny.png", "character-tiny-flip.png"]

    for m in made:
        im = Image.open(OUT + m)
        print(f"  {m}  {im.width}x{im.height}")


if __name__ == "__main__":
    main()
