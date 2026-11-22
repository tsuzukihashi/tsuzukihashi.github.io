"""TsuzuKit の個人開発アカウントで、うんちくんを宣伝する1本（2026-11-22）。4:5。

  /usr/bin/python3 src/make_slides.py      # PIL があるのは /usr/bin/python3（Homebrew の 3.15 には無い）

p01-renzoku  記録を続けた「結果」が主役（skill tiktok-slideshow 4-4）。
             ホームの「今日のうんち 4回・100日連続中」→ 回数で変わるキャラ → 10回をこえると → ステータス → うんちタイプ → 問い。

画面は PoopCounter の撮影用モード（`-videoCapture`、DEBUG だけ。Firestore には書かない）で
2026-11-22 にシミュレータで撮った。数字はモックのダミー（連続100日・累計350回・Lv.12）なので、
スライドでも説明文でも「僕の記録」とは言わない。「続けると、こうなる」の見せ方にする。
うんちタイプの絵は Storage にあるものと同じ PoopCounter/docs/verify/types/webp/MFPR-A.webp を、アプリのキャッシュに置いて出した。
キャラの絵は PoopCounter/PoopCounter/Assets.xcassets/funny/ の実物。回数との対応は DesignSystem/PooCountImage.swift の imageNames(for:)。
年間うんレポ（12月に開く・サポーター限定）は、明日見た人がすぐ使えないので入れない。
見た目は omoidemap-2026-11-2 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
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

# 1日の回数 → キャラ（PooCountImage.imageNames(for:) の中から1つずつ）
BY_COUNT = [("1回", "chef"), ("2回", "detective"), ("3回", "pirate"),
            ("4回", "boxing"), ("5回", "superhero"), ("6回", "rocket"),
            ("7回", "king"), ("8回", "celebration"), ("9回", "dizzy")]


def write(pattern: str, slides: list) -> None:
    d = HERE / "html" / pattern
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(slides, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


def img(name: str) -> str:
    return f"{A}/img/{name}"


def shot(name: str, width: int) -> str:
    """切り出した画面。幅で大きさを決める（横長のカードが多いので）"""
    return (f'<img src="{img(name)}" style="width:{width}px;display:block;margin:0 auto;border-radius:28px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}">')


def chara_grid() -> str:
    """1日の回数ごとに出るキャラを 3×3 で並べる"""
    cells = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center">'
        f'<img src="{img("poo_" + name + ".png")}" style="width:170px;height:118px;object-fit:contain">'
        f'<div style="font-family:Anton;font-size:30px;color:{PURPLE};margin-top:0">{label}</div></div>'
        for label, name in BY_COUNT)
    return (f'<div style="display:grid;grid-template-columns:repeat(3,190px);gap:4px 16px;justify-content:center;'
            f'background:#fff;border:3px solid {INK};border-radius:30px;box-shadow:10px 10px 0 {PURPLE};'
            f'padding:16px 26px;width:fit-content;margin:0 auto">{cells}</div>')


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


def cover() -> str:
    """1枚目。ホームのカード（回数・連続日数・キャラ）を一番大きく。文は上に2行だけ"""
    return k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:24px;font-size:52px">うんちを毎日記録していくと</div>
<div class="cover" style="margin-top:6px;font-size:104px">{k.mark("100日連続")}</div>
<div style="margin-top:40px">{shot("c-home.png", 720)}</div>""", "")


def sos() -> str:
    """溜め。10回をこえたときのキャラ（SOS・病気・とける・泣く・雨の5体。セリフは「ちょっと心配…」「病院行く？」など）"""
    return k.page(f"""
<div style="height:300px"></div>
<div class="big" style="font-size:66px">1日10回をこえると…</div>
<div style="margin-top:60px;display:flex;justify-content:center">
  <img src="{img("poo_sos.png")}" style="width:420px;display:block"></div>
<div class="big" style="margin-top:50px;font-size:72px">うんちくんに<br>{k.mark("心配される。")}</div>""", "")


def end(question: str, lead: str) -> str:
    return k.page(f"""
<div style="height:170px"></div>
<div class="big" style="font-size:58px">{question.replace("|", "<br>")}</div>
<div style="margin-top:44px;display:flex;justify-content:center">{big_icon(260)}</div>
<div class="subline" style="margin-top:44px;font-size:32px">{lead}</div>
<div style="margin-top:30px;display:flex;justify-content:center">{store_card()}</div>
<div class="big" style="font-size:46px;margin-top:22px">{k.mark("うんちくん")}</div>""", "")


P01 = [
    cover(),
    k.phone_item("1日の回数で", "うんちくんが変わる", chara_grid(),
                 "出た回数に合わせて、ちがう|うんちくんが出る。ぜんぶで37種類以上。", ""),
    sos(),
    k.phone_item("続けるほど", "数字がたまっていく", shot("c-status.png", 720),
                 "続けた日数と、記録した回数が|ずっと残る。", "記録するとレベルも上がる。"),
    k.phone_item("30日ぶんの記録から", "うんちタイプがわかる", shot("c-type.png", 490),
                 "出る時間・かたさ・回数から、|16タイプのどれかが出る。", "10回記録すると、診断できる。"),
    end("あなたのうんちは、|何タイプだと思いますか？", "うんちを記録して、友達や家族とシェアするアプリ"),
]

if __name__ == "__main__":
    write("p01-renzoku", P01)
    subprocess.run([sys.executable, str(KIT / "render.py"), str(HERE / "html"), str(HERE.parent)], check=True, timeout=600)
