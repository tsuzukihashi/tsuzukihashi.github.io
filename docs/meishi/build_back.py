#!/usr/bin/env python3
"""裏面の作り直しの案（2026-11-20）。ぬりえの裏では「何をしている人か」が分からない、と言われたため。

    python3 docs/meishi/build_back.py

裏の役目: 表で名前と3人の絵を見た人が、ひっくり返して「この人はアプリを作っている人だ」と分かること。
もらうのは仕事の相手（会社の人・開発者）。表の3人がどのアプリの子かもつながると、子どもにも話せる。

- docs/meishi/sheet-back.html  表と3つの裏を並べた見比べシート
アイコンは App Store の 512px（docs/meishi/parts/icons/。レビュー数の多い順の一覧は index.json）
"""
import json
import os

from build_kids import FRONT, KCSS

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "parts", "icons", "index.json")))

CSS = KCSS + """
.ic { display:block; border-radius:22.5%; box-shadow:0 0 0 .12mm rgba(20,17,8,.18); }
.jp { font-family:'Noto Sans JP',sans-serif; }
"""


def icon(bundle_tail, size):
    return f'<img class="ic" src="parts/icons/{bundle_tail}.png" style="width:{size}mm; height:{size}mm;">'


# ---------- G 代表作（一言は2026-11-20 に本人が決めたテーマ。1行に収める） ----------
PICKS = [
    ("PoopCounter", "うんちくん", "うんちの記録と共有"),
    ("OmoideMap", "旅行思い出マップ", "思い出の写真で地図を作る"),
    ("BookBank", "もくもく", "読んだ本が通帳の残高になる"),
    ("pip", "流れるメモ帳", "絶対に忘れないメモ"),
    ("OshiIsland", "推しアイランド", "いつも推しと一緒"),
    ("AnataReceipt", "あなたレシート", "今日の自分がレシートになる"),
]
ASKS = ["こんなアプリが欲しい", "このアプリを作ってほしい", "開発を手伝ってほしい", "相談に乗ってほしい"]
asks = "".join(f'''<div class="jp" style="font-weight:700; font-size:1.95mm; color:var(--ink); white-space:nowrap;"><span style="display:inline-block; width:1.3mm; height:1.3mm; border-radius:50%; background:var(--purple); margin-right:1mm; vertical-align:.25mm;"></span>{t}</div>''' for t in ASKS)
LABEL = """<div style="display:flex; justify-content:space-between; align-items:baseline;">
      <div class="en" style="font-weight:700; font-style:italic; font-size:2.1mm; letter-spacing:.12em; color:var(--purple);">INDIE APP DEVELOPER</div>
      <div class="jp" style="font-weight:700; font-size:1.8mm; letter-spacing:.06em; color:var(--muted);">誰も作らないものを、まじめに作る。</div>
    </div>"""
WORK = """<div style="position:absolute; left:0; right:0; bottom:0; height:14.5mm; border-radius:1.6mm; background:#efe6d4; display:flex; align-items:center; padding:0 3mm;">
      <div style="flex:1;">
        <div class="jp" style="font-weight:900; font-size:2.5mm; letter-spacing:.03em; color:var(--ink);">お仕事のご相談も、お気軽にどうぞ。</div>
        <div style="margin-top:1.2mm; display:grid; grid-template-columns:auto auto; gap:1mm 4mm; justify-content:start;">""" + asks + """</div>
      </div>
      <div style="text-align:center;">  <!-- https://tsuzukit.com/contact/ -->
        <img src="parts/qrfun/contact-01-dots.svg" style="width:10mm; height:10mm;">
        <div class="en" style="margin-top:.6mm; font-weight:700; font-size:1.8mm; line-height:1; letter-spacing:.06em; color:var(--muted);">contact</div>
      </div>
    </div>"""


def g_card(head, apps):
    return f"""
<div class="card">
  <div class="safe">
    {LABEL}
    {head}
    {apps}
    {WORK}
  </div>
</div>"""


# G1: 横一列のまま、一言が入るように SkyCode を外して5本にする（一言の幅に合わせて列の幅を変える）
row5 = "".join(f"""
      <div style="text-align:center;">
        <div style="display:flex; justify-content:center;">{icon(b, 9)}</div>
        <div class="jp" style="margin-top:1.2mm; font-weight:700; font-size:1.75mm; color:var(--ink); white-space:nowrap;">{n}</div>
        <div class="jp" style="margin-top:.4mm; font-weight:500; font-size:1.45mm; color:var(--muted); white-space:nowrap;">{d}</div>
      </div>""" for b, n, d in PICKS[:5])
G1_BACK = g_card(
    '<div class="jp" style="margin-top:.9mm; font-weight:900; font-size:3.5mm; line-height:1.35; letter-spacing:.02em; color:var(--ink);">10年で100本以上、<br>iPhoneのアプリを作っています。</div>',
    f'<div style="position:absolute; left:0; right:0; top:17mm; display:flex; justify-content:space-between;">{row5}</div>')

# G2: 6本のまま、2列×3段のリストにする（アイコンの右に名前と一言。見出しは1行）
list6 = "".join(f"""
      <div style="display:flex; align-items:center; gap:1.8mm;">
        {icon(b, 6.4)}
        <div>
          <div class="jp" style="font-weight:700; font-size:1.95mm; line-height:1.2; color:var(--ink); white-space:nowrap;">{n}</div>
          <div class="jp" style="margin-top:.7mm; font-weight:500; font-size:1.7mm; line-height:1.2; color:var(--muted); white-space:nowrap;">{d}</div>
        </div>
      </div>""" for b, n, d in PICKS)
G2_BACK = g_card(
    '<div class="jp" style="margin-top:.9mm; font-weight:900; font-size:3.15mm; letter-spacing:.01em; color:var(--ink); white-space:nowrap;">10年で100本以上、iPhoneのアプリを作っています。</div>',
    f'<div style="position:absolute; left:0; right:0; top:11.3mm; display:grid; grid-template-columns:1fr 1fr; gap:.9mm 3mm;">{list6}</div>')

G_BACK = G2_BACK  # 2026-11-20 に G2 に決めた

# ---------- H アイコンの壁 ----------
COLS, ROWS, SIZE, PITCH = 8, 7, 6.3, 7.45
wall = "".join(
    f'<div style="position:absolute; left:{4.2 + (i % COLS) * PITCH:.2f}mm; top:{4.6 + (i // COLS) * PITCH:.2f}mm;">'
    f'{icon(ICONS[i]["file"].split("/")[-1][:-4], SIZE)}</div>'
    for i in range(COLS * ROWS))
H_BACK = f"""
<div class="card">
  {wall}
  <div style="position:absolute; left:65.5mm; top:6mm; right:6mm; bottom:6mm;">
    <div class="impact" style="font-size:12.5mm; line-height:.95; color:var(--ink);">100+</div>
    <div class="impact" style="font-size:5.2mm; line-height:1; letter-spacing:.04em; color:var(--ink);">APPS</div>
    <div class="jp" style="margin-top:2.6mm; font-weight:700; font-size:2.25mm; line-height:1.55; color:var(--ink);">10年で100本以上の<br>iPhoneアプリを、<br>ひとりで作っています。</div>
        <div class="en" style="position:absolute; left:0; bottom:0; font-weight:700; font-size:2.1mm; letter-spacing:.04em; color:var(--ink);">tsuzukit.com</div>
  </div>
</div>"""

# ---------- I 表の3人のアプリ ----------
def col(chara, chara_h, ic, name, line):
    return f"""
    <div style="flex:1; display:flex; flex-direction:column; align-items:center; text-align:center;">
      <div style="height:15mm; display:flex; align-items:flex-end;">{chara}</div>
      <div style="margin-top:1.6mm;">{ic}</div>
      <div class="jp" style="margin-top:1.2mm; font-weight:900; font-size:2.2mm; color:var(--ink);">{name}</div>
      <div class="jp" style="margin-top:.5mm; font-weight:500; font-size:1.7mm; line-height:1.35; color:var(--muted);">{line}</div>
    </div>"""


mini = "".join(f'<div>{icon(x["file"].split("/")[-1][:-4], 2.9)}</div>'
               for x in [i for i in ICONS if i["bundle"].split(".")[-1] not in ("PoopCounter", "BookBank")][:8])
I_BACK = f"""
<div class="card">
  <div class="safe">
    <div class="jp" style="font-weight:900; font-size:3.3mm; letter-spacing:.02em; color:var(--ink);">うんちくんも、もくもくも、僕のアプリの子です。</div>
    <div class="en" style="margin-top:.6mm; font-weight:700; font-style:italic; font-size:2mm; letter-spacing:.1em; color:var(--purple);">INDIE APP DEVELOPER · 100+ APPS SINCE 2016</div>
    <div style="position:absolute; left:0; right:0; top:10.5mm; display:flex; gap:2mm;">
      {col('<img src="parts/unchikun-hi.png" style="height:13mm;">', 13, icon("PoopCounter", 7.5), "うんちくん", "うんちを記録するアプリ")}
      {col('<img src="parts/mokumoku-welcome.png" style="height:14mm;">', 14, icon("BookBank", 7.5), "もくもく", "読んだ本が貯まる<br>読書の通帳")}
      {col('<img src="parts/character-wave.svg" style="height:14.5mm;">', 14.5,
           f'<div style="display:grid; grid-template-columns:repeat(4, 2.9mm); gap:.6mm; padding:.2mm 0;">{mini}</div>',
           "TsuzuKit（僕）", "ほかにも100本以上。<br>ぜんぶ tsuzukit.com に")}
    </div>
  </div>
</div>"""

PATTERNS = [
    ("G1", "横一列・5本", "いまの G の並びのまま、一言が1行に入るように SkyCode を外して5本にする", G1_BACK),
    ("G2", "2列×3段・6本", "6本のまま、アイコンの右に名前と一言を置くリストにする。一言の字が少し大きくなる。見出しは1行", G2_BACK),
]


def sheet():
    rows = [f"""
<section class="row"><h2>表（07 自撮り・変えない）</h2>
  <div class="pair"><figure><div class="trim">{FRONT}</div></figure></div></section>"""]
    for key, name, why, back in PATTERNS:
        rows.append(f"""
<section class="row"><h2>{key}　{name}</h2><p>{why}</p>
  <div class="pair"><figure><div class="trim">{back}</div></figure></div></section>""")
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 裏面の案</title>
<style>{CSS}
body {{ background:#cfc9bc; padding:8mm; }}
.wrap {{ display:grid; grid-template-columns:repeat(2, 100mm); gap:4mm 8mm; }}
.row h2 {{ font-family:'Noto Sans JP'; font-size:4.2mm; font-weight:900; color:var(--ink); }}
.row p {{ font-family:'Noto Sans JP'; font-size:2.5mm; line-height:1.5; color:var(--text); margin:1mm 0 2.5mm; width:96mm; }}
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); margin-top:2mm; }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body><div class="wrap">{''.join(rows)}</div></body></html>"""
    open(os.path.join(HERE, "sheet-back.html"), "w").write(html)


if __name__ == "__main__":
    sheet()
    print("ok")
