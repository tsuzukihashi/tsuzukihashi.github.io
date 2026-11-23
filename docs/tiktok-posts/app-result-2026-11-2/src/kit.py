"""app-result-2026-11 の7本で共通に使う部品。見た目は omoidemap-2026-11-2・unchikun-2026-11 と同じ
（クリーム＋方眼・紫のずらし影・Dela Gothic One・Anton）。

型は「アプリが作った結果が主役」（skill tiktok-slideshow 4-4）:
1枚目 = 結果の絵を一番大きく＋言い切り2行 → 寄りの絵 → 溜め → 問い＋アプリの札。
"""
import sys
from pathlib import Path

KIT = Path.home() / ".claude/skills/tiktok-slideshow/scripts"
sys.path.insert(0, str(KIT))
import slide_kit as k  # noqa: E402

HERE = Path(__file__).parent
FONTS = HERE / "assets/fonts"
A = "../../assets"
MAKER = "Ryo Tsudukihashi"
INK, PURPLE = "#14110c", "#8b3df5"

BRAND = {
    "background": "background-color:#f6f2ea; background-image:linear-gradient(rgba(20,17,12,.07) 2px, transparent 2px),"
                  "linear-gradient(90deg, rgba(20,17,12,.07) 2px, transparent 2px); background-size:60px 60px;",
    "fonts": [("Dela", 400, FONTS / "DelaGothicOne-Regular.ttf"),
              ("Anton", 400, FONTS / "Anton-Regular.ttf"),
              ("NotoJP", "100 900", FONTS / "NotoSansJP-VF.ttf")],
    "head_font": "Dela", "head_weight": 400, "body_font": "NotoJP",
    "ink": INK, "sub": "#6c6356", "accent": PURPLE, "mark": "#e4d4ff", "card": "#ffffff",
    "shadow": "rgba(20,17,12,.18)", "frame": "3px solid #14110c", "pop": PURPLE, "num_font": "Anton",
}
k.set_brand(BRAND)


def fsize(text: str, base: int, width: int) -> int:
    """1行に収まる文字の大きさ。Dela Gothic One は全角1字がほぼ1em、半角は0.6em前後（slide_kit の fit は大きく出すぎて1字だけ折り返した）"""
    units = sum(0.62 if ord(c) < 128 else 1.04 for c in text)
    return min(base, int(width / units))


def write(pattern: str, slides: list) -> None:
    d = HERE / "html" / pattern
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(slides, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


def img(name: str) -> str:
    return f"{A}/img/{name}"


def shot(name: str, size: str) -> str:
    """切り出した画面。size は 'width:720px' か 'height:600px'。枠とずらし影で方眼の地から浮かせる"""
    return (f'<img src="{img(name)}" style="{size};display:block;margin:0 auto;border-radius:26px;'
            f'border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE};background:#fff">')


def plain(name: str, size: str) -> str:
    """枠を付けない絵（透過のキャラ・ステッカーなど）"""
    return f'<img src="{img(name)}" style="{size};display:block;margin:0 auto">'


def row(items: list, gap: int) -> str:
    """絵を横に並べる。items は shot()/plain() の結果"""
    cells = "".join(f'<div>{x}</div>' for x in items)
    return f'<div style="display:flex;gap:{gap}px;justify-content:center;align-items:center">{cells}</div>'


def cover(small: str, big: str, hero: str) -> str:
    """1枚目。上に2行（小さい前置き＋蛍光ペンの言い切り）、その下に結果の絵を一番大きく"""
    return k.page(f"""
<div style="height:150px"></div>
<div class="badge">ひとりでアプリを作ってます</div>
<div class="cover" style="margin-top:22px;font-size:{fsize(small, 50, 780)}px">{small}</div>
<div class="cover" style="margin-top:6px;font-size:{fsize(big, 96, 760)}px">{k.mark(big)}</div>
<div style="margin-top:34px">{hero}</div>""", "")


def item(kicker: str, name: str, hero: str, main: str, sub: str) -> str:
    return k.phone_item(kicker, name, hero, main, sub)


def pause(lead: str, hero: str, punch: str) -> str:
    """溜めの1枚。前置き → 絵 → 蛍光ペンの一言（| で改行）"""
    lines = punch.split("|")
    last = lines[-1]
    head = "<br>".join(lines[:-1])
    head = f"{head}<br>" if head else ""
    return k.page(f"""
<div style="height:260px"></div>
<div class="big" style="font-size:{fsize(lead, 62, 800)}px">{lead}</div>
<div style="margin-top:50px">{hero}</div>
<div class="big" style="margin-top:50px;font-size:72px">{head}{k.mark(last)}</div>""", "")


def store_card(icon: str, label: str) -> str:
    return (f'<div style="display:flex;align-items:center;gap:22px;background:#fff;border:3px solid {INK};'
            f'border-radius:24px;box-shadow:8px 8px 0 {PURPLE};padding:14px 30px">'
            f'<img src="{img(icon)}" style="width:86px;height:86px;border-radius:23%;display:block;'
            f'border:3px solid {INK}">'
            f'<span style="text-align:left;font-size:28px;line-height:1.4">{MAKER}<br>'
            f'<span style="color:#fff;background:{PURPLE};border-radius:999px;padding:0 18px">{label}</span></span></div>')


def end(question: str, icon: str, lead: str, name: str, label: str) -> str:
    """最後の1枚。普通の問い → アイコン → 何のアプリか1行 → ストアの札 → アプリ名。
    label は札の小さいボタンの文字（無料アプリは「入手」、有料アプリは値段を書かずに「App Store」）"""
    return k.page(f"""
<div style="height:170px"></div>
<div class="big" style="font-size:{min(fsize(x, 58, 780) for x in question.split("|"))}px">{question.replace("|", "<br>")}</div>
<div style="margin-top:44px;display:flex;justify-content:center">
  <img src="{img(icon)}" style="width:260px;height:260px;border-radius:23%;display:block;border:3px solid {INK};box-shadow:10px 10px 0 {PURPLE}"></div>
<div class="subline" style="margin-top:44px;font-size:32px">{lead}</div>
<div style="margin-top:30px;display:flex;justify-content:center">{store_card(icon, label)}</div>
<div class="big" style="font-size:{fsize(name, 46, 760)}px;margin-top:22px">{k.mark(name)}</div>""", "")


def render() -> None:
    import subprocess
    subprocess.run([sys.executable, str(KIT / "render.py"), str(HERE / "html"), str(HERE.parent)], check=True, timeout=900)
