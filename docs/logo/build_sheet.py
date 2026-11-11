#!/usr/bin/env python3
"""ロゴ案の比較シートを作る。

    python3 docs/logo/build_sheet.py                 # candidates/ の全部
    python3 docs/logo/build_sheet.py A-stack D-dot   # 名前を指定

candidates/<名前>.png は ChatGPT が出した生の絵（クリーム地に上段ロゴ・下段シンボル）。
上段と下段は、インクの無い横の帯でいちばん広いところで分ける。
うまく分かれないときは crops.json に {"<名前>": {"lockup": [x0,y0,x1,y1], "symbol": [...]}} を書く。

1案ごとに、いまのロゴと同じ形で並べる。
  クリーム地の原寸 / 暗いヘッダーの帯（実寸）/ ファビコン 16・32px / OGP カードの左上 / 丸いアイコン 48・96px
切り出したロゴは parts/<名前>-lockup.png と parts/<名前>-symbol.png に透過で残す。
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CAND = os.path.join(HERE, "candidates")
PARTS = os.path.join(HERE, "parts")
OUT = os.path.join(HERE, "sheet.png")

CREAM = np.array([246, 242, 234], dtype=float)
INK = np.array([20, 17, 12], dtype=float)
BAND = (63, 59, 53)  # ヘッダーの帯がヒーローの上に重なったときの色（スクショで実測）
FONT = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_L = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"


def unmix(rgb):
    """クリーム地の絵を、色＋アルファに分ける。墨はアルファ1の黒になる。"""
    a_ink = np.max((CREAM - INK) / CREAM)
    a = np.max((CREAM[None, None] - rgb) / CREAM[None, None], axis=2)
    a = np.clip(a / a_ink, 0, 1)
    a = np.clip((a - 0.08) / 0.92, 0, 1)  # 生成画像の地のわずかな色ずれを地として扱う
    safe = np.maximum(a, 1e-3)[..., None]
    fg = (rgb - (1 - a[..., None]) * CREAM) / safe
    fg = np.clip(fg, 0, 255)
    return np.dstack([fg, a * 255]).astype(np.uint8)


def despeck(rgba, min_area):
    """背景の点やゴミ（小さな塊）を消す。"""
    lab, n = ndimage.label(rgba[..., 3] > 24)
    if n == 0:
        return rgba
    areas = ndimage.sum(np.ones(lab.shape), lab, index=np.arange(1, n + 1))
    small = np.isin(lab, np.where(areas < min_area)[0] + 1)
    out = rgba.copy()
    out[small, 3] = 0
    return out


def trim(rgba, pad):
    al = rgba[..., 3] > 24
    ys, xs = np.where(al)
    if len(xs) == 0:
        return rgba
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, rgba.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, rgba.shape[1])
    return rgba[y0:y1, x0:x1]


def split(name, rgb):
    crops = {}
    path = os.path.join(HERE, "crops.json")
    if os.path.exists(path):
        crops = json.load(open(path)).get(name, {})
    rgba = despeck(unmix(rgb), 40)
    if crops:
        def cut(box):
            x0, y0, x1, y1 = box
            return trim(rgba[y0:y1, x0:x1], 2)
        return cut(crops["lockup"]), cut(crops["symbol"])
    ink_rows = (rgba[..., 3] > 40).sum(axis=1) > 0
    ys = np.where(ink_rows)[0]
    top, bottom = ys.min(), ys.max()
    # いちばん長い「インクの無い行の帯」で上下に分ける
    best, start, gap = (0, None), None, 0
    for y in range(top, bottom + 1):
        if not ink_rows[y]:
            if start is None:
                start = y
            gap = y - start + 1
            if gap > best[0]:
                best = (gap, (start + y) // 2)
        else:
            start = None
    if best[1] is None or best[0] < 30:
        raise SystemExit(f"{name}: 上段と下段を分ける帯が見つからない。crops.json に箱を書く")
    mid = best[1]
    return trim(rgba[:mid], 2), trim(rgba[mid:], 2)


def to_img(rgba):
    return Image.fromarray(np.ascontiguousarray(rgba))


def recolor_for_dark(img):
    """墨（暗い色）を白に、差し色はそのまま。"""
    a = np.array(img).astype(float)
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    sat = a[..., :3].max(2) - a[..., :3].min(2)
    dark = (lum < 110) & (sat < 60)
    a[dark, 0:3] = 255
    return Image.fromarray(a.astype(np.uint8))


def fit(img, w, h):
    r = min(w / img.width, h / img.height)
    return img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))), Image.LANCZOS)


def by_height(img, h):
    return img.resize((max(1, round(img.width * h / img.height)), h), Image.LANCZOS)


def square(img, size, pad_ratio):
    """シンボルを正方形の中央に置く（ファビコン・アイコン用）。"""
    inner = round(size * (1 - 2 * pad_ratio))
    s = fit(img, inner, inner)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(s, ((size - s.width) // 2, (size - s.height) // 2), s)
    return canvas


def current_parts():
    mark = Image.open(os.path.join(REPO, "assets/images/logo-mark.png")).convert("RGBA")
    mark = to_img(trim(np.array(mark), 2))
    ogp = Image.open(os.path.join(REPO, "assets/images/ogp/home.png")).convert("RGB")
    lock = to_img(trim(despeck(unmix(np.array(ogp.crop((60, 44, 262, 114))).astype(float)), 12), 2))
    return lock, mark


LABELS = {
    "A-stack": "A 積み上げ（アプリの形のタイルの上に座る）",
    "B-wordmark": "B 名前で立つ（K の脚が紫の下線に）",
    "C-seal": "C 續の判子",
    "D-dot": "D 文字に住む（i の点がキャラの頭）",
    "E-emblem": "E エンブレム",
}
ROW_H = 300
COLS = [("クリーム地", 520), ("ヘッダーの帯（実寸）", 300), ("タブ 16px / 32px", 250), ("OGP カード（X の表示幅）", 420), ("丸アイコン 48 / 96px", 220)]


def draw_row(sheet, y, label, lock, sym, font, font_s, fav):
    d = ImageDraw.Draw(sheet)
    d.text((24, y + 12), label, fill=(20, 17, 12), font=font)
    x = 24
    top = y + 52
    h = ROW_H - 70

    # 1. クリーム地
    w = COLS[0][1]
    d.rectangle([x, top, x + w, top + h], fill=(246, 242, 234), outline=(210, 204, 194))
    big = fit(lock, w - 60, h - 60)
    sheet.paste(big, (x + (w - big.width) // 2, top + (h - big.height) // 2), big)
    x += w + 16

    # 2. ヘッダーの帯（高さ72・ロゴの高さはいまの .nav-logo と同じ約26px）
    w = COLS[1][1]
    d.rectangle([x, top, x + w, top + h], fill=(246, 242, 234))
    d.rectangle([x, top, x + w, top + 72], fill=BAND)
    small = by_height(recolor_for_dark(lock), 26)
    if small.width > w - 40:
        small = fit(recolor_for_dark(lock), w - 40, 26)
    sheet.paste(small, (x + 20, top + (72 - small.height) // 2), small)
    d.text((x + 20, top + 90), "スマホ幅の帯", fill=(120, 112, 100), font=font_s)
    d.rectangle([x, top + 116, x + 200, top + 116 + 64], fill=BAND)
    small2 = by_height(recolor_for_dark(lock), 24)
    if small2.width > 170:
        small2 = fit(recolor_for_dark(lock), 170, 24)
    sheet.paste(small2, (x + 16, top + 116 + (64 - small2.height) // 2), small2)
    x += w + 16

    # 3. ファビコン（実寸）と、16px を4倍に拡大したもの
    w = COLS[2][1]
    d.rectangle([x, top, x + w, top + 40], fill=(222, 225, 230))
    d.rounded_rectangle([x + 8, top + 6, x + 180, top + 40], radius=8, fill=(255, 255, 255))
    f16 = fav[0] if fav else square(sym, 16, 0.0)
    sheet.paste(f16, (x + 18, top + 15), f16)
    d.text((x + 42, top + 13), "TsuzuKit", fill=(40, 40, 40), font=font_s)
    f32 = fav[1] if fav else square(sym, 32, 0.0)
    d.rectangle([x, top + 56, x + 60, top + 56 + 48], fill=(246, 242, 234), outline=(210, 204, 194))
    sheet.paste(f32, (x + 14, top + 64), f32)
    zoom = f16.resize((64, 64), Image.NEAREST)
    d.rectangle([x + 76, top + 56, x + 76 + 80, top + 56 + 80], fill=(246, 242, 234), outline=(210, 204, 194))
    sheet.paste(zoom, (x + 84, top + 64), zoom)
    d.text((x + 76, top + 142), "16px を4倍で", fill=(120, 112, 100), font=font_s)
    x += w + 16

    # 4. OGP（1200x630 をいまと同じ位置・高さに置いて、X のカード幅 420 に縮める）
    w = COLS[3][1]
    ogp = Image.open(os.path.join(REPO, "assets/images/ogp/home.png")).convert("RGB")
    ImageDraw.Draw(ogp).rectangle([60, 40, 520, 120], fill=(246, 242, 234))
    ol = by_height(lock, 50)
    if ol.width > 420:
        ol = fit(lock, 420, 50)
    ogp.paste(ol, (71, 54 + (50 - ol.height) // 2), ol)
    card = ogp.resize((w, round(630 * w / 1200)), Image.LANCZOS)
    sheet.paste(card, (x, top))
    d.rectangle([x, top, x + card.width - 1, top + card.height - 1], outline=(210, 204, 194))
    x += w + 16

    # 5. 丸いアイコン
    w = COLS[4][1]
    for size, ox in ((48, 0), (96, 70)):
        icon = Image.new("RGBA", (size, size), (246, 242, 234, 255))
        s = square(sym, size, 0.16)
        icon.paste(s, (0, 0), s)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
        sheet.paste(icon, (x + ox, top + 8), mask)
        ImageDraw.Draw(sheet).ellipse([x + ox, top + 8, x + ox + size - 1, top + 8 + size - 1], outline=(210, 204, 194))
    for size, ox in ((48, 0), (96, 70)):
        icon = Image.new("RGBA", (size, size), (20, 17, 12, 255))
        s = square(recolor_for_dark(sym), size, 0.16)
        icon.paste(s, (0, 0), s)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
        sheet.paste(icon, (x + ox, top + 120), mask)


def main():
    names = sys.argv[1:] or sorted(os.path.splitext(f)[0] for f in os.listdir(CAND) if f.endswith(".png"))
    os.makedirs(PARTS, exist_ok=True)
    icons = os.path.join(REPO, "assets/icons")
    fav_now = (Image.open(os.path.join(icons, "favicon-16x16.png")).convert("RGBA"),
               Image.open(os.path.join(icons, "favicon-32x32.png")).convert("RGBA"))
    rows = [("いまのロゴ（ファビコンは走るキャラ）", *current_parts(), fav_now)]
    for n in names:
        rgb = np.array(Image.open(os.path.join(CAND, n + ".png")).convert("RGB")).astype(float)
        lock, sym = split(n, rgb)
        lock, sym = to_img(lock), to_img(sym)
        lock.save(os.path.join(PARTS, f"{n}-lockup.png"))
        sym.save(os.path.join(PARTS, f"{n}-symbol.png"))
        rows.append((LABELS.get(n, n), lock, sym, None))
    W = 24 + sum(w for _, w in COLS) + 16 * (len(COLS) - 1) + 24
    H = 60 + ROW_H * len(rows) + 20
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    font = ImageFont.truetype(FONT, 22)
    font_s = ImageFont.truetype(FONT_L, 14)
    d = ImageDraw.Draw(sheet)
    x = 24
    for title, w in COLS:
        d.text((x, 20), title, fill=(120, 112, 100), font=font_s)
        x += w + 16
    for i, (label, lock, sym, fav) in enumerate(rows):
        y = 40 + ROW_H * i
        if i:
            d.line([24, y, W - 24, y], fill=(230, 226, 220), width=2)
        draw_row(sheet, y, label, lock, sym, font, font_s, fav)
    sheet.save(OUT)
    print(OUT, sheet.size)


if __name__ == "__main__":
    main()
