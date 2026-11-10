"""StepLens（お散歩のお題アプリ）を、見る人の悩みから入って、アプリで解決する順に見せる回（悩み → 解決の型）。
悩みは App Store の説明文の書き出し「いつものお散歩コース、ちょっとマンネリ化していませんか？」から取った。
n1: いつも同じ道で飽きる → お題が届くと、同じ道で探しものが始まる
n2: 先週の散歩で見たものを覚えていない → 撮った写真がカレンダーに残る

  python3 src/make_slides.py
  python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py src/html .

StepLens は伊藤さん（Shizuna Itoh）の名義で出ている、仲間と作っているアプリ。バッジは「仲間とアプリを作ってます」。
画面は App Store の 1.3.4 のストア用画像から、お題・写真・リアクション・カレンダーの部分を切り出した（名前と顔の写る行は入れない）。
できることは App Store の説明文と、ストア画像に写っていることだけ。
見た目は app-story-2026-11-2 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
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


def chara(name: str) -> str:
    return f"{A}/chara/character-{name}.png"


def shot(name: str, width: int) -> str:
    return (f'<img src="{img(name)}" style="width:{width}px;display:block;margin:0 auto;border-radius:24px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def with_chara(pose: str, size: int, inner: str) -> str:
    """切り出した画面の上の縁に、サイトの黒いキャラを立たせる（写真のタグや絵文字に重ねない）"""
    return (f'<div style="position:relative;display:inline-block;padding-top:{size + 16}px">{inner}'
            f'<img src="{chara(pose)}" style="position:absolute;top:0;right:60px;width:{size}px"></div>')


def tags(words: list) -> str:
    """お題の札（ストアの説明文に出てくるお題）"""
    chips = "".join(f'<span style="display:inline-block;background:{INK};color:#fff;font-weight:900;font-size:40px;'
                    f'border-radius:16px;padding:10px 28px;margin:10px 12px">＃{w}</span>' for w in words)
    return f'<div style="width:820px;margin:0 auto;text-align:center">{chips}</div>'


def store_card() -> str:
    return (f'<div style="display:inline-flex;align-items:center;gap:22px;background:#fff;border:3px solid {INK};'
            f'border-radius:24px;box-shadow:8px 8px 0 {PURPLE};padding:14px 30px">'
            f'<img src="{img("icon")}" style="width:86px;height:86px;border-radius:23%;display:block;border:3px solid {INK}">'
            f'<span style="text-align:left;font-size:30px;line-height:1.4;font-weight:900">StepLens<br>'
            f'<span style="font-weight:700;font-size:26px;color:#fff;background:{PURPLE};border-radius:999px;padding:0 18px">入手</span>'
            f'</span></div>')


def week(cells: list, tint: str) -> str:
    """月〜日の7日を1列に並べる。悩みの1枚で「毎日おなじ」「なにも残っていない」を見せる"""
    days = "月火水木金土日"
    out = ""
    for d, c in zip(days, cells):
        out += (f'<div style="width:96px;height:150px;background:#fff;border:3px solid {INK};border-radius:18px;'
                f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px">'
                f'<span style="font-weight:900;font-size:26px;color:{PURPLE}">{d}</span>'
                f'<span style="font-weight:900;font-size:{40 if len(c) == 1 else 22}px;color:{tint};'
                f'line-height:1.15;text-align:center">{c}</span></div>')
    return (f'<div style="display:flex;gap:10px;justify-content:center;filter:drop-shadow(8px 8px 0 {PURPLE})">{out}</div>')


def pair(a: str, b: str) -> str:
    """お題の写真を2枚ならべる"""
    one = (lambda n: f'<img src="{img(n)}" style="width:370px;height:370px;object-fit:cover;display:block;'
                     f'border-radius:22px;border:3px solid {INK};box-shadow:8px 8px 0 {PURPLE}">')
    return f'<div style="display:flex;gap:30px;justify-content:center">{one(a)}{one(b)}</div>'


tight = k.phone_item
SAME = ["いつも<br>の道"] * 7
BLANK = ["？"] * 7

# ---------------------------------------------------------------- n1 いつも同じ道で飽きる
write("n1-onaji-michi", [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">仲間とアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:84px">散歩、いつも<br>{k.mark("同じ道")}で<br>飽きてない？</div>
<div style="margin-top:40px">{week(SAME, "#6c6356")}</div>
<div style="margin-top:34px"><img src="{chara("sleep")}" style="width:230px"></div>""", ""),
    tight("01", "道はそのまま、探すものを変える", shot("home-top", 760),
          "毎日1つ、散歩のお題が届く。|#野良猫、#不思議な形の雲。", ""),
    tight("02", "いつもの道で、探しものが始まる", pair("cat", "cloud"),
          "お題に合うものを見つけたら、|写真を撮って投稿する。",
          "お題を探して歩くと、|見慣れた道が新鮮になる。"),
    tight("03", "同じ道でも、毎日ちがう1枚", shot("calendar", 650),
          "お題は日替わりだから、|カレンダーに並ぶ写真も毎日ちがう。", ""),
    k.page(f"""
<div style="height:170px"></div>
<div class="big">いつもの散歩道、<br>何年歩いてますか？</div>
<div style="margin-top:50px">{tags(["赤いドア", "くじらの形に見える雲", "野良猫", "不思議な形の雲"])}</div>
<div class="subline" style="margin-top:50px">同じ道に、毎日ちがうお題</div>
<div style="margin-top:22px">{with_chara("wave", 170, store_card())}</div>""", ""),
])

# ---------------------------------------------------------------- n2 見たものを覚えていない
write("n2-oboete-nai", [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">仲間とアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:84px">先週の散歩で<br>{k.mark("見たもの")}<br>覚えてる？</div>
<div style="margin-top:40px">{week(BLANK, PURPLE)}</div>
<div style="margin-top:34px"><img src="{chara("think")}" style="width:230px"></div>""", ""),
    tight("01", "毎日1つ、お題が届く", shot("home-top", 760),
          "#野良猫、#不思議な形の雲。|お題を探して、景色を見ながら歩く。", ""),
    tight("02", "見つけたら、1枚撮る", shot("cat", 500),
          "お題に合うものを見つけたら、|写真を撮って投稿する。", ""),
    tight("03", "歩いた日が、写真で残る", shot("calendar", 540),
          "撮った写真が、|カレンダーに1日ずつ並んでいく。",
          "あとから見返すと、|どの日に何を見たか分かる。"),
    k.page(f"""
<div style="height:170px"></div>
<div class="big">先週の散歩で、<br>何を見ましたか？</div>
<div style="margin-top:44px">{shot("calendar", 560)}</div>
<div class="subline" style="margin-top:44px">歩いた日が、写真で残る</div>
<div style="margin-top:22px">{store_card()}</div>""", ""),
])
