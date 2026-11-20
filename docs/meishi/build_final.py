#!/usr/bin/env python3
"""刷る名刺（表は 07 自撮り・裏は G 代表作の6本＋お仕事の相談）の入稿用 PDF を作る。文字はアウトライン（図形）にする。

    python3 docs/meishi/build_final.py   # 表は build_kids.py、裏は build_back.py の G_BACK を使う

1. 透明のある PNG を、名刺の地の色（#ded0b6）の上に先に重ねて、透明の無い画像にする
   （透明のまま次の手順に通すと、PDF の中に 72dpi の粗い透明の型が入った）
2. Chrome で PDF にする → pdftocairo で SVG にして文字を図形に → rsvg-convert で PDF に戻す
出力: docs/meishi/tsuzukit-meishi-nyuko.pdf（97x61mm・表→裏の2ページ・フォントなし）
"""
import os
import re
import shutil
import subprocess
import tempfile

from build_back import CSS, FRONT, G_BACK

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BG = (0xDE, 0xD0, 0xB6)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FLAT = ["parts/collab/07-selfie.png"]


def flatten():
    os.makedirs(os.path.join(HERE, "parts", "flat"), exist_ok=True)
    out = {}
    for rel in FLAT:
        im = Image.open(os.path.join(HERE, rel)).convert("RGBA")
        bg = Image.new("RGBA", im.size, BG + (255,))
        bg.alpha_composite(im)
        dst = "parts/flat/" + os.path.basename(rel)
        bg.convert("RGB").save(os.path.join(HERE, dst))
        out[rel] = dst
    return out


def main():
    mapping = flatten()
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 入稿用</title>
<style>{CSS}
@page {{ size:97mm 61mm; margin:0; }}
.card {{ page-break-after:always; }}
</style></head><body>{FRONT}{G_BACK}</body></html>"""
    for src, dst in mapping.items():
        assert f'src="{src}"' in html, src
        html = html.replace(f'src="{src}"', f'src="{dst}"')
    # ページ（97.03mm）が名刺（97mm）よりわずかに大きく、端に白い筋が出たので、ページ全体も地の色で塗る
    html = html.replace("</style>", "html, body { background:#ded0b6; }\n</style>", 1)
    final_html = os.path.join(HERE, "print-final.html")
    open(final_html, "w").write(html)
    with tempfile.TemporaryDirectory() as d:
        pdf = os.path.join(d, "chrome.pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=10000",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file://" + final_html],
                       check=True, capture_output=True)
        svgs = []
        for page in (1, 2):
            svg = os.path.join(d, f"p{page}.svg")
            subprocess.run(["pdftocairo", "-svg", "-f", str(page), "-l", str(page), pdf, svg], check=True)
            # Chrome の PDF は中身がページより 0.3pt ほど小さく、SVG にすると端に白い筋が残る。
            # いちばん下にページ全体の地の色を敷く
            s = open(svg).read()
            m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
            rect = f'<rect x="0" y="0" width="{m.group(1)}" height="{m.group(2)}" fill="#ded0b6"/>'
            s = s.replace("</defs>", "</defs>\n" + rect, 1)
            open(svg, "w").write(s)
            svgs.append(svg)
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", os.path.join(HERE, "tsuzukit-meishi-nyuko.pdf"), *svgs],
                       check=True)
        # 見比べ用に、アウトラインにする前の PDF も残す
        shutil.copy(pdf, os.path.join(HERE, "tsuzukit-meishi-final-fonts.pdf"))
    print("ok")


if __name__ == "__main__":
    main()
