"""TsuzuKit の個人開発アカウントで、7本のアプリを1本ずつ宣伝する（2026-11-23 作成・第2週ぶん）。4:5。

  ./src/crop.sh                            # 生の画面（assets/raw）から切り出す
  /usr/bin/python3 src/make_slides.py      # PIL があるのは /usr/bin/python3（Homebrew の 3.15 には無い）

型は app-result-2026-11 と同じ「アプリが作った結果が主役」（skill tiktok-slideshow 4-4）。部品 kit.py はそのまま写した。
画面はどれも各アプリのストア撮影の見本のデータ（本人の記録ではない）。スライドで「僕の記録」とは言わず、固定コメントで見本だと書く。
生の画面は assets/raw/ に置いた。どこから持ってきたかは posts.json の research に書いた。

使わなかったもの（有料の機能・個人名）:
- めくるん 03_themes・04_japanese … 和風・レトロなどのテーマは有料（CalendarTheme.swift:17-21）
- Kimochi 04_calendar・03_insights・05_dressup … カレンダーは Pro の人だけに出る（CalendarView.swift:11-15）。分析とかんむりも Pro。06_private は「りょうさん」の名前
- まばたき暗算 03_steps・04_custom … 枚数が足りたので使わない
- FlowerLens 03_language … 育て方は有料（ResultView.swift careSection）
- BirdLens 03_candidates・04_ecology … 有料
- 思い出カレンダー 03_notify・05_stamp・04_detail の「1年前の今日」 … 有料。寄りの絵はスタンプの写らない列（水〜土）だけ切った
"""
from kit import cover, end, item, render, shot, write  # noqa: F401

# ---------------------------------------------------------------- めくるん
MK = [
    cover("日めくりを下に引っぱると", "ビリッと破れる", shot("mk-tear.png", "height:620px")),
    item("毎朝の1枚に", "六曜と日替わりの名言", shot("mk-page.png", "height:470px"),
         "大安・友引などの六曜と、|その日の名言がのる。", "iPhoneのカレンダーの予定ものる。"),
    item("破った紙は", "すてずに重なっていく", shot("mk-stack.png", "height:470px"),
         "めくった紙が、|1枚ずつ積み重なる。", "破り方で、破れ方が変わる。"),
    item("重なった紙を開くと", "あの日の名言とメモ", shot("mk-detail.png", "width:600px"),
         "めくった日の名言とメモを、|あとから読み返せる。", "名言は3,278こ入っている。"),
    end("毎朝、日めくりを|めくっていますか？", "icon-mekurun.jpg", "引っぱって破る日めくりカレンダー", "めくるん", "入手"),
]

# ---------------------------------------------------------------- ふみばこ（有料アプリ）
FB = [
    cover("年賀状の宛名を、iPhoneから", "縦書きで印刷", shot("fb-card.png", "height:620px")),
    item("郵便番号を入れると", "住所が出てくる", shot("fb-postal.png", "height:470px"),
         "7桁を入れると、|都道府県から町まで出る。", "データはアプリの中。通信はしない。"),
    item("住所録は", "グループで分けられる", shot("fb-book.png", "width:560px"),
         "年賀状・親せき・仕事など。|出した・届いたの印もつく。", "連絡先やCSVからも読みこめる。"),
    item("はがきも封筒も", "用紙は6つから", shot("fb-paper.png", "height:470px"),
         "はがき・往復はがき・封筒4種。|下見と同じ大きさで印刷する。", "番地の数字は漢数字になる。"),
    end("今年の年賀状、|何枚書きますか？", "icon-fumibako.jpg", "宛名を縦書きで印刷する住所録", "ふみばこ", "App Store"),
]

# ---------------------------------------------------------------- Kimochi
KM = [
    cover("きもちを毎日タップしていくと", "36日つづいた", shot("km-home.png", "width:740px")),
    item("気分は", "5つからタップ", shot("km-record.png", "width:700px"),
         "5段階の気分をタップするだけ。|モチが同じ表情にかわる。", "タグやひとことは、書きたいときだけ。"),
    item("何してた？は", "12のタグから", shot("km-tags.png", "width:700px"),
         "仕事・友達・食事・睡眠など。|当てはまるものを選ぶ。", "ひとことのメモも残せる。"),
    item("記録したきもちは", "ホームにならぶ", shot("km-today.png", "width:740px"),
         "時間とタグとひとことが、|その日のカードに残る。", "記録はこの端末の中だけ。"),
    end("今日のきもちは、|5つのうちどれですか？", "icon-kimochi.jpg", "白いおもちのモチとつける気分日記", "Kimochi", "入手"),
]

# ---------------------------------------------------------------- まばたき暗算（有料アプリ）
MB = [
    cover("パッと出て消える数字を、頭の中で", "ぜんぶ足す", shot("mb-flash.png", "width:740px")),
    item("5問こたえると", "ステップ24合格", shot("mb-summary.png", "width:600px"),
         "5問中4問正解で、|次のステップへ。", "フラッシュは60段まである。"),
    item("耳で聞いて足す", "読み上げ算も", shot("mb-listen.png", "width:640px"),
         "「願いましては」から、|そろばん教室の読み方で。", "読み上げ算は24段。速さは3つ。"),
    item("答えるたびに", "2週間のグラフに", shot("mb-records.png", "height:480px"),
         "正解とまちがいの数が、|ひと目で分かる。", "記録は iCloud で同期される。"),
    end("暗算、何桁までなら|できますか？", "icon-mabataki.jpg", "フラッシュ暗算と読み上げ算の練習アプリ", "まばたき暗算", "App Store"),
]

# ---------------------------------------------------------------- FlowerLens
FL = [
    cover("道ばたの花を撮るだけで", "バラと分かる", shot("fl-result.png", "height:620px")),
    item("誕生日を選ぶと", "その日の誕生花", shot("fl-birth.png", "height:500px"),
         "6月1日はバラ。|花言葉は「愛」「美」。", "誕生日のプレゼント選びにも。"),
    item("月を選ぶと", "その月に咲く花", shot("fl-calendar.png", "height:500px"),
         "6月に咲く花が、|花言葉といっしょにならぶ。", "季節ごとに咲く花を確かめられる。"),
    item("撮った花は", "図鑑にたまる", shot("fl-collection.png", "height:500px"),
         "識別した花は、|自動で図鑑に入る。", "世界の花 約3,000種に対応。"),
    end("あなたの誕生花、|知っていますか？", "icon-flowerlens.jpg", "撮るだけで花の名前が分かる図鑑", "FlowerLens", "入手"),
]

# ---------------------------------------------------------------- BirdLens
BL = [
    cover("公園の鳥を撮ったら、数秒で", "カワセミと出た", shot("bl-result.png", "width:720px")),
    item("鳥を見つけたら", "枠に入れて撮る", shot("bl-camera.png", "height:500px"),
         "カメラを向けて撮るだけ。|アルバムの写真からも。", "無料で識別できるのは2回まで。"),
    item("名前のほかに", "体長と分類も", shot("bl-info.png", "width:740px"),
         "体長・季節・分類が出る。|AIの自信の度合いも。", "ちがったら、正しい名前を登録できる。"),
    item("見つけた鳥は", "図鑑にたまる", shot("bl-collection.png", "height:500px"),
         "撮った鳥は、|自動で図鑑に入る。", "お気に入りに印をつけられる。"),
    end("最近、名前の分からない鳥を|見かけましたか？", "icon-birdlens.jpg", "撮るだけで野鳥の名前が分かる図鑑", "BirdLens", "入手"),
]

# ---------------------------------------------------------------- 思い出カレンダー
DS = [
    cover("1日1枚、写真をのこしていくと", "10月が写真で埋まる", shot("ds-home.png", "height:620px")),
    item("その日のマスに", "毎日ちがう1枚", shot("ds-week.png", "height:500px"),
         "景色・ペット・ごはん。|その日の写真がマスに入る。", "日記の文章が苦手でも、写真1枚でいい。"),
    item("日付を押すと", "その日の1枚が開く", shot("ds-overlay.png", "height:480px"),
         "大きな写真と、|ひとことのメモ。", "撮った場所も残せる。"),
    item("今日の1枚は", "＋から足す", shot("ds-add.png", "width:700px"),
         "＋を押して、|今日の写真を1枚えらぶ。", "無料で30日ぶん残せる。"),
    end("今日、写真を1枚|撮りましたか？", "icon-omoide.jpg", "1日1枚の写真でつける日記", "思い出カレンダー", "入手"),
]

POSTS = {
    "p1-mekurun": MK, "p2-fumibako": FB, "p3-kimochi": KM, "p4-mabataki": MB,
    "p5-flowerlens": FL, "p6-birdlens": BL, "p7-omoide": DS,
}

if __name__ == "__main__":
    for key, slides in POSTS.items():
        write(key, slides)
    render()
