#!/usr/bin/env python3
"""D 案のシンボル候補を、小さく使う大きさで並べる。

    python3 docs/logo/build_symbol_sheet.py

symbols/<名前>.png（ChatGPT の生の絵。クリーム地にシンボル1つ）を読み、
いまの D のシンボル（parts/D-dot-symbol.png）と一緒に、
タブ 16px（と4倍拡大）/ 32px / 丸アイコン 48・96px（クリーム地・墨地）/ ホーム画面 180px を並べる。
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_sheet import FONT, FONT_L, despeck, recolor_for_dark, square, to_img, trim, unmix  # noqa: E402

LABELS = {
    "D-now": "いまの D（真円に目2つ）",
    "S1-i": "S1 i を取り出す",
    "S2-peek": "S2 アイコンの枠からのぞく",
    "S3-body": "S3 全身で座る",
    "S4-ki": "S4 Ki の組み文字",
    "S5-glance": "S5 横目と片手",
}


def load(name):
    if name == "D-now":
        return Image.open(os.path.join(HERE, "parts", "D-dot-symbol.png")).convert("RGBA")
    rgb = np.array(Image.open(os.path.join(HERE, "symbols", name + ".png")).convert("RGB")).astype(float)
    return to_img(trim(despeck(unmix(rgb), 40), 2))


def circle(sym, size, bg, dark):
    icon = Image.new("RGBA", (size, size), bg + (255,))
    s = square(recolor_for_dark(sym) if dark else sym, size, 0.17)
    icon.paste(s, (0, 0), s)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    return icon, mask


def main():
    names = ["D-now", "S1-i", "S2-peek", "S3-body", "S4-ki", "S5-glance"]
    row_h, W = 230, 1500
    sheet = Image.new("RGB", (W, 50 + row_h * len(names)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(FONT, 20)
    small = ImageFont.truetype(FONT_L, 13)
    heads = [(24, "大きく"), (250, "タブ 16px"), (420, "16px を4倍"), (530, "32px"), (610, "丸 48 / 96（クリーム）"), (850, "丸 48 / 96（墨）"), (1090, "ホーム画面 180px")]
    for x, t in heads:
        d.text((x, 16), t, fill=(120, 112, 100), font=small)
    for i, n in enumerate(names):
        sym = load(n)
        y = 44 + row_h * i
        if i:
            d.line([24, y - 6, W - 24, y - 6], fill=(230, 226, 220), width=2)
        d.text((24, y), LABELS[n], fill=(20, 17, 12), font=font)
        top = y + 34
        d.rectangle([24, top, 214, top + 180], fill=(246, 242, 234))
        big = square(sym, 170, 0.04)
        sheet.paste(big, (34, top + 5), big)
        # タブ
        d.rectangle([240, top, 400, top + 36], fill=(222, 225, 230))
        d.rounded_rectangle([246, top + 5, 396, top + 36], radius=8, fill=(255, 255, 255))
        f16 = square(sym, 16, 0.0)
        sheet.paste(f16, (256, top + 13), f16)
        d.text((280, top + 11), "TsuzuKit", fill=(40, 40, 40), font=small)
        d.rectangle([420, top, 500, top + 80], fill=(246, 242, 234))
        z = f16.resize((64, 64), Image.NEAREST)
        sheet.paste(z, (428, top + 8), z)
        d.rectangle([530, top, 586, top + 56], fill=(246, 242, 234))
        f32 = square(sym, 32, 0.0)
        sheet.paste(f32, (542, top + 12), f32)
        for bx, bg, dark in ((610, (246, 242, 234), False), (850, (20, 17, 12), True)):
            for size, ox in ((48, 0), (96, 64)):
                ic, m = circle(sym, size, bg, dark)
                sheet.paste(ic, (bx + ox, top + 4), m)
        tile = Image.new("RGBA", (180, 180), (246, 242, 234, 255))
        s = square(sym, 180, 0.18)
        tile.paste(s, (0, 0), s)
        m = Image.new("L", (180, 180), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, 179, 179], radius=40, fill=255)
        sheet.paste(tile, (1090, top), m)
        ImageDraw.Draw(sheet).rounded_rectangle([1090, top, 1269, top + 179], radius=40, outline=(210, 204, 194))
    out = os.path.join(HERE, "symbol-sheet.png")
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
