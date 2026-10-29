"""他社の人気アプリ＋自分のアプリを混ぜた「〇〇なアプリ5選」3本（2026-10-29）。skill: tiktok-app-mix

    python3 make_slides.py            # html/ を書き出す
    python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html ..
    python3 make_slides.py && python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html .. p2-live
    （p2-live の最後の1枚は p1・p3 の 01.png を並べるので、p1・p3 を先に撮ってから撮り直す）

季節に合わせた3本: 寒くなってきた冬の朝（Monivo）、年末のライブ（TicketMania）、来年の手帳を選ぶ時期（めくるん）。
アプリの評価・件数は assets/lookup.json（iTunes lookup、2026-10-29 取得）から読む。手で書かない。
他社アプリについて書いた文は、全部そのアプリのストア説明文にあることだけ。使ってみた感想は書かない。
自作の文は、それぞれのリポジトリのコードで裏を取った:
  Monivo = Monivo（AlarmKitScheduler / RecordingViewModel の上限 / フレンドへ送る声）
  TicketMania = TicketMania（PostView の非公開トグル / PostViewModel のハッシュタグ）
  めくるん = Mekulun（tearPageUseCase / Rokuyo.swift / Quote.swift / CalendarEventUseCase の EKEventStore）
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/tiktok-app-mix/scripts"))
import mix_kit as m  # noqa: E402

SRC = Path(__file__).resolve().parent
A = SRC / "assets"
OUT = SRC.parent
m.setup(A / "fonts", A / "chara")

LOOKUP = {r["trackId"]: r for r in json.loads((A / "lookup.json").read_text())["results"]}
OWN = {6793626358, 6444087177, 6761456691}
CHIP1 = "このうち1つは、僕が作りました"


def app(track_id: int, name: str, short: str) -> dict:
    r = LOOKUP[track_id]
    icon = next(A.glob(f"icons/{track_id}.*"))
    return {"icon": icon.as_uri(), "name": name, "short": short, "maker": r["artistName"],
            "rating": r["averageUserRating"], "count": r["userRatingCount"], "own": track_id in OWN}


def shot(track_id: int, n: int) -> str:
    return next(A.glob(f"shots/{track_id}_{n}.*")).as_uri()


def write(key: str, pages: list) -> None:
    d = SRC / "html" / key
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.html"):
        old.unlink()
    for i, html in enumerate(pages, 1):
        (d / f"{i:02d}.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- P1 ストアカード型: 冬の朝
tenki = app(433865746, "tenki.jp", "tenki.jp")
navi = app(365876050, "NAVITIME", "NAVITIME")
radiko = app(370515585, "radiko", "radiko")
psleep = app(1579464667, "Pokémon Sleep", "Pokémon<br>Sleep")
monivo = app(6793626358, "Monivo", "Monivo")

write("p1-fuyu-asa", [
    m.cover("寒くて布団から出られない人へ", ["冬の朝が", m.mark("ちょっとラク"), "になるアプリ"], "5選", CHIP1),
    m.card("01", "眠りが浅いときに起こす", psleep, [shot(1579464667, 1), shot(1579464667, 0)],
           "スマホを枕元に置いて眠るだけで計測します|眠りが浅いときに鳴るスマートアラームつき", ""),
    m.card("02", "1時間ごとの気温が分かる", tenki, [shot(433865746, 0), shot(433865746, 3)],
           "1時間ごとの気温と降水確率が見られます|日本気象協会の公式。2週間先の予報まで", ""),
    m.card("03", "電車が止まっても迂回できる", navi, [shot(365876050, 1), shot(365876050, 2)],
           "電車が止まると、AIが迂回ルートを説明します|号車ごとの混雑予測も見られます", ""),
    m.card("04", "聴き逃した番組をあとで聴く", radiko, [shot(370515585, 2), shot(370515585, 3)],
           "全国の民放99局とNHKのラジオが聴けます|7日以内の番組は、タイムフリーで聴けます", ""),
    m.card("05", "大好きな人の声で起きる", monivo, [shot(6793626358, 0), shot(6793626358, 1)],
           "恋人や友達が録った声で、アラームが鳴ります|アプリを閉じていても、マナーモードでも鳴ります", ""),
    m.recap("冬の朝がちょっとラクになるアプリ 5選", [psleep, tenki, navi, radiko, monivo],
            "冬の朝、何時に起きていますか？", "保存して、寒い朝に見てね"),
])

# ---------------------------------------------------------------- P3 ストアカード型: 来年の手帳
timetree = app(952578473, "TimeTree", "TimeTree")
lifebear = app(538340426, "Lifebear", "Lifebear")
caho = app(1459080258, "Cahoカレンダー", "Caho<br>カレンダー")
gcal = app(909319292, "Google カレンダー", "Google<br>カレンダー")
mekulun = app(6761456691, "めくるん", "めくるん")

write("p3-techo", [
    m.cover("来年の手帳を選ぶ前に", ["来年の", m.mark("手帳になる"), "アプリ"], "5選", CHIP1),
    m.card("01", "予定をふたりで共有する", timetree, [shot(952578473, 1), shot(952578473, 2)],
           "家族や恋人、職場とカレンダーを共有できます|だれかが予定を足すと、通知が届きます", ""),
    m.card("02", "ToDoも日記もひとつに", lifebear, [shot(538340426, 1), shot(538340426, 3)],
           "カレンダーとToDo・ノート・日記がひとつに|着せかえとスタンプで、手帳みたいに飾れます", ""),
    m.card("03", "かわいい絵のカレンダー", caho, [shot(1459080258, 1), shot(1459080258, 2)],
           "イラストレーターCahoさんの絵で飾れます|予定ごとに色分け。3日間の表示が見やすい", ""),
    m.card("04", "予約が自動で入る", gcal, [shot(909319292, 0), shot(909319292, 3)],
           "Gmailに届いた予約が、自動で予定に入ります|月・週・日の表示をすぐ切り替えられます", ""),
    m.card("05", "毎朝ビリッとめくる", mekulun, [shot(6761456691, 0), shot(6761456691, 1)],
           "下に引っぱると、紙がビリッと破れてめくれます|六曜と日替わりの名言、iPhoneの予定も出ます", ""),
    m.recap("来年の手帳になるアプリ 5選", [timetree, lifebear, caho, gcal, mekulun],
            "来年の予定、どこに書きますか？", "保存して、手帳を選ぶ日に見てね"),
])

# ---------------------------------------------------------------- P2 〇〇編型: 年末のライブ
eplus = app(465887673, "e+（イープラス）", "e+")
lawson = app(1175974437, "ローチケ電子チケット", "ローチケ")
yjnorikae = app(291676451, "Yahoo!乗換案内", "Yahoo!乗換案内")
wni = app(302955766, "ウェザーニュース", "ウェザーニュース")
ticket = app(6444087177, "TicketMania", "TicketMania")

tiles = [(p.as_uri(), c) for p, c in ((OUT / "p1-fuyu-asa/01.png", "冬の朝のアプリ"),
                                      (OUT / "p3-techo/01.png", "来年の手帳のアプリ")) if p.exists()]
write("p2-live", [
    m.cover("年末のライブに行く人へ", ["ライブの", m.mark("前と当日"), "に入れるアプリ"], "5選", CHIP1),
    m.section(["1. チケットを取る編", "2. 当日編", "3. 終わったあと編", "の順で紹介します"], "チケットを取る編", [
        m.block("1.", eplus, "先行受付や抽選結果を|通知でお知らせ。発売日は|アプリの優先レーンあり", True),
        m.block("2.", lawson, "スマホがチケットになる。|同行者のスマホにも|かんたんに受け渡せる", False),
    ]),
    m.section([], "当日編", [
        m.block("3.", yjnorikae, "目的地に近い出口まで|案内してくれる。到着前に|アラームも設定できる", True),
        m.block("4.", wni, "近づいてくる雨雲を、|5分ごとのアニメで表示。|1kmごとの細かい予報", False),
    ]),
    m.card("5.", "終わったチケットを残す", ticket, [shot(6444087177, 0), shot(6444087177, 1)],
           "チケットを、写真とひとことで残せます|ハッシュタグで分けて、非公開にもできます", "終わったあと編"),
    m.thanks("最後まで見てくれてありがとう", "個人開発をしています|人気のアプリと、自分で作ったアプリを|まぜて紹介しています",
             tiles, "保存して見返してね"),
])
print("書き出した: p1-fuyu-asa / p2-live / p3-techo")
