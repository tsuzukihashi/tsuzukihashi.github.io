"""TsuzuKit の個人開発アカウントで、旅行思い出マップを紹介する3本（2026-11-10）。4:5。

  python3 src/make_slides.py

s14-sticker   作っていて起きた話。ふたりで同じ地図を作っているのに、招待された人が貼ったステッカーが
              相手の地図に出ていなかった。届いた質問の予想どおり、地図を作った人の分しか残っていなかった。
              2026年9月に直した（出典: omoide-map/Docs/investigation-sticker-not-shared.md・コミット 349b250e・
              v1.54.0 の提出 0962fd11）。質問は原文ではなく要約で出す。
p01-shokai    ふつうの紹介。写真が市町村の形に切り抜かれる → 写真一覧 → 1か所に何枚でも → 市区町村まで → 先月のおもいで。
p02-mikaesanai 悩みから入る。旅行の写真が撮ったきり → 国の形に貼る（ヨーロッパ・アメリカ）→ 選べる地図。

絵は投稿ごとに分けて、同じ絵を2回使わない（skill tiktok-slideshow 0節の5）。前の回（app-story-2026-10 の
s05・app-picks・apps-x-sen）で使ったストアの1枚絵と日本地図の画面は使わない。
画面は omoide-map の fastlane/raw_screenshots/ja・Docs/verify・Assets.xcassets の実物から切り出した。
旅先の写真3枚は Pexels（assets/img/_pexels_used.json）。アプリの画面だとは言わない。
見た目は app-story-2026-11 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
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
INK, PURPLE, RED, GREEN = "#14110c", "#8b3df5", "#d6453d", "#2e9e5b"
tight = k.phone_item


def write(pattern: str, slides: list) -> None:
    d = HERE / "html" / pattern
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(slides, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


def img(name: str) -> str:
    return f"{A}/img/{name}"


def shot(name: str, height: int) -> str:
    """切り出した画面。高さで大きさを決める（縦長の画面が多いので）"""
    return (f'<img src="{img(name)}" style="height:{height}px;display:block;border-radius:24px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def stickers(names: list, size: int) -> str:
    """アプリの中のステッカーの絵を、白い札に並べる"""
    cells = "".join(f'<img src="{img("st-" + n + ".png")}" style="width:{size}px;height:{size}px;object-fit:contain">'
                    for n in names)
    return (f'<div style="display:grid;grid-template-columns:repeat(3,{size}px);gap:18px 30px;background:#fff;'
            f'border:3px solid {INK};border-radius:30px;box-shadow:10px 10px 0 {PURPLE};padding:26px 40px">{cells}</div>')


def photos(names: list) -> str:
    """旅先の写真を、少しずつ傾けて重ねる（カメラロールにたまっていく見え方）"""
    tilt = [(-8, -170, 20), (5, 0, 0), (-3, 170, 30)]
    pics = "".join(
        f'<img src="{img(n)}" style="position:absolute;left:50%;top:0;width:250px;height:340px;object-fit:cover;'
        f'margin-left:{-125 + dx}px;margin-top:{dy}px;transform:rotate({r}deg);border:10px solid #fff;border-radius:18px;'
        f'box-shadow:0 14px 30px rgba(20,17,12,.25)">'
        for n, (r, dx, dy) in zip(names, tilt))
    return f'<div style="position:relative;width:760px;height:390px">{pics}</div>'


def log(rows: list) -> str:
    """起きたことを並べる札。rows は [(左の見出し, 中身, "ok" / "ng")]。見出しの列は中身の長さから決める"""
    units = max(sum(0.6 if ord(c) < 128 else 1 for c in head) for head, _, _ in rows)
    head_w = int(units * 28) + 8
    cells = ""
    for i, (head, text, state) in enumerate(rows):
        color, mark = (GREEN, "✓") if state == "ok" else (RED, "✕")
        line = "" if i == len(rows) - 1 else "border-bottom:2px dashed rgba(20,17,12,.18);"
        cells += (f'<div style="display:flex;align-items:center;gap:20px;padding:14px 4px;{line}">'
                  f'<span style="flex:none;width:{head_w}px;text-align:left;font-weight:900;color:{PURPLE};font-size:28px">{head}</span>'
                  f'<span style="flex:1;text-align:left;font-size:30px;font-weight:800">{text}</span>'
                  f'<span style="flex:none;width:52px;height:52px;border-radius:50%;background:{color};color:#fff;'
                  f'display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:900">{mark}</span></div>')
    return (f'<div style="width:740px;background:#fff;border:3px solid {INK};border-radius:26px;'
            f'box-shadow:10px 10px 0 {PURPLE};padding:12px 30px">{cells}</div>')


def voice() -> str:
    """届いた質問（要約）。原文ではないので、札に『要約』と書く"""
    return (f'<div style="position:relative;display:inline-block;text-align:left">'
            f'<div style="background:#fff;border:3px solid {INK};border-radius:30px;box-shadow:10px 10px 0 {PURPLE};'
            f'padding:30px 44px;font-size:38px;line-height:1.65;font-weight:700;width:720px">'
            f'<div style="font-size:26px;color:#6c6356;font-weight:700;margin-bottom:10px">届いた質問（要約）</div>'
            f'わたしが貼ったステッカーが、<br>相手の地図に出ない。<br>相手が貼ったのは見えるのに。<br>'
            f'地図を作った人かどうかが、<br>関係ありますか？</div>'
            f'<div style="position:absolute;left:90px;bottom:-30px;width:44px;height:44px;background:#fff;'
            f'border-right:3px solid {INK};border-bottom:3px solid {INK};transform:rotate(45deg)"></div></div>')


def store_card() -> str:
    return (f'<div style="display:flex;align-items:center;gap:22px;background:#fff;border:3px solid {INK};'
            f'border-radius:24px;box-shadow:8px 8px 0 {PURPLE};padding:14px 30px">'
            f'<img src="{img("icon.jpg")}" style="width:86px;height:86px;border-radius:23%;display:block;'
            f'border:3px solid {INK}">'
            f'<span style="text-align:left;font-size:28px;line-height:1.4">{MAKER}<br>'
            f'<span style="color:#fff;background:{PURPLE};border-radius:999px;padding:0 18px">入手</span></span></div>')


def big_icon(size: int) -> str:
    return (f'<img src="{img("icon.jpg")}" style="width:{size}px;height:{size}px;border-radius:23%;display:block;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def end(question: str, lead: str) -> str:
    return k.page(f"""
<div style="height:170px"></div>
<div class="big" style="font-size:58px">{question.replace("|", "<br>")}</div>
<div style="margin-top:44px;display:flex;justify-content:center">{big_icon(260)}</div>
<div class="subline" style="margin-top:44px;font-size:32px">{lead}</div>
<div style="margin-top:30px;display:flex;justify-content:center">{store_card()}</div>
<div class="big" style="font-size:46px;margin-top:22px">{k.mark("旅行思い出マップ")}</div>""", "")


# ---------------------------------------------------------------- s14 ステッカーが相手に見えなかった
S14 = [
    k.cover("ひとりでアプリを作ってます", ["ステッカーが", k.mark("相手に"), "見えなかった"],
            "旅の写真を地図に貼るアプリの話",
            stickers(["daruma", "shisa", "akabeko", "koinobori", "fujisan", "takoyaki"], 112)),
    tight("僕のアプリ", "旅行思い出マップ", shot("home.png", 400),
          "旅の写真が県や市町村の形に|切り抜かれて、地図にはまる。", "ご当地のステッカーも貼れる。"),
    tight("まず知ってほしいこと", "ふたりで同じ地図",
          log([("1", "地図を作る", "ok"), ("2", "家族や恋人を招待する", "ok"), ("3", "同じ地図をいっしょに埋める", "ok")]),
          "招待すると、ふたりで|同じ地図に写真を貼っていける。", "招待は、リンクを送るだけ。"),
    tight("ある日", "こんな質問が届いた", voice(),
          "質問には、原因の予想まで|書いてあった。", ""),
    tight("調べたら", "予想が当たっていた",
          log([("地図を作った人", "貼った分が残る", "ok"), ("招待された人", "貼った分が残らない", "ng")]),
          "招待された人が貼った分は、|残っていなかった。", "しかも画面では、|ちゃんと貼れたように見えていた。"),
    tight("2026年9月", "だれが貼っても見える", shot("stickersheet.png", 400),
          "1枚ずつ分けて残すようにして、|だれが貼っても出るようにした。", "質問をくれた人の予想が、|そのまま答えでした。"),
    end("いっしょに地図を|埋めたい人、いますか？", "旅の写真を、地図に貼って残すアプリ"),
]

# ---------------------------------------------------------------- p01 ふつうの紹介
P01 = [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:80px">旅の写真が、<br>{k.mark("市町村の形")}になる</div>
<div style="margin-top:40px;display:flex;justify-content:center">{shot("gunma.png", 600)}</div>""", ""),
    tight("行った県ごとに", "写真一覧", shot("list.png", 470),
          "行った県ごとに、写真が並ぶ。", "地方ごとに、いくつ行ったかも出る。"),
    tight("1か所に", "写真は何枚でも", shot("gallery.png", 560),
          "ひとつの場所に、|写真を好きなだけ足せる。", ""),
    tight("市区町村まで", "北海道は179", shot("hokkaido-card.png", 500),
          "42の都道府県で、|市区町村まで記録できる。", "ぜんぶで1,667エリア。"),
    tight("毎月とどく", "先月のおもいで", shot("monthly.png", 560),
          "先月の写真が、|毎月まとめて届く。", ""),
    end("次に埋めたい県は、|どこですか？", "写真を貼る基本は、ずっと無料のまま"),
]

# ---------------------------------------------------------------- p02 撮ったきりの旅行の写真
P02 = [
    k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:30px;font-size:80px">旅行の写真、<br>{k.mark("撮ったきり")}に<br>なってない？</div>
<div class="subline" style="margin-top:24px">国の形に切り抜いて、地図に貼ってみる</div>
<div style="margin-top:40px;display:flex;justify-content:center">{photos(["trip-3735561.jpg", "trip-15564123.jpg", "trip-33839189.jpg"])}</div>""", ""),
    tight("僕が作ったのは", "ヨーロッパは29か国", shot("europe.png", 600),
          "撮った写真が国の形に|切り抜かれて、地図にはまる。", ""),
    tight("アメリカも", "50州と1準州", shot("usmap.png", 520),
          "行った州が、写真で埋まっていく。", ""),
    tight("どこの地図でも", "旅先から選ぶ", shot("area.png", 470),
          "日本・アメリカ・アジア・台湾・|ヨーロッパから選べる。", "日本は、市区町村の地図まである。"),
    end("次の旅行は、|どこの国ですか？", "旅の写真を、地図に貼って残すアプリ"),
]

if __name__ == "__main__":
    write("s14-sticker", S14)
    write("p01-shokai", P01)
    write("p02-mikaesanai", P02)
    subprocess.run([sys.executable, str(KIT / "render.py"), str(HERE / "html"), str(HERE.parent)], check=True, timeout=600)
