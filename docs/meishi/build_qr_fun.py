#!/usr/bin/env python3
"""遊びのある QR の案（2026-11-20）。表の QR（https://tsuzukit.com/）を差し替える候補。

    python3 docs/meishi/build_qr_fun.py

- docs/meishi/parts/qrfun/<案>.svg   QR の部品（1マス = 1 の座標。幅 13mm で使う）
- docs/meishi/sheet-qrfun.html       表に入れた見比べ
読めるかは qr_vision.swift（Apple の Vision。iPhone のカメラと同じ読み取り）で確かめる。
"""
import os

import qrcode

from build_kids import KCSS, front

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parts", "qrfun")
URL = "https://tsuzukit.com/"
INK = "#14110c"
PURPLE = "#8b3df5"
BG = "#ded0b6"


def matrix(level, url=URL):
    q = qrcode.QRCode(error_correction=level, border=0)
    q.add_data(url)
    q.make(fit=True)
    return [[bool(v) for v in row] for row in q.get_matrix()]


def in_finder(n, r, c):
    return (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)


def finders(n):
    return [(0, 0), (0, n - 7), (n - 7, 0)]


def finder_round(r, c, color=INK):
    # 外の輪（7x7）と中の 3x3 を角丸で
    return (f'<path fill-rule="evenodd" fill="{color}" d="M{c + 1.6},{r} h3.8 a1.6,1.6 0 0 1 1.6,1.6 v3.8 a1.6,1.6 0 0 1 -1.6,1.6 h-3.8 '
            f'a1.6,1.6 0 0 1 -1.6,-1.6 v-3.8 a1.6,1.6 0 0 1 1.6,-1.6 z M{c + 1.9},{r + 1} h3.2 a.9,.9 0 0 1 .9,.9 v3.2 a.9,.9 0 0 1 -.9,.9 '
            f'h-3.2 a.9,.9 0 0 1 -.9,-.9 v-3.2 a.9,.9 0 0 1 .9,-.9 z"/>'
            f'<rect x="{c + 2}" y="{r + 2}" width="3" height="3" rx="1" fill="{color}"/>')


def finder_face(r, c):
    # 中の 3x3 を TsuzuKit のキャラの顔にする（黒い丸に白い縦長の目2つ）
    return (finder_round(r, c).split("<rect")[0]
            + f'<circle cx="{c + 3.5}" cy="{r + 3.5}" r="1.62" fill="{INK}"/>'
            # 目を大きくすると Vision で読めなくなった（rx .22 で ×）。rx .15・ry .3 ならどの大きさでも読めた
            f'<ellipse cx="{c + 3.1}" cy="{r + 3.3}" rx=".15" ry=".3" fill="{BG}"/>'
            f'<ellipse cx="{c + 3.9}" cy="{r + 3.3}" rx=".15" ry=".3" fill="{BG}"/>')


def dots(m, color=INK, skip=None):
    n = len(m)
    out = []
    for r in range(n):
        for c in range(n):
            if m[r][c] and not in_finder(n, r, c) and not (skip and skip(r, c)):
                out.append(f'<circle cx="{c + .5}" cy="{r + .5}" r=".46"/>')
    return f'<g fill="{color}">{"".join(out)}</g>'


def liquid(m, color=INK):
    # 隣どうしがつながる、とろっとした形
    n = len(m)
    out = []
    dark = lambda r, c: 0 <= r < n and 0 <= c < n and m[r][c] and not in_finder(n, r, c)
    for r in range(n):
        for c in range(n):
            if not dark(r, c):
                continue
            out.append(f'<circle cx="{c + .5}" cy="{r + .5}" r=".5"/>')
            if dark(r, c + 1):
                out.append(f'<rect x="{c + .5}" y="{r}" width="1" height="1"/>')
            if dark(r + 1, c):
                out.append(f'<rect x="{c}" y="{r + .5}" width="1" height="1"/>')
    return f'<g fill="{color}">{"".join(out)}</g>'


def svg(n, body, extra_top=0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-extra_top} {n} {n + extra_top}">{body}</svg>')


def center_face(n, k):
    # 真ん中の k×k マスを空けて、TsuzuKit の顔（半円の頭に目）を置く
    s = (n - k) / 2
    cx, cy = n / 2, n / 2
    return (f'<rect x="{s}" y="{s}" width="{k}" height="{k}" rx="1.4" fill="{BG}"/>'
            f'<circle cx="{cx}" cy="{cy + .35}" r="{k / 2 - .9}" fill="{INK}"/>'
            f'<ellipse cx="{cx - .75}" cy="{cy - .1}" rx=".42" ry=".8" fill="{BG}"/>'
            f'<ellipse cx="{cx + .75}" cy="{cy - .1}" rx=".42" ry=".8" fill="{BG}"/>')


def build():
    os.makedirs(OUT, exist_ok=True)
    M = matrix(qrcode.constants.ERROR_CORRECT_M)
    H = matrix(qrcode.constants.ERROR_CORRECT_H)
    nm, nh = len(M), len(H)
    k = 9  # 真ん中の顔を大きく。29マス中 9x9 を空けても読めた（ぼかし・傾き込み）
    lo, hi = (nh - k) / 2, (nh + k) / 2
    in_center = lambda r, c: lo - .5 <= r < hi + .5 and lo - .5 <= c < hi + .5
    v = {
        "01-dots": svg(nm, dots(M) + "".join(finder_round(r, c) for r, c in finders(nm))),
        "02-liquid": svg(nm, liquid(M) + "".join(finder_round(r, c) for r, c in finders(nm))),
        "03-faces": svg(nm, dots(M) + "".join(finder_face(r, c) for r, c in finders(nm))),
        "04-faces-purple": svg(nm, dots(M, PURPLE) + "".join(finder_face(r, c) for r, c in finders(nm))),
        "05-center": svg(nh, dots(H, INK, in_center) + "".join(finder_round(r, c) for r, c in finders(nh)) + center_face(nh, k)),
        "06-center-faces": svg(nh, dots(H, PURPLE, in_center) + "".join(finder_face(r, c) for r, c in finders(nh)) + center_face(nh, k)),
    }
    # 裏の問い合わせの QR（https://tsuzukit.com/contact/）は 01 のまるドット（2026-11-20）
    C = matrix(qrcode.constants.ERROR_CORRECT_M, "https://tsuzukit.com/contact/")
    nc = len(C)
    open(os.path.join(OUT, "contact-01-dots.svg"), "w").write(svg(nc, dots(C) + "".join(finder_round(r, c) for r, c in finders(nc))))
    for name, s in v.items():
        open(os.path.join(OUT, name + ".svg"), "w").write(s)
    return list(v)


CAPTIONS = {
    "01-dots": "まるドット。マスを丸にして、角の四角も角丸に",
    "02-liquid": "とろっとつながる形。キャラの丸い体と同じ線",
    "03-faces": "3つの角が TsuzuKit の顔。丸の目が2つ",
    "04-faces-purple": "03 のドットを紫に。顔は墨のまま",
    "05-center": "真ん中に TsuzuKit の顔。読み取りの強さを上げて空けた",
    "06-center-faces": "角も真ん中も顔。ドットは紫。4人の TsuzuKit",
}


def sheet(names):
    base = front('<img src="parts/collab/07-selfie.png" style="max-width:100%; max-height:100%;">')
    # 表は 05 に決めたので、見比べの「今」は前の四角い QR に戻して並べる
    base = base.replace('src="parts/qrfun/05-center.svg"', 'src="parts/qr-site.svg"')
    old = '<img class="qr" src="parts/qr-site.svg" style="width:13mm; height:13mm;">'
    assert old in base
    cells = [f'<figure><figcaption><b>今</b>　四角いまま</figcaption><div class="zoom"><img src="parts/qr-site.svg"></div><div class="trim">{base}</div></figure>']
    for n in names:
        card = base.replace(old, f'<img class="qr" src="parts/qrfun/{n}.svg" style="width:13mm; height:13mm;">')
        cells.append(f'<figure><figcaption><b>{n[:2]}</b>　{CAPTIONS[n]}</figcaption>'
                     f'<div class="zoom"><img src="parts/qrfun/{n}.svg"></div><div class="trim">{card}</div></figure>')
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 QR の案</title>
<style>{KCSS}
body {{ background:#cfc9bc; padding:8mm; }}
.wrap {{ display:grid; grid-template-columns:repeat(3, 95mm); gap:7mm 6mm; }}
figcaption {{ font-family:'Noto Sans JP'; font-size:2.5mm; line-height:1.45; color:var(--ink); margin-bottom:1.6mm; height:7.5mm; }}
figcaption b {{ font-size:3.4mm; }}
.zoom {{ background:{BG}; width:91mm; height:40mm; display:flex; align-items:center; justify-content:center; margin-bottom:2mm; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.zoom img {{ width:32mm; height:32mm; }}
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body><div class="wrap">{''.join(cells)}</div></body></html>"""
    open(os.path.join(HERE, "sheet-qrfun.html"), "w").write(html)


if __name__ == "__main__":
    names = build()
    sheet(names)
    print("ok", names)
