"""他社の人気アプリ＋自分のアプリを混ぜた「〇〇なアプリ X選」3本（2026-11-03）。skill: tiktok-app-mix

    python3 make_slides.py            # html/ を書き出す
    python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html ..
    python3 make_slides.py && python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html .. p2-test
    （p2-test の最後の1枚は p1・p3 の 01.png を並べるので、p1・p3 を先に撮ってから撮り直す）

推し活（推しアイランド・ストアカード）、テスト前（いつでもタイマー・〇〇編）、待ち時間のゲーム（ゼリーセイムパズル・アイコン図鑑 9:16）。
アプリの評価・件数は assets/lookup.json（iTunes lookup、2026-11-03 取得）から読む。手で書かない。
他社アプリについて書いた文は、全部そのアプリのストア説明文にあることだけ。使ってみた感想は書かない。
自作の文は、それぞれのリポジトリのコードで裏を取った:
  推しアイランド = OshiIsland（StayWidget/StayWidgetLiveActivity.swift / StayWidgetAttributes.swift の dialogue / Feature/PhotoToPixelArt）
  いつでもタイマー = PomodoroPIP（Manager/PiPManager.swift / Views/Settings/Category / Views/Report/ReportScreen.swift）
  ゼリーセイムパズル = JellySamePuzzle（GameViewModel.cycleRainbowBlock / RootView の RankingView・HighScoreUseCase）
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
OWN = {6751716346, 6443471257, 6747354292}
CHIP1 = "このうち1つは、僕が作りました"
BG = (A / "photos/18766587.jpg").as_uri()  # 夕方の駅のホーム（Pexels / Tolga Aksoy。人物は遠景のみ）


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


# ---------------------------------------------------------------- P1 ストアカード型: 推し活
weverse = app(1456559188, "Weverse", "Weverse")
joysound = app(502359087, "キョクナビJOYSOUND", "キョクナビ<br>JOYSOUND")
uchiwa = app(6443780213, "ファンサください！", "ファンサ<br>ください！")
widgetclub = app(1580284904, "WidgetClub", "WidgetClub")
oshi = app(6751716346, "推しアイランド", "推しアイランド")

write("p1-oshi", [
    m.cover("推しがいる人へ", ["推しと過ごす", m.mark("時間が増える"), "アプリ"], "5選", CHIP1),
    m.card("01", "推しの日常が届く", weverse, [shot(1456559188, 2), shot(1456559188, 3)],
           "推しの日常やニュース、LIVE配信が見られます|世界中のファンの言葉は、自動で翻訳されます", ""),
    m.card("02", "推しの動画を背景に歌う", joysound, [shot(502359087, 0), shot(502359087, 2)],
           "スマホが、お店のカラオケのリモコンになります|好きな動画や写真を、カラオケの背景に出せます", ""),
    m.card("03", "会いに行く日のうちわ", uchiwa, [shot(6443780213, 0), shot(6443780213, 1)],
           "名前うちわもファンサうちわも、テンプレートから|ぷくぷく文字やグリッター、韓国語のフォントも", ""),
    m.card("04", "ホーム画面を好きな画像に", widgetclub, [shot(1580284904, 1), shot(1580284904, 3)],
           "好きな画像で動く壁紙を設定できます|ウィジェットは100種類以上、アイコンも1万件以上", ""),
    m.card("05", "画面の上の黒いところに推し", oshi, [shot(6751716346, 0), shot(6751716346, 2)],
           "写真1枚からドット絵を作って、画面の上に置けます|長押しすると、推しがひとこと言います", ""),
    m.recap("推しと過ごす時間が増えるアプリ 5選", [weverse, joysound, uchiwa, widgetclub, oshi],
            "あなたの推しは、だれですか？", "保存して、推し活のときに見てね"),
])

# ---------------------------------------------------------------- P3 アイコン図鑑 9:16: 待ち時間のゲーム
blockblast = app(1617391485, "ブロックブラスト", "ブロックブラスト")
nanpure = app(1193508329, "ナンプレ", "ナンプレ")
tetris = app(1491074310, "Tetris", "Tetris")
pokopoko = app(888615473, "LINE ポコポコ", "LINE ポコポコ")
jelly = app(6747354292, "ゼリーセイムパズル", "ゼリーセイム<br>パズル")
dsoli = app(6475757306, "Disney Solitaire", "Disney<br>Solitaire")
noutore = app(1579132658, "毎日 脳トレ", "毎日 脳トレ")
screwdom = app(6740043080, "Screwdom", "Screwdom")
dtb = app(1173389241, "どうぶつタワーバトル", "どうぶつタワーバトル")

GAMES = [  # (app, 一覧の札（11字まで）, 1枚のひとこと, [画面], 札) 他社の札は、そのアプリのストア説明文にあることだけ
    (blockblast, "8×8に置いて消す", "置いて、そろえて、消す", [shot(1617391485, 0), shot(1617391485, 3)],
     "8×8の盤面にブロックを並べて、そろった列を消します|日替わりのパズルと、エンドレスのハイスコア挑戦"),
    (nanpure, "数字パズルの定番", "紙と鉛筆の、あのナンプレ", [shot(1193508329, 1), shot(1193508329, 3)],
     "初心者から達人級まで、難しさを選べます|ヒントや、ミスの自動チェックも付いています"),
    (tetris, "オフラインでも遊べる", "公式のテトリス", [shot(1491074310, 1), shot(1491074310, 2)],
     "積む。消す。繰り返す。公式のテトリスです|オフラインでも、いつでもどこでも遊べます"),
    (pokopoko, "動物の3マッチ", "かわいい動物の3マッチ", [shot(888615473, 1), shot(888615473, 3)],
     "うさぎやくまの動物ブロックをそろえて消します|期間限定のイベントステージがたくさん"),
    (jelly, "つなげてタップで消す", "ぷるぷるをつなげて消す", [shot(6747354292, 0), shot(6747354292, 2)],
     "同じ色が2つ以上つながったら、タップで消せます|ランキングで、世界中の人とスコアを競えます"),
    (dsoli, "ディズニーの名場面", "ソリティアにディズニー", [shot(6475757306, 0), shot(6475757306, 1)],
     "勝つたびに、ディズニーとピクサーの名場面が開きます|トライピークス式のソリティアです"),
    (noutore, "1日5分で脳を診断", "1日5分で脳を測る", [shot(1579132658, 1), shot(1579132658, 2)],
     "1問5分の脳トレで、脳のレベルを測定します|26種類の脳トレ。スタンプを押すと種類が増えます"),
    (screwdom, "ネジを色ごとに外す", "ネジを色ごとに外す", [shot(6740043080, 0), shot(6740043080, 2)],
     "ピンに刺さったネジを、同じ色の箱へ移します|時間制限なし。自分のペースで解けます"),
    (dtb, "積んで落とした方が負け", "積んで、落としたら負け", [shot(1173389241, 2), shot(1173389241, 3)],
     "順番に動物を積んで、先に落とした方の負け|オンラインで対戦。通信制限中でも遊べます"),
]
write("p3-game", [
    m.tall_cover(BG, "待ち時間に開くゲーム 9選", "9つのうち1つは、僕が作りました"),
    m.tall_grid(BG, [(a, label) for a, label, *_ in GAMES]),
    *[m.tall_card(f"{i}", "9", catch, a, shots, note) for i, (a, _, catch, shots, note) in enumerate(GAMES, 1)],
    m.tall_reveal(BG, [jelly], "このうち1つは|僕がひとりで作りました",
                  "アプリを100本以上、ひとりで作っています|気になったら名前で探してみてね"),
])

# ---------------------------------------------------------------- P2 〇〇編型: テスト前
mikan = app(920856839, "mikan", "mikan")
eigonotomo = app(1222472255, "英語の友", "英語の友")
wordholic = app(1434981148, "WordHolic", "WordHolic")
kobun = app(946696486, "古文・漢文", "古文・漢文")
timer = app(6443471257, "いつでもタイマー", "いつでも<br>タイマー")

tiles = [(p.as_uri(), c) for p, c in ((OUT / "p1-oshi/01.png", "推し活のアプリ"),
                                      (OUT / "p3-game/01.png", "待ち時間のゲーム")) if p.exists()]
write("p2-test", [
    m.cover("テストが近い人へ", ["テスト勉強が", m.mark("はかどる"), "アプリ"], "5選", CHIP1),
    m.section(["1. 英語編", "2. 暗記編", "3. 時間をはかる編", "の順で紹介します"], "英語編", [
        m.block("1.", mikan, "英単語を発音つきで|サクサク暗記。ターゲットや|パス単など200冊以上", True),
        m.block("2.", eigonotomo, "旺文社の本の音声が|聴ける。スロー再生も、|オフラインの再生もできる", False),
    ]),
    m.section([], "暗記編", [
        m.block("3.", wordholic, "自分で単語帳を作る。|フォルダに分けて、|無料で好きなだけ作れる", True),
        m.block("4.", kobun, "古文単語272と助動詞、|漢文の句法。定期試験と|共通テストに出るところ", False),
    ]),
    m.card("5.", "タイマーが画面に残る", timer, [shot(6443471257, 1), shot(6443471257, 0)],
           "ほかのアプリを開いていても、タイマーが残ります|カテゴリ分けと、達成したタイマーのレポートも", "時間をはかる編"),
    m.thanks("最後まで見てくれてありがとう", "個人開発をしています|人気のアプリと、自分で作ったアプリを|まぜて紹介しています",
             tiles, "保存して見返してね"),
])
print("書き出した: p1-oshi / p2-test / p3-game")
