"""TsuzuKit のアプリ × 作っていて本当に起きた話。StepLens（お散歩のお題アプリ）で、和暦の iPhone にお題が届かなかった話。

  python3 src/make_slides.py
  python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py src/html .

StepLens は伊藤さん（Shizuna Itoh）の名義で出ている、仲間と作っているアプリ。僕（Ryo）がいちばん多くコードを書いているが、
「ぜんぶ僕が作りました」とは書かない。バッジは「仲間とアプリを作ってます」、主語は「僕たち」。
話はすべて StelLenz リポジトリ（~/workspace/StelLenz）で裏を取った（出典は posts.json の research）。
画面は App Store の 1.3.4 のストア用画像（伊藤さんの名前と顔の写る行は切り落とした）。
見た目は app-story-2026-10-2 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/tiktok-slideshow/scripts"))
import slide_kit as k

HERE = Path(__file__).parent
FONTS = HERE / "assets/fonts"
A = "../../assets"

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
INK, PURPLE, GREEN, RED = "#14110c", "#8b3df5", "#1f9d6b", "#e2483d"


def write(pattern: str, slides: list) -> None:
    d = HERE / "html" / pattern
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(slides, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


def img(name: str) -> str:
    return f"{A}/img/{name}.png"


def chara(name: str) -> str:
    return f"{A}/chara/character-{name}.png"


def shot(name: str, width: int) -> str:
    return (f'<img src="{img(name)}" style="width:{width}px;display:block;margin:0 auto;border-radius:24px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def with_peek(inner: str) -> str:
    """切り出した画面の上の縁に、サイトの黒いキャラを立たせる（文字や投稿ボタンに重ねない）"""
    return (f'<div style="position:relative;display:inline-block;padding-top:166px">{inner}'
            f'<img src="{chara("peek")}" style="position:absolute;top:0;right:60px;width:150px"></div>')


def dates(width: int) -> str:
    """同じ日を、西暦の iPhone と和暦の iPhone で並べる"""
    def row(label: str, text: str, tint: str) -> str:
        return (f'<div style="display:flex;align-items:center;gap:26px;background:#fff;border:3px solid {INK};'
                f'border-radius:24px;box-shadow:8px 8px 0 {PURPLE};padding:18px 30px">'
                f'<span style="flex:none;font-weight:900;font-size:28px;color:#fff;background:{tint};'
                f'border-radius:999px;padding:4px 22px">{label}</span>'
                f'<span style="font-family:Dela;font-size:46px;white-space:nowrap">{text}</span></div>')
    return (f'<div style="width:{width}px;margin:0 auto;display:flex;flex-direction:column;gap:26px">'
            f'{row("西暦", "2026年11月10日", INK)}{row("和暦", "令和8年11月10日", PURPLE)}</div>')


def keys(fixed: bool) -> str:
    """アプリがお題を探すときの数字。直す前は和暦だと見つからない。直したあとは和暦でも西暦の数字で探す"""
    def row(label: str, num: str, result: str, ok: bool) -> str:
        color, mark = (GREEN, "✓") if ok else (RED, "✕")
        return (f'<div style="display:flex;align-items:center;gap:22px;padding:16px 4px">'
                f'<span style="flex:none;font-weight:900;font-size:28px;color:{PURPLE};width:150px;text-align:left">{label}</span>'
                f'<span style="flex:1;text-align:left;font-family:Anton;font-size:68px;letter-spacing:2px;line-height:1">{num}</span>'
                f'<span style="flex:none;font-weight:900;font-size:28px">{result}</span>'
                f'<span style="flex:none;width:56px;height:56px;border-radius:50%;background:{color};color:#fff;'
                f'display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900">{mark}</span></div>')
    return (f'<div style="width:740px;margin:0 auto;background:#fff;border:3px solid {INK};border-radius:26px;'
            f'box-shadow:10px 10px 0 {PURPLE};padding:10px 30px">'
            f'{row("西暦のiPhone", "20261110", "お題あり", True)}'
            f'<div style="border-top:2px dashed rgba(20,17,12,.18)"></div>'
            f'{row("和暦のiPhone", "20261110" if fixed else "81110", "お題あり" if fixed else "見つからない", fixed)}</div>')


def settings_path() -> str:
    """iPhone の設定で暦を見る場所（iOS 27.2 の InternationalSettings の文言）"""
    steps = ["設定", "一般", "言語と地域", "暦法"]
    chips = f'<span style="font-family:Anton;font-size:40px;color:{PURPLE}">›</span>'.join(
        f'<span style="background:#fff;border:3px solid {INK};border-radius:16px;padding:8px 20px;'
        f'font-weight:900;font-size:34px;white-space:nowrap">{w}</span>' for w in steps)
    return f'<div style="display:flex;align-items:center;justify-content:center;gap:12px">{chips}</div>'


def store_card() -> str:
    return (f'<div style="display:inline-flex;align-items:center;gap:22px;background:#fff;border:3px solid {INK};'
            f'border-radius:24px;box-shadow:8px 8px 0 {PURPLE};padding:14px 30px">'
            f'<img src="{img("icon")}" style="width:86px;height:86px;border-radius:23%;display:block;border:3px solid {INK}">'
            f'<span style="text-align:left;font-size:30px;line-height:1.4;font-weight:900">StepLens<br>'
            f'<span style="font-weight:700;font-size:26px;color:#fff;background:{PURPLE};border-radius:999px;padding:0 18px">入手</span>'
            f'</span></div>')


tight = k.phone_item

# ---------------------------------------------------------------- s14 StepLens
write("s14-steplens", [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">仲間とアプリを作ってます</div>
<div class="cover" style="margin-top:34px;font-size:84px">iPhoneを<br>{k.mark("和暦")}にしてる人に<br>お題が届かなかった</div>
<div class="subline" style="margin-top:26px">毎日お題が届く、お散歩アプリの話</div>
<div style="margin-top:40px">{with_peek(shot("walkers", 740))}</div>""", ""),
    tight("僕たちのアプリ", "毎日1つ、散歩のお題が届く", shot("neko", 470),
          "#野良猫、#不思議な形の雲。|お題を探しに歩いて、撮って投稿する。",
          "お題は日替わり。|その日になると、ホームに出てくる。"),
    k.item("まず知ってほしいこと", "iPhoneは和暦にもできる", dates(720),
           "設定の 言語と地域 › 暦法 で、|西暦か和暦を選べる。",
           "和暦にすると、iPhoneの日付が|令和で出るようになる。"),
    k.item("お題の探し方", "今日の日付を、数字にして探す", keys(False),
           "アプリは今日の日付を数字にして、|その日のお題を探していた。",
           "和暦だと令和8年の8から数えて|81110になり、お題が見つからない。"),
    k.item("2026年10月", "どの暦でも、西暦で数える", keys(True),
          "和暦のiPhoneでも、|今日のお題が出るように直した。",
          "公開してから1年5か月、|気づけていなかった。"),
    k.page(f"""
<div style="height:170px"></div>
<div class="big">あなたのiPhone、<br>西暦？和暦？</div>
<div class="subline" style="margin-top:56px">iPhoneの暦は、ここで見られる</div>
<div style="margin-top:22px">{settings_path()}</div>
<div style="margin-top:50px"><img src="{chara("think")}" style="width:220px"></div>
<div class="subline" style="margin-top:30px">いまは西暦でも和暦でも、毎日お題が届く</div>
<div style="margin-top:22px">{store_card()}</div>""", ""),
])
