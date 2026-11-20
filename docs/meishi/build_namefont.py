#!/usr/bin/env python3
"""表の名前（續橋 涼）の書体を10通り並べる見比べシート（2026-11-20）。

    python3 docs/meishi/build_namefont.py

- docs/meishi/sheet-namefont.html / .png
書体は Google Fonts から。「續」は入っていない書体がある（Murecho・Train One）ので、
3字とも入っていることを fontTools で確かめたものだけ使っている。
"""
import os
import urllib.parse

from build_back import CSS
from build_kids import FRONT

HERE = os.path.dirname(os.path.abspath(__file__))
NAME_STYLE = "font-family:'Noto Sans JP'; font-weight:900; font-size:6mm; letter-spacing:.12em;"

# (番号, 書体, 太さ, 一言, 字間)
FONTS = [
    ("今", "Noto Sans JP", 900, "いまの書体。太いゴシック", ".12em"),
    ("01", "Dela Gothic One", 400, "極太のゴシック。ロゴの TsuzuKit の太さに近い", ".08em"),
    ("02", "Mochiy Pop One", 400, "丸くて太いポップ体。3人の絵と同じやわらかさ", ".08em"),
    ("03", "Zen Maru Gothic", 900, "丸ゴシックの太字。やわらかいが崩しすぎない", ".12em"),
    ("04", "RocknRoll One", 400, "角を丸めたゴシック。少しくだけた感じ", ".1em"),
    ("05", "DotGothic16", 400, "ドット文字。アプリを作る人らしさ・ゲームっぽさ", ".1em"),
    ("06", "Zen Old Mincho", 900, "太い明朝。まじめで落ち着いた印象", ".14em"),
    ("07", "Shippori Mincho B1", 600, "はらいの効いた明朝。06 より細身で上品", ".14em"),
    ("08", "Kaisei Decol", 700, "丸みのある明朝。やさしいけれど品がある", ".12em"),
    ("09", "Yuji Syuku", 400, "筆の字。名刺らしい和の顔になる", ".12em"),
    ("10", "Potta One", 400, "筆で描いたポップ体。元気でにぎやか", ".08em"),
]


def font_import():
    fams = "&".join("family=" + urllib.parse.quote(f).replace("%20", "+") + (f":wght@{w}" if w != 400 else "")
                    for _, f, w, _, _ in FONTS[1:])
    return f"@import url('https://fonts.googleapis.com/css2?{fams}&display=block');\n"


def card(font, weight, spacing):
    assert NAME_STYLE in FRONT
    return FRONT.replace(NAME_STYLE, f"font-family:'{font}'; font-weight:{weight}; font-size:6mm; letter-spacing:{spacing};")


def main():
    cells = "".join(f"""
<figure><figcaption><b>{no}</b>　{f}<br><span>{why}</span></figcaption>
  <div class="trim">{card(f, w, sp)}</div></figure>""" for no, f, w, why, sp in FONTS)
    big = "".join(f"""
<div class="bigcell"><div class="no">{no}　{f}</div>
  <div style="font-family:'{f}'; font-weight:{w}; font-size:13mm; letter-spacing:{sp}; color:var(--ink); line-height:1.25;">續橋 涼</div></div>""" for no, f, w, why, sp in FONTS)
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 名前の書体</title>
<style>{font_import()}{CSS}
body {{ background:#cfc9bc; padding:8mm; }}
.wrap {{ display:grid; grid-template-columns:repeat(3, 95mm); gap:6mm 6mm; }}
figcaption {{ font-family:'Noto Sans JP'; font-size:2.6mm; line-height:1.45; color:var(--ink); margin-bottom:1.6mm; height:8mm; }}
figcaption b {{ font-size:3.4mm; }}
figcaption span {{ color:var(--text); font-size:2.3mm; }}
.big {{ display:grid; grid-template-columns:repeat(3, 95mm); gap:4mm 6mm; margin-bottom:10mm; }}
.bigcell {{ background:#ded0b6; padding:3mm 5mm 4mm; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.bigcell .no {{ font-family:'Noto Sans JP'; font-size:2.6mm; font-weight:700; color:var(--muted); margin-bottom:1mm; }}
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body><div class="big">{big}</div><div class="wrap">{cells}</div></body></html>"""
    open(os.path.join(HERE, "sheet-namefont.html"), "w").write(html)


if __name__ == "__main__":
    main()
    print("ok")
