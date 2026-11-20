#!/usr/bin/env python3
"""表に「代表」を足した見本（2026-11-20）。TsuzuKit は屋号なので、付けるなら「代表」か英語の FOUNDER。

    python3 docs/meishi/build_title.py

- docs/meishi/sheet-title.html / .png  （入稿用 PDF はまだ変えない）
"""
import os

from build_kids import FRONT, KCSS

HERE = os.path.dirname(os.path.abspath(__file__))

NAME = """<div style="font-family:'RocknRoll One'; font-weight:400; font-size:6mm; letter-spacing:.1em; color:var(--ink);">續橋 涼</div>"""
ROLE = """<div class="en" style="margin-top:.5mm; font-weight:700; font-style:italic; font-size:2.2mm; letter-spacing:.08em; color:var(--purple);">iOS DEVELOPER &amp; CREATOR</div>"""
BLOCK_TOP = '<div style="position:absolute; left:0; top:12mm;">'
LOGO_IMG = '<img src="../../assets/images/logo/tsuzukit-wordmark.svg" style="height:5mm">'
for s in (NAME, ROLE, BLOCK_TOP, LOGO_IMG):
    assert s in FRONT, s

SMALL = "font-family:'Noto Sans JP'; font-weight:700; letter-spacing:.2em; color:var(--muted);"

VARIANTS = [
    ("今", "肩書きは iOS DEVELOPER &amp; CREATOR だけ", FRONT),
    ("A", "名前の上に小さく「代表」", FRONT
        .replace(BLOCK_TOP, '<div style="position:absolute; left:0; top:10.4mm;">')
        .replace(NAME, f'<div style="{SMALL} font-size:2.2mm; margin-bottom:.6mm;">代表</div>' + NAME)),
    ("B", "名前の左に小さく「代表」", FRONT
        .replace(NAME, f'<div style="display:flex; align-items:baseline; gap:2mm;"><span style="{SMALL} font-size:2.3mm;">代表</span>{NAME}</div>')),
    ("C", "英語の肩書きの頭に FOUNDER", FRONT
        .replace("iOS DEVELOPER &amp; CREATOR</div>", "FOUNDER / iOS DEVELOPER &amp; CREATOR</div>")),
    ("D", "ロゴの右に「代表」（TsuzuKit 代表と読める）", FRONT
        .replace(LOGO_IMG, f'<div style="display:flex; align-items:flex-end; gap:2mm;">{LOGO_IMG}<span style="{SMALL} font-size:2.4mm; line-height:1; margin-bottom:.2mm; color:var(--ink);">代表</span></div>')),
]


def main():
    cells = "".join(f'<figure><figcaption><b>{k}</b>　{why}</figcaption><div class="trim">{card}</div></figure>'
                    for k, why, card in VARIANTS)
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 代表を足した見本</title>
<style>{KCSS}
body {{ background:#cfc9bc; padding:8mm; }}
.wrap {{ display:grid; grid-template-columns:repeat(2, 95mm); gap:6mm 6mm; }}
figcaption {{ font-family:'Noto Sans JP'; font-size:2.6mm; color:var(--ink); margin-bottom:1.6mm; }}
figcaption b {{ font-size:3.4mm; }}
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body><div class="wrap">{cells}</div></body></html>"""
    open(os.path.join(HERE, "sheet-title.html"), "w").write(html)


if __name__ == "__main__":
    main()
    print("ok")
