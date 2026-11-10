"""TsuzuKit のアプリ × 作っていて本当に起きた話（2026-11-10）。もくもく（読書銀行）の子どもの通帳。

  python3 src/make_slides.py

筋: Threads に「小学生の子どもも読書家。でもスマホはまだ持っていない。親のアプリの中で子どもの分の通帳を作りたい」
という声が届いた。そのころの通帳は1冊だけで、画面は漢字だらけだった。だから、開くと画面の漢字にふりがなが付く
子どもの通帳を作った（6.6.0。2026-11-05 から App Store に出ている）。
声の中身は BookBank/docs/plan-passbooks.md の「きっかけ（Threads に届いた声）」の要約で、原文ではない。
画面は BookBank/docs/verify/ の撮影（kids-tabs-2026-11-03・kids-themes-2026-11-03）から切り出した。
あそびかたの絵は アプリの中の絵（Assets.xcassets/KidsGuide。ChatGPT で描いたもの）。
前のもくもくの回（s10 本が探せなくなった・s11 通帳にした・p2 宣伝・p1 一文・p2 読みたい本）とは別の話。
見た目は app-story-2026-10 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
"""
import subprocess
import sys
from pathlib import Path

KIT = Path.home() / ".claude/skills/tiktok-slideshow/scripts"
sys.path.insert(0, str(KIT))
import slide_kit as k  # noqa: E402

HERE = Path(__file__).parent
FONTS = HERE / "assets/fonts"
A = "../../assets"
MAKER = "Ryo Tsudukihashi"

BRAND = {
    "background": "background-color:#f6f2ea; background-image:linear-gradient(rgba(20,17,12,.07) 2px, transparent 2px),"
                  "linear-gradient(90deg, rgba(20,17,12,.07) 2px, transparent 2px); background-size:60px 60px;",
    "fonts": [("Dela", 400, FONTS / "DelaGothicOne-Regular.ttf"),
              ("Anton", 400, FONTS / "Anton-Regular.ttf"),
              ("NotoJP", "100 900", FONTS / "NotoSansJP-VF.ttf")],
    "head_font": "Dela", "head_weight": 400, "body_font": "NotoJP",
    "ink": "#14110c", "sub": "#6c6356", "accent": "#8b3df5", "mark": "#e4d4ff", "card": "#ffffff",
    "shadow": "rgba(20,17,12,.18)", "frame": "3px solid #14110c", "pop": "#8b3df5", "num_font": "Anton",
}
k.set_brand(BRAND)
INK, PURPLE = "#14110c", "#8b3df5"


def write(pattern: str, slides: list) -> None:
    d = HERE / "html" / pattern
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(slides, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


def img(name: str) -> str:
    return f"{A}/img/{name}"


def chara(name: str) -> str:
    return f"{A}/chara/{name}.png"


def shot(name: str, width: int) -> str:
    return (f'<img src="{img(name)}" style="width:{width}px;display:block;border-radius:24px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def with_moku(name: str, size: int, inner: str) -> str:
    """切り出した画面の右上に、もくもくを半分乗せる"""
    lift = int(size * 0.86)
    return (f'<div style="position:relative;padding-top:{lift}px;display:inline-block">{inner}'
            f'<img src="{chara(name)}" style="position:absolute;top:0;right:0;width:{size}px;height:{size}px"></div>')


def voice() -> str:
    """Threads に届いた声（要約）。吹き出しの札"""
    return (f'<div style="position:relative;display:inline-block;text-align:left">'
            f'<div style="background:#fff;border:3px solid {INK};border-radius:30px;box-shadow:10px 10px 0 {PURPLE};'
            f'padding:30px 44px;font-size:38px;line-height:1.65;font-weight:700;width:720px">'
            f'<div style="font-size:26px;color:#6c6356;font-weight:700;margin-bottom:10px">Threads に届いた声（要約）</div>'
            f'小学生の子どもも、本が大好き。<br>でも、スマホはまだ持っていない。<br>'
            f'親のアプリの中で、<br>子どもの分の通帳を作れたら。</div>'
            f'<div style="position:absolute;left:90px;bottom:-30px;width:44px;height:44px;background:#fff;'
            f'border-right:3px solid {INK};border-bottom:3px solid {INK};transform:rotate(45deg)"></div></div>')


def store_card() -> str:
    return (f'<div style="display:flex;align-items:center;gap:22px;background:#fff;border:3px solid {INK};'
            f'border-radius:24px;box-shadow:8px 8px 0 {PURPLE};padding:14px 30px">'
            f'<img src="{img("icon.png")}" style="width:86px;height:86px;border-radius:23%;display:block;'
            f'border:3px solid {INK}">'
            f'<span style="text-align:left;font-size:28px;line-height:1.4">{MAKER}<br>'
            f'<span style="color:#fff;background:{PURPLE};border-radius:999px;padding:0 18px">入手</span></span></div>')


tight = k.phone_item

# ---------------------------------------------------------------- s13 子どもの通帳
SLIDES = [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:84px">スマホのない子の<br>読書も、{k.mark("通帳")}に</div>
<div class="subline" style="margin-top:24px">Threads に届いた声から作った話</div>
<div style="margin-top:40px;display:flex;justify-content:center">{shot("guide-passbook.jpg", 660)}</div>""", ""),
    tight("僕のアプリ", "もくもく - 読書銀行", with_moku("welcome", 230, shot("card.png", 680)),
          "読んだ本の値段が、銀行の通帳みたいに<br>貯まっていく読書アプリです。", ""),
    tight("ある日", "こんな声が届いた", voice(),
          "でも、そのころの通帳は1冊だけ。<br>画面も、漢字だらけでした。", ""),
    tight("作ったもの", "ふりがなの付く通帳", with_moku("milestone", 170, shot("kids-ruby.png", 540)),
          "子どもの通帳を開くと、<br>画面の漢字にふりがなが付きます。", ""),
    tight("子どもだけの柄", "どうぶつ・うみ・うちゅう", shot("kids-themes.png", 620),
          "子どもの通帳だけで選べる柄を、<br>5つ足しました。", "どうぶつ・うみ・うちゅう・<br>のりもの・おかし。"),
    tight("自分で記帳", "読みおわったら、自分で", shot("guide-record.jpg", 700),
          "本のうらのバーコードを写すと、<br>子どもが自分で記帳できます。", "最初に、もくもくが<br>あそびかたを案内します。"),
    k.page(f"""
<div style="height:150px"></div>
<div class="big">お子さんが読んだ本、<br>どこに残していますか？</div>
<div style="margin-top:34px;display:flex;justify-content:center">{shot("guide-grow.jpg", 600)}</div>
<div class="subline" style="margin-top:34px;font-size:32px">子どもの通帳は、だれでも何冊でも作れます</div>
<div style="margin-top:26px;display:flex;justify-content:center">{store_card()}</div>
<div class="big" style="font-size:46px;margin-top:20px">{k.mark("もくもく - 読書銀行")}</div>""", ""),
]

if __name__ == "__main__":
    write("s13-kids-passbook", SLIDES)
    subprocess.run([sys.executable, str(KIT / "render.py"), str(HERE / "html"), str(HERE.parent)], check=True)
