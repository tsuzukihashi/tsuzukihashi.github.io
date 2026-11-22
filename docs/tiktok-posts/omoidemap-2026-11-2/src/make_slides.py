"""TsuzuKit の個人開発アカウントで、旅行思い出マップを宣伝する1本（2026-11-22）。4:5。

  python3 src/make_slides.py

p01-mada28  りょうくん本人の日本地図（「フィルムで残す思い出」・都道府県 28/47）が主役。
            @tsuzuki817 で一番伸びた 2026-02-03 の動画（304,435回）が「自分の地図＋日本も広い！の一言」だったので、
            同じ作りをスライドでやる（skill tiktok-slideshow 4-4）。機能の説明を並べず、1枚の地図を寄って見せる。

絵は omoide-map/fastlane/raw_screenshots/ja/OmoideShots-17ProMax-01_japan.png の1枚から、
全体（上の県の数の表示は外す）・東日本・西日本・県の数の4か所を切り出した（同じ範囲は2回使わない）。
北海道の写真は2人が大きく写るので、寄りの絵にはしない（全体の中に小さく出るだけ）。
前の回（omoidemap-2026-11）の絵（群馬・写真一覧・北海道の札・先月のおもいで・ヨーロッパ・アメリカ・ステッカー）は使わない。
見た目は omoidemap-2026-11 と同じ（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。
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


def shot(name: str, height: int) -> str:
    """切り出した地図。白地の画面なので、枠とずらし影で方眼の地から浮かせる"""
    return (f'<img src="{img(name)}" style="height:{height}px;display:block;margin:0 auto;border-radius:24px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE};background:#f4f4f4">')


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
    """1枚目。地図を一番大きく。文は上に2行だけ（地図に重ねない）"""
    return k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:22px;font-size:50px">旅の写真を、行った県に貼ったら</div>
<div class="cover" style="margin-top:6px;font-size:104px">{k.mark("まだ28県")}</div>
<div style="margin-top:26px">{shot("z-all.png", 600)}</div>""", "")


def count() -> str:
    """溜めの1枚。地図の上に出る県の数を、そのまま大きく見せる"""
    return k.page(f"""
<div style="height:300px"></div>
<div class="big" style="font-size:66px">47のうち、まだ28。</div>
<div style="margin-top:60px">{shot("z-count.png", 150)}</div>
<div class="big" style="margin-top:80px;font-size:96px">{k.mark("日本も広い。")}</div>""", "")


def end(question: str, lead: str) -> str:
    return k.page(f"""
<div style="height:170px"></div>
<div class="big" style="font-size:58px">{question.replace("|", "<br>")}</div>
<div style="margin-top:44px;display:flex;justify-content:center">{big_icon(260)}</div>
<div class="subline" style="margin-top:44px;font-size:32px">{lead}</div>
<div style="margin-top:30px;display:flex;justify-content:center">{store_card()}</div>
<div class="big" style="font-size:46px;margin-top:22px">{k.mark("旅行思い出マップ")}</div>""", "")


P01 = [
    cover(),
    k.phone_item("行った県は", "東は、写真でいっぱい", shot("z-kanto.png", 500),
                 "行った県が、その旅の写真で|埋まっていく。", "写真は、県の形に切り抜かれる。"),
    k.phone_item("行っていない県は", "西は、ほとんど空っぽ", shot("z-west.png", 470),
                 "緑のままの県が、|まだ行っていない県。", "次にどこへ行くか、地図を見て決められる。"),
    count(),
    end("あなたの地図は、|何県うまりそうですか？", "旅の写真を、地図に貼って残すアプリ"),
]

if __name__ == "__main__":
    write("p01-mada28", P01)
    subprocess.run([sys.executable, str(KIT / "render.py"), str(HERE / "html"), str(HERE.parent)], check=True, timeout=600)
