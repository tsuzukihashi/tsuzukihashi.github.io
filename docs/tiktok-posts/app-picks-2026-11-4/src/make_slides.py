"""他社の人気アプリ＋StepLens を混ぜた「いつもの散歩が楽しくなるアプリ 5選」（2026-11-10）。skill: tiktok-app-mix

    python3 make_slides.py
    python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html ..

ストアカード型。貯まる（トリマ）・数える（歩数計Maipo）・道を選ぶ（ALKOO）・育てる（PixelPot）・見つける（StepLens）で、5本とも役目がちがう。
StepLens と同じく「お題で写真を撮る」アプリは入れない（比べられて終わる）。
アプリの評価・件数は assets/lookup.json（iTunes lookup、2026-11-10 取得）から読む。手で書かない。
他社アプリについて書いた文は、全部そのアプリのストアの説明文にあることだけ。使ってみた感想は書かない。
StepLens は伊藤さん（Shizuna Itoh）名義の、仲間と作っているアプリ。名乗りは「仲間と作りました」（own_label）。
StepLens の文は App Store の説明文で確かめた（毎日お題が届く・見つけたら撮って投稿・ほかの人の投稿も見られる）。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/tiktok-app-mix/scripts"))
import mix_kit as m  # noqa: E402

SRC = Path(__file__).resolve().parent
A = SRC / "assets"
m.setup(A / "fonts", A / "chara")

LOOKUP = {r["trackId"]: r for r in json.loads((A / "lookup.json").read_text())["results"]}
STEPLENS = 6520386794
CHIP1 = "このうち1つは、仲間と作りました"


def app(track_id: int, name: str, short: str) -> dict:
    r = LOOKUP[track_id]
    icon = next(A.glob(f"icons/{track_id}.*"))
    d = {"icon": icon.as_uri(), "name": name, "short": short, "maker": r["artistName"],
         "rating": r["averageUserRating"], "count": r["userRatingCount"], "own": track_id == STEPLENS}
    if track_id == STEPLENS:
        d["own_label"] = "仲間と作りました"
    return d


def shot(track_id: int, n: int) -> str:
    return next(A.glob(f"shots/{track_id}_{n}.*")).as_uri()


def write(key: str, pages: list) -> None:
    d = SRC / "html" / key
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(pages, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


torima = app(1502193377, "トリマ", "トリマ")
maipo = app(1053295462, "歩数計Maipo", "歩数計<br>Maipo")
alkoo = app(911333356, "ALKOO", "ALKOO")
pixelpot = app(6758675804, "PixelPot", "PixelPot")
steplens = app(STEPLENS, "StepLens", "StepLens")

write("p1-sanpo", [
    m.cover("毎日歩く人へ", ["いつもの散歩が", m.mark("楽しくなる"), "アプリ"], "5選", CHIP1),
    m.card("01", "歩くと、ポイントが貯まる", torima, [shot(1502193377, 1), shot(1502193377, 3)],
           "移動した距離や、1日の歩数でマイルが貯まります|貯めたマイルは、電子マネーやポイントと交換", ""),
    m.card("02", "持って歩くだけで、歩数を数える", maipo, [shot(1053295462, 1), shot(1053295462, 2)],
           "ポケットに入れて歩くだけで、歩数を自動で計測|ひと月の歩数は、カレンダーでひと目で分かる", ""),
    m.card("03", "日陰の多い道を選んで歩く", alkoo, [shot(911333356, 1), shot(911333356, 0)],
           "日陰を優先したルートを、地図に出してくれます|歩きたい歩数を入れると、散歩ルートも作れる", ""),
    m.card("04", "歩いた分だけ、植物が育つ", pixelpot, [shot(6758675804, 1), shot(6758675804, 2)],
           "毎日の歩数で、植物が芽吹いて花を咲かせます|ホーム画面のウィジェットで、育つ様子を眺められる", ""),
    m.card("05", "毎日のお題を、探して歩く", steplens, [shot(STEPLENS, 0), shot(STEPLENS, 1)],
           "毎日届くお題を見つけたら、写真を撮って投稿|ほかの人が見つけた景色も見られます", ""),
    m.recap("いつもの散歩が楽しくなるアプリ 5選", [torima, maipo, alkoo, pixelpot, steplens],
            "今日は、何歩歩きましたか？", "保存して、散歩に出る前に見返してね"),
])
print("書き出した: p1-sanpo")
