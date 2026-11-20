#!/usr/bin/env python3
"""もらった人の子どもも喜ぶ名刺の案（うんちくん・もくもく・旅行思い出マップ入り）。

    python3 docs/meishi/build_parts.py
    python3 docs/meishi/build_kids.py

- docs/meishi/sheet-kids.html     見比べるシート
- docs/meishi/print-<案>.html      入稿用（塗り足し込み 97x61mm。表→裏の順。E は裏が3種）

キャラはアプリの絵をそのまま使う（docs/meishi/parts/ にコピー済み）。
うんちくんの元絵は 300px 前後なので、名刺の上で 25mm を超える大きさにしない。
"""
import os

from build_cards import CSS, LOGO, MAIL

HERE = os.path.dirname(os.path.abspath(__file__))

KCSS = CSS + """
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=block');
.maru { font-family:'Zen Maru Gothic','Noto Sans JP',sans-serif; }
.chara { position:absolute; display:block; }
"""

# ---------- 共通の表（大人が見る面。右半分に作った人とキャラが並ぶ） ----------
FRONT = f"""
<div class="card">
  <!-- 3人の絵は ChatGPT の Image で作った1枚（docs/meishi/prompt-trio.md） -->
  <img class="chara" src="parts/trio.png" style="left:45mm; top:5mm; width:44mm;">
  <div class="safe">
    <img src="{LOGO}/tsuzukit-wordmark.svg" style="height:5mm">
    <div style="position:absolute; left:0; top:12mm;">
      <div style="font-family:'Noto Sans JP'; font-weight:900; font-size:6mm; letter-spacing:.12em; color:var(--ink);">續橋 涼</div>
      <div class="en" style="margin-top:1mm; font-weight:700; font-size:2.9mm; letter-spacing:.06em; color:var(--ink);">Ryo Tsuzukihashi</div>
      <div class="en" style="margin-top:.5mm; font-weight:700; font-style:italic; font-size:2.2mm; letter-spacing:.08em; color:var(--purple);">iOS DEVELOPER &amp; CREATOR</div>
    </div>
    <div class="contact" style="position:absolute; left:0; bottom:0;">
      <div><b>MAIL</b>{MAIL}</div>
      <div><b>WEB</b>tsuzukit.com</div>
      <div><b>X</b>@tsuzuki817</div>
      <div><b>GITHUB</b>tsuzukihashi</div>
    </div>
    <div style="position:absolute; right:0; bottom:0; text-align:center;">
      <img class="qr" src="parts/qr-site.svg" style="width:13mm; height:13mm;">
      <div class="en" style="margin-top:.8mm; font-weight:700; font-size:1.8mm; letter-spacing:.06em; color:var(--muted);">tsuzukit.com</div>
    </div>
  </div>
</div>"""

# ---------- D ぬりえ地図 ----------
D_BACK = """
<div class="card">  <!-- 表と同じクリーム地。県は白いまま残して、塗るところが分かるようにする -->
  <img class="chara" src="parts/japan-nurie.svg" style="left:40mm; top:5.5mm; height:51mm;">
  <img class="chara" src="parts/unchikun-balloons.png" style="left:52mm; top:6mm; width:10mm;">
  <img class="chara" src="parts/mokumoku-welcome.png" style="left:76mm; top:44.5mm; width:13mm;">
  <img class="chara" src="parts/character-wave.svg" style="left:24mm; bottom:-1.5mm; height:13mm;">
  <div class="safe">
    <div class="maru" style="font-weight:900; font-size:4.4mm; line-height:1.35; color:var(--ink);">いった<br>ところを<br>ぬってみよう！</div>
    <div class="maru" style="margin-top:2.2mm; font-weight:700; font-size:2.3mm; line-height:1.6; color:var(--text);">
      <span style="display:inline-block; width:3mm; height:3mm; border:.3mm solid var(--ink); border-radius:.5mm; vertical-align:-.5mm; background:#f4a6b8;"></span> すんでいる<br>
      <span style="display:inline-block; width:3mm; height:3mm; border:.3mm solid var(--ink); border-radius:.5mm; vertical-align:-.5mm; background:#f6c86b;"></span> いったことがある
    </div>
    <div class="maru" style="position:absolute; left:0; bottom:9.5mm; font-weight:700; font-size:1.9mm; line-height:1.45; color:var(--muted);">アプリ「旅行思い出マップ」<br>なら しゃしんで ぬれるよ</div>
  </div>
</div>"""

# ---------- E キャラカード（3しゅ） ----------
def e_card(no, bg, accent, img, img_style, name, app, line, qr):
    return f"""
<div class="card" style="background:{bg};">
  <div style="position:absolute; left:5mm; top:5mm; right:5mm; bottom:5mm; border:.5mm solid var(--ink); border-radius:3mm; background:#fffdf8;"></div>
  <div style="position:absolute; left:5mm; top:5mm; width:42mm; bottom:5mm; border-radius:3mm 0 0 3mm; background:{accent};"></div>
  <img class="chara" src="{img}" style="{img_style}">
  <div class="safe">
    <div class="en" style="position:absolute; left:44mm; top:1.5mm; font-weight:800; font-style:italic; font-size:2.3mm; letter-spacing:.12em; color:var(--muted);">No.{no} / 3</div>
    <div class="maru" style="position:absolute; left:44mm; top:6mm; font-weight:900; font-size:6mm; line-height:1.1; color:var(--ink);">{name}</div>
    <div class="maru" style="position:absolute; left:44mm; top:15.5mm; right:0; font-weight:700; font-size:2.5mm; line-height:1.5; color:var(--text);">{line}</div>
    <div class="maru" style="position:absolute; left:44mm; bottom:0; font-weight:700; font-size:1.9mm; line-height:1.4; color:var(--muted);">アプリ<br>{app}</div>
    <img class="qr" src="{qr}" style="position:absolute; right:1mm; bottom:1mm; width:10mm; height:10mm;">
  </div>
  <div class="maru" style="position:absolute; left:7mm; bottom:7mm; font-weight:900; font-size:2mm; color:var(--ink); background:#fffdf8; border:.3mm solid var(--ink); border-radius:2mm; padding:.4mm 1.6mm;">ぜんぶ あつめてね</div>
</div>"""

E_BACKS = [
    e_card(1, "#f9d3dc", "#f7b9c8", "parts/unchikun-celebration.png", "left:11mm; top:9mm; width:31mm;",
           "うんちくん", "うんちくん", "まいにちの うんちを<br>きろくする なかま。<br>げんきの もとだよ。", "parts/qr-unchikun.svg"),
    e_card(2, "#c9dbec", "#9dbedd", "parts/mokumoku-deposit.png", "left:8.5mm; top:12mm; width:36mm;",
           "もくもく", "もくもく", "よんだ ほんを<br>つみあげていく くも。<br>ほんが だいすき。", "parts/qr-mokumoku.svg"),
    e_card(3, "#d8ecd9", "#b5dbb9", "parts/japan-color.svg", "left:8mm; top:8.5mm; height:38mm;",
           "おもいで<br>ちず", "旅行思い出マップ", "いった ところが<br>ちずに のこるよ。", "parts/qr-omoidemap.svg"),
]
E_BACKS[2] = E_BACKS[2].replace('top:15.5mm;', 'top:20mm;')

# ---------- F 4コマ（このひとが つくったもの） ----------
def panel(img, img_style, title, line, bg):
    return f"""
<div style="position:relative; flex:1; border:.4mm solid var(--ink); border-radius:2mm; background:{bg}; overflow:hidden;">
  <img src="{img}" style="position:absolute; {img_style}">
  <div class="maru" style="position:absolute; left:0; right:0; bottom:1.4mm; text-align:center; font-weight:900; font-size:2.3mm; color:var(--ink);">{title}</div>
  <div class="maru" style="position:absolute; left:1mm; right:1mm; top:1.3mm; text-align:center; font-weight:700; font-size:1.75mm; line-height:1.35; color:var(--text);">{line}</div>
</div>"""

F_BACK = f"""
<div class="card" style="background:#fffdf8;">
  <div class="safe" style="display:flex; flex-direction:column;">
    <div class="maru" style="font-weight:900; font-size:3.2mm; color:var(--ink); margin-bottom:1.6mm;">この ひとが つくったよ</div>
    <div style="flex:1; display:flex; gap:1.6mm;">
      {panel("parts/unchikun-hi.png", "left:50%; top:11mm; width:17mm; transform:translateX(-50%);", "うんちくん", "うんちを<br>きろくするよ", "#fde3ea")}
      {panel("parts/mokumoku-deposit.png", "left:50%; top:12mm; width:19mm; transform:translateX(-50%);", "もくもく", "よんだ ほんが<br>たまるよ", "#e3edf7")}
      {panel("parts/japan-color.svg", "left:50%; top:10mm; width:17mm; transform:translateX(-50%);", "おもいでちず", "いった ところが<br>ちずに のこる", "#e6f3e7")}
      {panel("parts/character-think.svg", "left:50%; top:11.5mm; height:17mm; transform:translateX(-50%);", "つぎは…？", "つぎは なにを<br>つくろうかな", "#efe9dd")}
    </div>
  </div>
</div>"""

PATTERNS = [
    ("D", "ぬりえ地図", "裏が旅行思い出マップの日本地図のぬりえ。子どもが行ったところを色えんぴつで塗れる。アプリでやっていることを、紙で先に遊んでもらう", [D_BACK]),
    ("E", "キャラカード 3しゅ", "裏がキャラのカードで、うんちくん・もくもく・おもいでちずの3種類。何枚か渡すと「ぜんぶあつめたい」になる。QR はそれぞれのアプリのページ", E_BACKS),
    ("F", "4コマ「この ひとが つくったよ」", "裏が4つのコマ。親が子どもに「この人、うんちくん作った人だよ」と話せる。最後のコマは「つぎは なにを つくろうかな」", [F_BACK]),
]


def sheet():
    rows = [f"""
<section class="row">
  <h2>共通の表</h2>
  <p>名前と連絡先は大人のための面なので、前の A 案のまま。作った人（TsuzuKit のキャラ）・うんちくん・もくもくを、ChatGPT で1枚のまとまった絵にして右半分に置く</p>
  <div class="pair"><figure><div class="trim">{FRONT}</div><figcaption>表</figcaption></figure></div>
</section>"""]
    for key, name, why, backs in PATTERNS:
        figs = "".join(f'<figure><div class="trim">{b}</div><figcaption>裏{"（" + str(i + 1) + "）" if len(backs) > 1 else ""}</figcaption></figure>' for i, b in enumerate(backs))
        rows.append(f"""
<section class="row">
  <h2>{key}　{name}</h2>
  <p>{why}</p>
  <div class="pair">{figs}</div>
</section>""")
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺の案（子どもも喜ぶ）</title>
<style>{KCSS}
body {{ background:#d9d3c6; padding:10mm; }}
.row {{ margin-bottom:9mm; }}
.row h2 {{ font-family:'Noto Sans JP'; font-size:5mm; font-weight:900; color:var(--ink); }}
.row p {{ font-family:'Noto Sans JP'; font-size:3mm; color:var(--text); margin:1.5mm 0 4mm; max-width:300mm; }}
.pair {{ display:flex; gap:8mm; align-items:flex-start; }}
figure figcaption {{ font-family:'Noto Sans JP'; font-size:2.6mm; color:var(--muted); margin-top:1.5mm; }}
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body>{''.join(rows)}</body></html>"""
    open(os.path.join(HERE, "sheet-kids.html"), "w").write(html)


def prints():
    for key, _, _, backs in PATTERNS:
        html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 {key}</title>
<style>{KCSS}
@page {{ size:97mm 61mm; margin:0; }}
.card {{ page-break-after:always; }}
</style></head><body>{FRONT}{''.join(backs)}</body></html>"""
        open(os.path.join(HERE, f"print-{key}.html"), "w").write(html)


if __name__ == "__main__":
    sheet()
    prints()
    print("ok")
