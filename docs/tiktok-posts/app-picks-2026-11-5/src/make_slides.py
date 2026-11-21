"""他社の人気アプリ＋旅行思い出マップを混ぜた「飛行機・新幹線・バス 行き方で選ぶ旅行アプリ 5選」（2026-11-21）。skill: tiktok-app-mix

    python3 make_slides.py
    python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html ..

ストアカード型。年末年始の旅行に向けて、飛行機（スカイスキャナー）・電車（乗換案内）・高速バス（WILLER TRAVEL）・
宿（楽天トラベル）・帰ってから（旅行思い出マップ）の順に並べる。5本とも役目がちがう。
前の旅行の回（app-picks-2026-10/p2-ryokou）の相手（tabiori・KKday・通貨両替電卓・Airalo）とは1本もかぶらせない。
旅行思い出マップと同じことをする競合（経県値など）は入れない。

アプリの評価・件数は assets/lookup.json（iTunes lookup、2026-11-21 取得）から読む。手で書かない。
他社アプリについて書いた文は、全部そのアプリのストアの説明文にあることだけ。使ってみた感想は書かない。
楽天トラベルの2枚目（実在の人の写真）と3枚目（「5と0のつく日」は説明文に無い）は使わない。

旅行思い出マップの絵は、ほかの回で使っていないもの（skill tiktok-slideshow 0節の5）:
  - 6478291625_detail.png  写真を開いた画面（fastlane/raw_screenshots/ja/…04_comment.png の上だけ。下のアイコン入りのコメント欄は切った）
  - 6478291625_story.png   地図をストーリーズの形で共有する画面（ShareCardStory.swift。2026-10-11 に入り、公開中の 2.1.1 にある）
ストアの1・2枚目（日本地図・群馬）は app-picks-2026-10 で使ったので外した。
説明文にある「1年の振り返り動画」は書かない。コード（YearReviewUseCase.swift）では 2025年の写真だけを対象に
2026/1/3 までの期間限定で、いまは出ない。
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
OMOIDE = 6478291625
CHIP1 = "このうち1つは、僕が作りました"


def app(track_id: int, name: str, short: str) -> dict:
    r = LOOKUP[track_id]
    icon = next(A.glob(f"icons/{track_id}.*"))
    return {"icon": icon.as_uri(), "name": name, "short": short, "maker": r["artistName"],
            "rating": r["averageUserRating"], "count": r["userRatingCount"], "own": track_id == OMOIDE}


def shot(track_id: int, n) -> str:
    return next(A.glob(f"shots/{track_id}_{n}.*")).as_uri()


def write(key: str, pages: list) -> None:
    d = SRC / "html" / key
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(pages, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


sky = app(415458524, "スカイスキャナー", "スカイ<br>スキャナー")
jorudan = app(299490481, "乗換案内", "乗換案内")
willer = app(6472978090, "WILLER TRAVEL", "WILLER<br>TRAVEL")
rakuten = app(300815151, "楽天トラベル", "楽天<br>トラベル")
omoide = app(OMOIDE, "旅行思い出マップ", "旅行思い出<br>マップ")

write("p1-ikikata", [
    m.cover("年末年始に旅行する人へ", ["飛行機・新幹線・バス", m.mark("行き方") + "で選ぶ", "旅行アプリ"], "5選", CHIP1),
    m.card("01", "飛行機で行くなら", sky, [shot(415458524, 2), shot(415458524, 1)],
           "カレンダーで、月のいちばん安い日が分かる|値段が変わったら、通知で知らせてくれる", ""),
    m.card("02", "新幹線・電車で行くなら", jorudan, [shot(299490481, 2), shot(299490481, 0)],
           "経路を調べて、そのまま新幹線や高速バスを予約|「1本後に乗りたい」も、ワンタップで調べ直せる", ""),
    m.card("03", "高速バス・夜行バスで行くなら", willer, [shot(6472978090, 0), shot(6472978090, 1)],
           "全国480路線以上の高速バス・夜行バスを予約|乗車ナビで、近くのバス停も確かめられる", ""),
    m.card("04", "泊まる宿をさがすなら", rakuten, [shot(300815151, 0), shot(300815151, 3)],
           "温泉旅館もビジネスホテルも、日程と人数で探せる|お得なクーポンやセールもチェックできる", ""),
    m.card("05", "帰ってきたら、地図に貼る", omoide, [shot(OMOIDE, "detail"), shot(OMOIDE, "story")],
           "旅先の写真が、県や市町村の形で地図に貼られる|地図は、ストーリーズの縦長の形でも共有できる", ""),
    m.recap("行き方で選ぶ旅行アプリ 5選", [sky, jorudan, willer, rakuten, omoide],
            "飛行機・新幹線・バス、どれで行きますか？", "保存して、予約する前に見返してね"),
])
print("書き出した: p1-ikikata")
