#!/usr/bin/env python3
"""D 案（裏はぬりえ地図）の表を、3人が一緒に何かしている10場面で作る。

    python3 docs/meishi/cutout_collab.py   # 先に背景を抜く
    python3 docs/meishi/build_collab.py

- docs/meishi/sheet-collab.html        10枚の表と共通の裏を並べたシート
- docs/meishi/collab/print-D-<番号>.html  入稿用（表→裏）
"""
import json
import os

from build_kids import D_BACK, KCSS, front

HERE = os.path.dirname(os.path.abspath(__file__))
SCENES = json.load(open(os.path.join(HERE, "collab", "scenes.json")))
NAMES = {
    "01-map": "地図を広げる", "02-tower": "肩車タワー", "03-hightouch": "ハイタッチ", "04-book": "絵本を読む",
    "05-cloudride": "もくもくに乗る", "06-books": "本の塔", "07-selfie": "自撮り", "08-walk": "手をつないで旅",
    "09-laptop": "アプリづくり", "10-picnic": "ピクニック",
}


def art(key, prefix):
    return f'<img src="{prefix}parts/collab/{key}.png" style="max-width:100%; max-height:100%;">'


def sheet():
    figs = []
    for key, _ in SCENES:
        figs.append(f'<figure><div class="trim">{front(art(key, ""))}</div><figcaption>{key[:2]}　{NAMES[key]}</figcaption></figure>')
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 D 案の表 10パターン</title>
<style>{KCSS}
body {{ background:#d9d3c6; padding:8mm; }}
h2 {{ font-family:'Noto Sans JP'; font-size:5mm; font-weight:900; color:var(--ink); margin-bottom:4mm; }}
.grid {{ display:grid; grid-template-columns:repeat(3, 91mm); gap:7mm 8mm; }}
figure figcaption {{ font-family:'Noto Sans JP'; font-size:2.8mm; font-weight:700; color:var(--text); margin-top:1.4mm; }}
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body>
<h2>表（10パターン）と共通の裏</h2>
<div class="grid">{''.join(figs)}<figure><div class="trim">{D_BACK}</div><figcaption>裏（共通）</figcaption></figure></div>
</body></html>"""
    open(os.path.join(HERE, "sheet-collab.html"), "w").write(html)


def prints():
    for key, _ in SCENES:
        back = D_BACK.replace('src="parts/', 'src="../parts/')
        html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 D-{key}</title>
<style>{KCSS.replace("../../assets", "../../../assets")}
@page {{ size:97mm 61mm; margin:0; }}
.card {{ page-break-after:always; }}
</style></head><body>{front(art(key, "../")).replace('src="parts/', 'src="../parts/').replace('src="../../assets', 'src="../../../assets')}{back}</body></html>"""
        open(os.path.join(HERE, "collab", f"print-D-{key}.html"), "w").write(html)


if __name__ == "__main__":
    sheet()
    prints()
    print("ok")
