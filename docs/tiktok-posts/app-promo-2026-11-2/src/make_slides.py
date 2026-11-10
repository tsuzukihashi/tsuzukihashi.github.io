"""StepLens（お散歩のお題アプリ）を、見る人の悩みから入って、アプリで解決する順に見せる回（悩み → 解決の型）。
悩みは App Store の説明文の書き出し「いつものお散歩コース、ちょっとマンネリ化していませんか？」から取った。
n1: いつも同じ道で飽きる → お題が届くと、同じ道で探しものが始まる
n2: 先週の散歩で見たものを覚えていない → 撮った写真がカレンダーに残る
アプリの画面は p1-steplens（紹介）と s14-steplens（和暦の話）で使ったので、この2本では使わない（2026-11-10 本人「同じ画像ばっかり」）。
お題の名前は実物（App Store の説明文・ストア画像）で、写真は Pexels の実写（assets/photos/*/_manifest.json）。写真には「写真はイメージです」を添える。
2本のあいだでも、1本の中でも、同じ写真は1回だけ。

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


def photo(tag_dir: str, pid: str) -> str:
    return f"{A}/photos/{tag_dir}/{pid}.jpg"


NOTE = '<div style="font-size:22px;color:#6c6356;margin-top:12px">写真はイメージです</div>'


def tag_chip(text: str, size: int) -> str:
    return (f'<span style="background:rgba(20,17,12,.82);color:#fff;font-weight:900;font-size:{size}px;'
            f'border-radius:14px;padding:6px 18px;white-space:nowrap">{text}</span>')


def framed_photo(src: str, size: int, label: str) -> str:
    """正方形の写真の右上に、お題の札を重ねる"""
    return (f'<div style="position:relative;width:{size}px;height:{size}px;margin:0 auto">'
            f'<img src="{src}" style="width:{size}px;height:{size}px;object-fit:cover;display:block;border-radius:24px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">'
            f'<div style="position:absolute;top:18px;right:18px">{tag_chip(label, 30)}</div></div>')


def week(cells: list, tint: str) -> str:
    """月〜日の7日を1列に並べる。悩みの1枚で「毎日おなじ」「なにも残っていない」を見せる"""
    out = ""
    for d, c in zip("月火水木金土日", cells):
        out += (f'<div style="width:96px;height:150px;background:#fff;border:3px solid {INK};border-radius:18px;'
                f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px">'
                f'<span style="font-weight:900;font-size:26px;color:{PURPLE}">{d}</span>'
                f'<span style="font-weight:900;font-size:{40 if len(c) == 1 else 22}px;color:{tint};'
                f'line-height:1.15;text-align:center">{c}</span></div>')
    return f'<div style="display:flex;gap:10px;justify-content:center;filter:drop-shadow(8px 8px 0 {PURPLE})">{out}</div>'


def photo_week(photos: list) -> str:
    """月〜土は撮った写真、日はまだ「？」。1枚目の7日と対にする"""
    def cell(day: str, inner: str) -> str:
        return (f'<div style="position:relative;width:168px;height:168px;border:3px solid {INK};border-radius:18px;'
                f'overflow:hidden;background:#fff">{inner}'
                f'<span style="position:absolute;top:8px;left:8px;background:#fff;color:{PURPLE};font-weight:900;'
                f'font-size:24px;border-radius:10px;padding:0 10px;border:2px solid {INK}">{day}</span></div>')
    cells = [cell(d, f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;display:block">')
             for d, src in zip("月火水木金土", photos)]
    cells.append(cell("日", f'<div style="height:100%;display:flex;align-items:center;justify-content:center;'
                            f'font-weight:900;font-size:64px;color:{PURPLE}">？</div>'))
    return (f'<div style="width:740px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:center;gap:14px;'
            f'filter:drop-shadow(8px 8px 0 {PURPLE})">{"".join(cells)}</div>')


def pair(a: str, la: str, b: str, lb: str) -> str:
    return (f'<div style="display:flex;gap:30px;justify-content:center">'
            f'{framed_photo(a, 370, la)}{framed_photo(b, 370, lb)}</div>')


def ending(question: str, line: str, pose: str) -> str:
    return k.page(f"""
<div style="height:200px"></div>
<div class="big">{question}</div>
<div style="margin-top:60px"><img src="{chara(pose)}" style="width:260px"></div>
<div class="subline" style="margin-top:40px">{line}</div>
<div style="margin-top:22px">{store_card()}</div>""", "")


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
    tight("01", "道はそのまま、探すものを変える",
          framed_photo(photo("michi", "18766722"), 540, "今日のお題　#赤いドア") + NOTE,
          "毎日1つ、散歩のお題が届く。|いつもの道で、それを探して歩く。", ""),
    tight("02", "いつもの道で、探しものが始まる",
          pair(photo("akai-door", "17398836"), "#赤いドア", photo("noraneko", "39407407"), "#野良猫") + NOTE,
          "見つけたら、写真を撮って投稿する。|ほかの人が見つけた景色も見られる。",
          "お題を探して歩くと、|見慣れた道が新鮮になる。"),
    tight("03", "同じ道でも、毎日ちがう1枚",
          photo_week([photo("akai-door", "8304865"), photo("kujira-kumo", "7833039"), photo("noraneko", "32590772"),
                      photo("fushigi-kumo", "10757616"), photo("akai-tatemono", "1292496"), photo("kadan", "7534832")]) + NOTE,
          "お題は日替わりだから、|撮る写真も毎日ちがう。", ""),
    ending("いつもの散歩道、<br>何年歩いてますか？", "同じ道に、毎日ちがうお題", "run"),
])

# ---------------------------------------------------------------- n2 見たものを覚えていない
write("n2-oboete-nai", [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">仲間とアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:84px">先週の散歩で<br>{k.mark("見たもの")}<br>覚えてる？</div>
<div style="margin-top:40px">{week(BLANK, PURPLE)}</div>
<div style="margin-top:34px"><img src="{chara("think")}" style="width:230px"></div>""", ""),
    tight("01", "毎日1つ、お題が届く",
          framed_photo(photo("kujira-kumo", "36768656"), 540, "今日のお題　#くじらの形に見える雲") + NOTE,
          "お題を探して、|景色を見ながら歩く。", ""),
    tight("02", "見つけたら、1枚撮る",
          framed_photo(photo("noraneko", "40557739"), 540, "#野良猫") + NOTE,
          "お題に合うものを見つけたら、|写真を撮って投稿する。", ""),
    tight("03", "歩いた日が、写真で残る",
          photo_week([photo("akai-door", "8646429"), photo("kujira-kumo", "17194999"), photo("noraneko", "33317487"),
                      photo("fushigi-kumo", "9940016"), photo("akai-tatemono", "31284160"), photo("kadan", "8516871")]) + NOTE,
          "撮った写真が、|カレンダーに1日ずつ並んでいく。",
          "あとから見返すと、|どの日に何を見たか分かる。"),
    ending("先週の散歩で、<br>何を見ましたか？", "歩いた日が、写真で残る", "cheer"),
])
