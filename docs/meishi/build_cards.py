#!/usr/bin/env python3
"""TsuzuKit の名刺の案を HTML にする。

    python3 docs/meishi/build_parts.py   # 先に部品
    python3 docs/meishi/build_cards.py

- docs/meishi/sheet.html   見比べるシート（仕上がりの 91x55mm で切って並べる）
- docs/meishi/print-<案>.html  入稿用。1ページ目が表、2ページ目が裏。塗り足し 3mm 込みの 97x61mm
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = "../../assets/images/logo"

MAIL = "ryo.tsuzukihashi@tsuzukit.com"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Saira+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700;900&display=block');
:root { --cream:#f6f2ea; --ink:#14110c; --text:#2a2620; --muted:#6c6356; --purple:#8b3df5; --line:rgba(20,17,8,.18); }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'Inter','Noto Sans JP',sans-serif; color:var(--text); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
img { display:block; max-width:none; }
/* 塗り足し込みの紙。中身は .safe（仕上がりから 3mm 内側）に置く */
.card { position:relative; width:97mm; height:61mm; overflow:hidden; background:var(--cream); }
.card.tate { width:61mm; height:97mm; }
.card.ink { background:var(--ink); color:#fff; }
.safe { position:absolute; left:6mm; top:6mm; right:6mm; bottom:6mm; }
.en { font-family:'Saira Condensed','Inter',sans-serif; }
.impact { font-family:'Anton','Saira Condensed',sans-serif; }
.contact { font-size:2.3mm; line-height:1.55; letter-spacing:.01em; color:var(--text); }
.contact b { display:inline-block; width:9mm; font-family:'Saira Condensed',sans-serif; font-weight:700; font-style:italic; font-size:2.1mm; letter-spacing:.06em; color:var(--muted); }
.ink .contact, .ink .contact b { color:#fff; }
.qr { width:15mm; height:15mm; }
"""

# ---------- A 名前の面＋ロゴの面 ----------
A_FRONT = f"""
<div class="card">
  <div class="safe">
    <img src="{LOGO}/tsuzukit-wordmark.svg" style="height:5.2mm">
    <div style="position:absolute; left:0; top:13mm;">
      <div style="font-family:'Noto Sans JP'; font-weight:900; font-size:6.4mm; letter-spacing:.12em; color:var(--ink);">續橋 涼</div>
      <div class="en" style="margin-top:1.2mm; font-weight:700; font-size:3mm; letter-spacing:.06em; color:var(--ink);">Ryo Tsuzukihashi</div>
      <div class="en" style="margin-top:.6mm; font-weight:700; font-style:italic; font-size:2.3mm; letter-spacing:.08em; color:var(--purple);">iOS DEVELOPER &amp; CREATOR</div>
    </div>
    <div class="contact" style="position:absolute; left:0; bottom:0;">
      <div><b>MAIL</b>{MAIL}</div>
      <div><b>WEB</b>tsuzukit.com</div>
      <div><b>X</b>@tsuzuki817</div>
      <div><b>GITHUB</b>tsuzukihashi</div>
    </div>
    <div style="position:absolute; right:0; bottom:0; text-align:center;">
      <img class="qr" src="parts/qr-site.svg">
      <div class="en" style="margin-top:1mm; font-weight:700; font-size:1.9mm; letter-spacing:.06em; color:var(--muted);">tsuzukit.com</div>
    </div>
  </div>
</div>"""

A_BACK = f"""
<div class="card ink">
  <div class="safe" style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
    <img src="{LOGO}/tsuzukit-wordmark-white.svg" style="height:13mm">
    <div style="margin-top:4.5mm; font-family:'Noto Sans JP'; font-weight:700; font-size:2.9mm; letter-spacing:.14em;">誰も作らないものを、まじめに作る。</div>
    <div class="en" style="margin-top:1.4mm; font-weight:700; font-style:italic; font-size:2.2mm; letter-spacing:.2em; opacity:.7;">NOBODY ELSE WILL. — 100+ APPS SINCE 2016</div>
  </div>
</div>"""

# ---------- B キャラが主役 ----------
B_FRONT = f"""
<div class="card">
  <img src="parts/character-wave.svg" style="position:absolute; right:1mm; bottom:-3mm; height:36mm;">
  <div class="safe">
    <img src="{LOGO}/tsuzukit-wordmark.svg" style="height:4.4mm">
    <div style="position:absolute; left:0; top:11mm;">
      <div style="font-family:'Noto Sans JP'; font-weight:900; font-size:5.8mm; letter-spacing:.12em; color:var(--ink);">續橋 涼</div>
      <div class="en" style="margin-top:1mm; font-weight:700; font-size:2.8mm; letter-spacing:.06em; color:var(--ink);">Ryo Tsuzukihashi</div>
      <div class="en" style="margin-top:.5mm; font-weight:700; font-style:italic; font-size:2.2mm; letter-spacing:.08em; color:var(--purple);">iOS DEVELOPER &amp; CREATOR</div>
    </div>
    <div class="contact" style="position:absolute; left:0; bottom:0;">
      <div><b>MAIL</b>{MAIL}</div>
      <div><b>WEB</b>tsuzukit.com</div>
      <div><b>X</b>@tsuzuki817</div>
      <div><b>GITHUB</b>tsuzukihashi</div>
    </div>
  </div>
</div>"""

B_BACK = f"""
<div class="card">
  <img src="parts/character-cheer.svg" style="position:absolute; left:44mm; bottom:-1.5mm; height:22mm;">
  <div class="safe">
    <div style="font-family:'Noto Sans JP'; font-weight:900; font-size:4.6mm; line-height:1.3; letter-spacing:.04em; color:var(--ink);">誰も作らないものを、<br>まじめに作る。</div>
    <div class="impact" style="position:absolute; left:0; bottom:5.2mm; font-size:9mm; line-height:1; color:var(--ink);">100+ APPS</div>
    <div class="en" style="position:absolute; left:0; bottom:0; font-weight:700; font-style:italic; font-size:2.6mm; letter-spacing:.14em; color:var(--purple);">SINCE 2016 · NOBODY ELSE WILL.</div>
    <div style="position:absolute; right:0; bottom:0; text-align:center;">
      <img class="qr" src="parts/qr-site.svg">
      <div class="en" style="margin-top:1mm; font-weight:700; font-size:1.9mm; letter-spacing:.06em; color:var(--muted);">tsuzukit.com</div>
    </div>
  </div>
</div>"""

# ---------- C 和の面・英の面（縦） ----------
C_FRONT = f"""
<div class="card tate">
  <div class="safe">
    <div style="position:absolute; right:3mm; top:6mm; writing-mode:vertical-rl; font-family:'Noto Sans JP'; font-weight:900; font-size:8.6mm; letter-spacing:.18em; color:var(--ink);">續橋涼</div>
    <div style="position:absolute; right:14.5mm; top:6.5mm; writing-mode:vertical-rl; font-family:'Noto Sans JP'; font-weight:700; font-size:2.8mm; letter-spacing:.3em; color:var(--purple);">個人開発者</div>
    <div style="position:absolute; left:2mm; top:6mm; writing-mode:vertical-rl; font-family:'Noto Sans JP'; font-weight:500; font-size:2.5mm; letter-spacing:.24em; color:var(--muted);">誰も作らないものを、まじめに作る。</div>
    <div style="position:absolute; left:0; right:0; bottom:0; border-top:.25mm solid var(--ink); padding-top:2.4mm;">
      <img src="{LOGO}/tsuzukit-wordmark.svg" style="height:4.2mm">
      <div class="contact" style="margin-top:1.8mm; font-size:2.1mm;">{MAIL}<br>tsuzukit.com</div>
    </div>
  </div>
</div>"""

C_BACK = f"""
<div class="card tate ink">
  <div class="safe">
    <img src="{LOGO}/tsuzukit-wordmark-white.svg" style="height:6mm">
    <div class="en" style="margin-top:7mm; font-weight:800; font-size:5.2mm; line-height:1.05; letter-spacing:.02em;">Ryo<br>Tsuzukihashi</div>
    <div class="en" style="margin-top:1.4mm; font-weight:700; font-style:italic; font-size:2.2mm; letter-spacing:.08em; opacity:.75;">iOS DEVELOPER &amp; CREATOR</div>
    <div class="impact" style="margin-top:6mm; font-size:7.2mm; line-height:1;">100+ APPS</div>
    <div class="en" style="margin-top:.8mm; font-weight:700; font-style:italic; font-size:2.2mm; letter-spacing:.14em; opacity:.75;">SINCE 2016 · NOBODY ELSE WILL.</div>
    <div style="position:absolute; left:0; right:0; bottom:0; display:flex; align-items:flex-end; justify-content:space-between;">
      <div class="contact" style="font-size:2.1mm;">
        <div><b>MAIL</b></div><div style="font-size:1.95mm;">{MAIL}</div>
        <div><b>X</b>@tsuzuki817</div>
        <div><b>GITHUB</b>tsuzukihashi</div>
      </div>
      <div style="background:var(--cream); padding:1.2mm; border-radius:.6mm;"><img class="qr" src="parts/qr-site.svg" style="width:12mm; height:12mm;"></div>
    </div>
  </div>
</div>"""

PATTERNS = [
    ("A", "名前の面＋ロゴの面", "表に名前・連絡先・QR をまとめ、裏は墨地に文字ロゴと合言葉だけ。会社の人は表だけで用が済み、開発者には裏で屋号を覚えてもらう", A_FRONT, A_BACK),
    ("B", "キャラが主役", "表の右にキャラが手を振る。裏は「誰も作らないものを、まじめに作る。」と 100+ APPS と QR。勉強会で「あのキャラの人」と覚えてもらう寄り", B_FRONT, B_BACK),
    ("C", "和の面・英の面（縦）", "縦の名刺。表は縦組みの日本語、裏は墨地の英語。国内の会社の人には表、海外の開発者には裏を見せる", C_FRONT, C_BACK),
]


def sheet():
    rows = []
    for key, name, why, front, back in PATTERNS:
        tate = "tate" in front
        rows.append(f"""
<section class="row">
  <h2>{key}　{name}</h2>
  <p>{why}</p>
  <div class="pair">
    <figure><div class="trim {'tate' if tate else ''}">{front}</div><figcaption>表</figcaption></figure>
    <figure><div class="trim {'tate' if tate else ''}">{back}</div><figcaption>裏</figcaption></figure>
  </div>
</section>""")
    html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺の案</title>
<style>{CSS}
body {{ background:#d9d3c6; padding:10mm; }}
.row {{ margin-bottom:9mm; }}
.row h2 {{ font-family:'Noto Sans JP'; font-size:5mm; font-weight:900; color:var(--ink); }}
.row p {{ font-family:'Noto Sans JP'; font-size:3mm; color:var(--text); margin:1.5mm 0 4mm; max-width:200mm; }}
.pair {{ display:flex; gap:10mm; align-items:flex-start; }}
figure figcaption {{ font-family:'Noto Sans JP'; font-size:2.6mm; color:var(--muted); margin-top:1.5mm; }}
/* 仕上がりの 91x55mm で切って見せる */
.trim {{ width:91mm; height:55mm; overflow:hidden; position:relative; box-shadow:0 .6mm 2mm rgba(0,0,0,.18); }}
.trim.tate {{ width:55mm; height:91mm; }}
.trim > .card {{ position:absolute; left:-3mm; top:-3mm; }}
</style></head><body>{''.join(rows)}</body></html>"""
    open(os.path.join(HERE, "sheet.html"), "w").write(html)


def prints():
    for key, _, _, front, back in PATTERNS:
        tate = "tate" in front
        size = "61mm 97mm" if tate else "97mm 61mm"
        html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><title>TsuzuKit 名刺 {key}</title>
<style>{CSS}
@page {{ size:{size}; margin:0; }}
.card {{ page-break-after:always; }}
</style></head><body>{front}{back}</body></html>"""
        open(os.path.join(HERE, f"print-{key}.html"), "w").write(html)


if __name__ == "__main__":
    sheet()
    prints()
    print("ok")
