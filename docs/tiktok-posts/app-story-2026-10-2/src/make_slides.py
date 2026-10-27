"""TsuzuKit のアプリ × 作っていて本当に起きた話（第2回）。もくもく（旧 BookBank）を、銀行の通帳にした話。

  python3 src/make_slides.py
  python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py src/html .

前の回（app-story-2026-10/s10-bookbank）は「本が探せなくなった話」。今回は別の話で、見た目の前と後を絵で見せる。
話はすべて BookBank のリポジトリで裏を取った（出典は posts.json の research）。
前の画面は App Store Connect に残っていた 5.0.0 のストア用スクショから切り出した。いまの画面は 6.3.0 のストア用の撮影。
見た目は app-story-2026-10 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/tiktok-slideshow/scripts"))
import slide_kit as k

HERE = Path(__file__).parent
FONTS = HERE / "assets/fonts"
A = "../../assets"
MAKER = "Ryo Tsudukihashi"
FACE = f"{A}/chara/character-peek.png"

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
    return f"{A}/img/{name}.png"


def framed(src: str, height: int) -> str:
    return (f'<img src="{src}" style="height:{height}px;display:block;border-radius:22px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def app_icon(src: str, size: int) -> str:
    return (f'<img src="{src}" style="width:{size}px;height:{size}px;border-radius:23%;display:block;'
            f'border:3px solid {INK};box-shadow:8px 8px 0 {PURPLE}">')


def arrow() -> str:
    return f'<span style="font-family:Anton;font-size:84px;color:{PURPLE};line-height:1">→</span>'


def before_after(left: str, right: str, labels: tuple) -> str:
    """前と後を矢印でつないで並べる。下に「前」「いま」の小さな札"""
    def cell(html: str, label: str) -> str:
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px">{html}'
                f'<span style="font-weight:900;font-size:28px;background:#fff;border:3px solid {INK};'
                f'border-radius:999px;padding:2px 20px">{label}</span></div>')
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:34px">'
            f'{cell(left, labels[0])}{arrow()}{cell(right, labels[1])}</div>')


def phone(name: str, height: int) -> str:
    return k.phone(img("mock-" + name), height)


def pair(left: str, right: str, height: int) -> str:
    return k.phone_pair(img("mock-" + left), img("mock-" + right), height)


tight = k.phone_item


# ---------------------------------------------------------------- s11 もくもく（旧 BookBank）
write("s11-mokumoku", [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:88px">7年前の<br>読書アプリを<br>{k.mark("通帳")}にした</div>
<div class="subline" style="margin-top:24px">紹介文では、通帳のつもりだった</div>
<div style="margin-top:30px">{before_after(phone("old-1", 350), phone("new-1", 350), ("前", "いま"))}</div>""", ""),
    tight("僕のアプリ", "2019年に作った読書アプリ", phone("old-1", 600),
          "本にいくら使ったかを見るアプリ。<br>紹介文は「銀行の口座に記帳するように」", ""),
    tight("でも、見た目は", "青い板が並んでいるだけ", pair("old-3", "old-4", 600),
          "どこを見ても、通帳っぽさがなかった。<br>2021〜2023年は、ほぼさわれなかった。", ""),
    tight("2026年10月", "画面を、通帳そのものに", phone("new-1", 600),
          "1冊が1行。列も本物の通帳と同じ<br>年月日・摘要・お預り金額・差引残高。", ""),
    tight("こだわったところ", "数字の頭の「＊」",
          f'<img src="{img("new-1-rows")}" style="width:730px;display:block;margin:0 auto;'
          f'border-radius:22px;border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">',
          "銀行の通帳にある「＊」は、<br>あとから数字を書き足せないための印。",
          "本の金額にも同じ印をつけた。<br>記帳すると、残高の数字が回って増える。"),
    tight("いまのもくもく", "もくもく - 読書銀行",
          f'<div style="display:flex;flex-direction:column;align-items:center;gap:24px">'
          f'<div style="display:flex;align-items:center;gap:22px;background:#fff;border:3px solid {INK};border-radius:24px;'
          f'box-shadow:8px 8px 0 {PURPLE};padding:14px 30px">{app_icon(img("icon-new"), 86)}'
          f'<span style="text-align:left;font-size:28px;line-height:1.4">{MAKER}<br>'
          f'<span style="color:#fff;background:{PURPLE};border-radius:999px;padding:0 18px">入手</span></span></div>'
          f'{pair("new-3", "new-6", 480)}</div>',
          "アイコンも、本の上で黙々と読む雲<br>「もくもく」に変えました。", ""),
    k.page(f"""
<div style="height:150px"></div>
<div class="big">読んだ本、<br>どこに記録していますか？</div>
<div style="margin-top:40px">{before_after(phone("old-1", 530), phone("new-1", 530), ("前", "いま"))}</div>
<div class="subline" style="margin-top:30px">2019年から7年かけて、やっと通帳に</div>
<div class="big" style="font-size:46px;margin-top:6px">{k.mark("もくもく - 読書銀行")}</div>""", ""),
])
