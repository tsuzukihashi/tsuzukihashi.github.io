"""他社の人気アプリ＋自分のアプリを混ぜた「〇〇なアプリ X選」3本（2026-11-05）。skill: tiktok-app-mix

    python3 make_slides.py            # html/ を書き出す
    python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html ..
    python3 make_slides.py && python3 ~/.claude/skills/tiktok-slideshow/scripts/render.py html .. p2-nenga
    （p2-nenga の最後の1枚は p1・p3 の 01.png を並べるので、p1・p3 を先に撮ってから撮り直す）

誕生日（バースデームーン・ストアカード）、年賀状とクリスマスカード（フチドリ！・〇〇編）、コードを書く人（WidgetQiita・アイコン図鑑 9:16）。
アプリの評価・件数は assets/lookup.json（iTunes lookup、2026-11-05 取得）から読む。手で書かない。
他社アプリについて書いた文は、全部そのアプリのストア説明文にあることだけ。使ってみた感想は書かない。
自作の文は、それぞれのリポジトリのコードで裏を取った:
  バースデームーン = birthdaymoon（Entity/MoonType.swift の6種類 / ContentView.swift の mixColors・DatePinView・ImageRenderer）
  フチドリ！ = fuchidori（Presentation/Views/Editor/EditorView.swift の VNGenerateForegroundInstanceMaskRequest・borderWidth・applyBorder・pngData・PHPhotoLibrary）
  WidgetQiita = qiita-widget（Shared/Repository/ItemRepository.swift の WidgetDayType today/weekly/monthly / FavoriteTag ターゲット / HistoryItem.isFavorite）
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
OWN = {6737449860, 6748528617, 1585253685}
CHIP1 = "このうち1つは、僕が作りました"
BG = (A / "photos/25437427.jpg").as_uri()  # 暗い机とモニター（Pexels / So Phors。人物なし）


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


# ---------------------------------------------------------------- P1 ストアカード型: 誕生日
kinen = app(988424260, "記念日°", "記念日°")
chatgpt = app(6448311069, "ChatGPT", "ChatGPT")
hotpepper = app(290033990, "ホットペッパーグルメ", "ホットペッパー<br>グルメ")
canva = app(897446215, "Canva", "Canva")
moon = app(6737449860, "バースデームーン", "バースデー<br>ムーン")

write("p1-birthday", [
    m.cover("誕生日を祝う人へ", ["大切な人の", m.mark("誕生日に"), "使うアプリ"], "5選", CHIP1),
    m.card("01", "あと何日かを毎日知らせる", kinen, [shot(988424260, 0), shot(988424260, 3)],
           "誕生日までのカウントダウンを、毎日知らせます|ウィジェットに置けて、iCloudにバックアップも", ""),
    m.card("02", "プレゼントのアイデアを相談", chatgpt, [shot(6448311069, 3), shot(6448311069, 1)],
           "誕生日のプレゼントのアイデアを探せます|グリーティングカードも作ってもらえます", ""),
    m.card("03", "お祝いのディナーを予約", hotpepper, [shot(290033990, 0), shot(290033990, 3)],
           "誕生日や記念日のディナーのお店を探して予約|サプライズができるお店も、アプリ限定クーポンも", ""),
    m.card("04", "カードも招待状もテンプレから", canva, [shot(897446215, 1), shot(897446215, 2)],
           "招待状やチラシのテンプレートが、何千種類も|写真の編集もコラージュも、これひとつで", ""),
    m.card("05", "ふたりの誕生日カラーで月を作る", moon, [shot(6737449860, 0), shot(6737449860, 1)],
           "366日ぶんの誕生日カラーで、月の画像を作れます|ふたりの色を混ぜた月も。壁紙やSNSに", ""),
    m.recap("大切な人の誕生日に使うアプリ 5選", [kinen, chatgpt, hotpepper, canva, moon],
            "次に祝う誕生日は、だれのですか？", "保存して、誕生日の前に見返してね"),
])

# ---------------------------------------------------------------- P3 アイコン図鑑 9:16: コードを書く人
gemini = app(6477489729, "Google Gemini", "Gemini")
github = app(1477376905, "GitHub", "GitHub")
notion = app(1232780281, "Notion", "Notion")
claude = app(6473753684, "Claude", "Claude")
wq = app(1585253685, "WidgetQiita", "WidgetQiita")
termius = app(549039908, "Termius", "Termius")
notebook = app(6737527615, "Gemini Notebook", "Gemini<br>Notebook")
discord = app(985746746, "Discord", "Discord")
slack = app(618783545, "Slack", "Slack")

DEV = [  # (app, 一覧の札（11字まで）, 1枚のひとこと, [画面], 札) 他社の札は、そのアプリのストア説明文にあることだけ
    # 名前が2行（Gemini<br>Notebook）のものは真ん中の段に置く。下の段は札が名前の下に来るので2行目が隠れる
    (gemini, "画面を見せて相談", "画面を見せながら相談できる", [shot(6477489729, 1), shot(6477489729, 2)],
     "Gemini Liveで、画面やカメラを共有して相談|コードの記述も、データの分析もできます"),
    (github, "外でもレビューできる", "レビューもマージも外から", [shot(1477376905, 2), shot(1477376905, 3)],
     "IssueやPull Requestを読んで、返信できます|レビューとマージも、スマホから"),
    (notion, "メモもタスクも1か所", "メモもタスクも1か所に", [shot(1232780281, 1), shot(1232780281, 2)],
     "メモ、ドキュメント、タスクを1か所にまとめます|個人の利用は無料。学生も無料です"),
    (notebook, "資料を読ませて質問", "資料を読ませて質問する", [shot(6737527615, 1), shot(6737527615, 2)],
     "PDFやWebサイト、YouTubeの動画を読み込ませます|答えには出典が付き、音声の解説も聴けます"),
    (wq, "記事がホーム画面に", "エンジニアの記事がホーム画面に", [shot(1585253685, 0), shot(1585253685, 3)],
     "Qiitaのホットな記事を、ウィジェットで毎日|期間は1日・1週間・1か月。好きなタグだけも"),
    (termius, "サーバーに1タップ", "サーバーに1タップでつなぐ", [shot(549039908, 0), shot(549039908, 3)],
     "スマホからサーバーに、SSHで1タップ接続|よく使うコマンドを保存して、1タップで実行"),
    (claude, "バグを見つけて直す", "コードのバグを見つけて直す", [shot(6473753684, 1), shot(6473753684, 3)],
     "コードをレビューして、バグを修正します|100以上の言語を翻訳。文章作成やリサーチも"),
    (discord, "仲間と集まる場所", "仲間と集まる場所", [shot(985746746, 0), shot(985746746, 3)],
     "テキストも音声も、呼び出しなしで出入りできます|自分のスペースを作って、コミュニティにも"),
    (slack, "チームの連絡を集約", "チームの連絡をまとめる", [shot(618783545, 0), shot(618783545, 1)],
     "チームのメッセージと通話を、ここに集約します|会話はトピックやプロジェクトごとに整理"),
]
write("p3-code", [
    m.tall_cover(BG, "コードを書く人のアプリ 9選", "9つのうち1つは、僕が作りました"),
    m.tall_grid(BG, [(a, label) for a, label, *_ in DEV]),
    *[m.tall_card(f"{i}", "9", catch, a, shots, note) for i, (a, _, catch, shots, note) in enumerate(DEV, 1)],
    m.tall_reveal(BG, [wq], "このうち1つは|僕がひとりで作りました",
                  "iPhoneアプリを100本以上、ひとりで作っています|気になったら名前で探してみてね"),
])

# ---------------------------------------------------------------- P2 〇〇編型: 年賀状とクリスマスカード
pinterest = app(429047995, "Pinterest", "Pinterest")
phonto = app(438429273, "Phonto", "Phonto")
shimauma = app(1531076582, "しまうまプリント", "しまうま<br>プリント")
okuru = app(1294508767, "OKURU", "OKURU")
fuchi = app(6748528617, "フチドリ！", "フチドリ！")

tiles = [(p.as_uri(), c) for p, c in ((OUT / "p1-birthday/01.png", "誕生日のアプリ"),
                                      (OUT / "p3-code/01.png", "コードを書く人のアプリ")) if p.exists()]
write("p2-nenga", [
    m.cover("カードを手作りする人へ", ["年賀状も", m.mark("クリスマスカードも"), "作れるアプリ"], "5選", CHIP1),
    m.section(["1. デザイン編", "2. 刷る・贈る編", "3. もうひと手間編", "の順で紹介します"], "デザイン編", [
        m.block("1.", pinterest, "画像検索でアイデア探し。|気に入った画像はワンタップ|で保存、ボードに整理できる", True),
        m.block("2.", phonto, "写真に文字を入れる。|日本語フォント40種類で、|縦書きもメッセージカードも", False),
    ]),
    m.section([], "刷る・贈る編", [
        m.block("3.", shimauma, "写真プリントが1枚6円から。|カメラのキタムラなら|最短1時間で受け取れる", True),
        m.block("4.", okuru, "写真を12枚選ぶだけで|家族カレンダーに。|年末年始の贈り物にも", False),
    ]),
    m.card("5.", "写真を切り抜いて縁取り", fuchi, [shot(6748528617, 0), shot(6748528617, 2)],
           "写真を選ぶと、スマホの中だけで背景を切り抜きます|好きな色と太さで縁取って、透過PNGで保存", "もうひと手間編"),
    m.thanks("最後まで見てくれてありがとう", "個人開発をしています|人気のアプリと、自分で作ったアプリを|まぜて紹介しています",
             tiles, "保存して、年末に見返してね"),
])
print("書き出した: p1-birthday / p2-nenga / p3-code")
