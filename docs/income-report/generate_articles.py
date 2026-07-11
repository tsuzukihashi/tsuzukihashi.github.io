#!/usr/bin/env python3
"""限界個人開発者の月収１０００万円計画 の月次記事＋ハブページを生成する

文言はCLAUDE.md「文章スタイル【全文章共通・絶対遵守】」の編集ルール適用済み。
新しい月を足すときも同ルールを通した文章にすること。
"""
import os

REPO = "/Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com"
GOAL = 10_000_000

MONTHS = [
    {
        "ym": "2025-11", "date": "2025-11-30", "label": "2025年11月",
        "admob": 21074, "appstore": 16976, "play": None,
        "total": 38050, "mom": None, "rate": "0.38",
        "desc": "月収1000万円を目指す個人開発者の収益公開シリーズ、その創刊号。2025年11月の収益は38,050円。AdMobとApp Storeの内訳を眺めて、次の一手を決める。",
        "highlights": [
            ("旅行思い出マップ", "¥25,747", "広告で12,415円、サポータープランで13,332円。全収益の68%をこの1本が稼いだ。eCPMは728円と悪くない。"),
            ("流れるメモ帳", "¥7,308", "広告5,013円とサブスク2,295円。累計146万円を稼いだ看板アプリも、いまは月5千円のペース。"),
            ("その他", "¥5,000弱", "フチドリ！の買い切りが1件、スワイポンの週間プランが12件、あとは細かな広告収益。収益化できているアプリはまだ数えるほどしかない。"),
        ],
        "analysis": """
<p>創刊号の数字は月収38,050円でした。50本以上のアプリをApp Storeに並べてきて、この金額です。限界個人開発者を名乗る理由がこの表に詰まっています。</p>
<p>内訳を見ると、収益の68%を旅行思い出マップが占めています。広告のeCPMは728円と悪くない。ただ、そもそも収益化の仕組みが入っているアプリが数本しかありません。ダウンロードも月2,350件では絶対量が足りない。</p>
<p>裏を返せば伸びしろだらけです。ここから毎月、数字と向き合って次の一手を打っていきます。</p>
""",
        "next_actions": [
            "旅行思い出マップのサポータープラン導線を強化する。推すのは1年間プラン",
            "収益化が入っていないアプリに、広告かサブスクを順番に入れていく",
            "年末の振り返り需要に向けて旅行思い出マップのASOを見直す",
        ],
        "closing": "まずは月10万円。目標の1%を超えるところから始めます。",
    },
    {
        "ym": "2025-12", "date": "2025-12-31", "label": "2025年12月",
        "admob": 20777, "appstore": 60977, "play": None,
        "total": 81754, "mom": "+114.9", "rate": "0.82",
        "desc": "2025年12月の収益は81,754円で前月から2倍あまり。旅行思い出マップが年末需要でダウンロード4倍、サブスクが素直についてきた。",
        "highlights": [
            ("旅行思い出マップ", "¥67,816", "ダウンロードが前月の4.2倍、6,657件まで伸びた。1年間サポータープランが32件売れてサブスクだけで54,532円。広告は13,284円。"),
            ("流れるメモ帳", "¥7,474", "サブスク3,003円と広告4,471円。毎月ちゃんと足元を支えてくれる。"),
            ("スワイポン", "¥1,623", "写真整理アプリ。年末に容量を空けたい人が増えるのか、プレミアムプランが少しずつ動いた。"),
        ],
        "analysis": """
<p>81,754円。前月の2.1倍で、初めて月8万円台に乗りました。</p>
<p>要因ははっきりしています。旅行思い出マップのダウンロードが1,584件から6,657件まで伸びました。年末は今年の旅行を振り返りたくなる時期で、このアプリと相性がいい。そして増えたダウンロードの分だけサブスクも素直についてきた。中でも1年間サポータープランが32件売れたのが大きくて、これは1年分の売上を先にもらえる契約です。</p>
<p>一方でAdMobは20,777円と横ばいでした。広告は毎日開かれるかどうかで決まるので、ダウンロードが増えてもツール系アプリではこうなります。</p>
""",
        "next_actions": [
            "お正月も新規獲得が見込めるので、1月も手を緩めない",
            "サブスクを嫌う層に向けて、英語圏向けアプリで買い切りプランを試す",
            "うんちくんの海外展開を準備する",
        ],
        "closing": "ダウンロードが増えればサブスクは伸びる。次はそれを取り切る仕組みです。",
    },
    {
        "ym": "2026-01", "date": "2026-01-31", "label": "2026年1月",
        "admob": 22021, "appstore": 72086, "play": 102,
        "total": 94209, "mom": "+15.2", "rate": "0.94",
        "desc": "2026年1月の収益は94,209円。Google Playで初めての売上102円が立ち、英語圏では買い切りプランが動き出した。",
        "highlights": [
            ("旅行思い出マップ", "¥60,214", "ダウンロードは8,493件とさらに増加。サブスクで44,488円、広告で15,624円。そしてAndroid版がGoogle Playで初めての売上102円を記録した。"),
            ("Medicine Reminder", "¥13,272", "お薬リマインダーの英語版。買い切りプランが海外で3件売れた。単価が高いので件数が少なくても効く。"),
            ("ShellLensとFocusDrive", "¥7,443", "英語圏向けアプリの年額プランがぽつぽつ売れ始めた。"),
        ],
        "analysis": """
<p>94,209円、前月から15.2%伸びました。10万円まであと少し。</p>
<p>今月の出来事は2つあります。ひとつはGoogle Playの初売上102円。金額は小さくても、iOS一本足だった収益にAndroidという2本目の足が生えました。</p>
<p>もうひとつは、先月仕込んだ買い切りプランが英語圏で動き出したことです。Medicine Reminderで3件、13,272円。サブスクに疲れたユーザーは確実にいて、海外では買い切りの訴求がよく刺さる。この学びは後々効いてきます。</p>
<p>収益源が5本のアプリに分散し始めたのもいい兆しです。</p>
""",
        "next_actions": [
            "うんちくんに初回限定の年額ワンタイムオファーを入れる",
            "うんちくんAndroid版の収益化を進める",
            "買い切りプランをほかの英語圏向けアプリにも広げる",
        ],
        "closing": "Playストアの102円は、たぶん一生忘れない売上です。",
    },
    {
        "ym": "2026-02", "date": "2026-02-28", "label": "2026年2月",
        "admob": 69179, "appstore": 145619, "play": 204,
        "total": 215002, "mom": "+128.2", "rate": "2.15",
        "desc": "2026年2月の収益は215,002円で前月の2.3倍。うんちくんが月2万ダウンロードまで跳ね、年額ワンタイムオファーが54件刺さった。",
        "highlights": [
            ("うんちくん", "¥88,914", "ダウンロードが月20,554件まで跳ねた。年額ワンタイムオファーが54件で44,982円、広告も43,932円。一気に大黒柱になった。"),
            ("旅行思い出マップ", "¥79,376", "サブスク68,016円は過去最高。広告と合わせて2本柱の一角を守っている。"),
            ("流れるメモ帳", "¥17,506", "広告10,577円にサブスク6,929円。地味に効く3本目の柱。"),
        ],
        "analysis": """
<p>215,002円。前月の2.3倍で、初めて20万円台に乗りました。目標達成率も2%を超えています。</p>
<p>主役は完全にうんちくんです。海外でダウンロードが跳ねて月2万件。そこへ先月のNextActionで実装した年額ワンタイムオファーが54件刺さりました。毎日記録するアプリなので広告収益も同時に伸びる。ダウンロードの爆発、初回限定オファー、毎日開くアプリ。この三拍子が揃うとこうなります。</p>
<p>面白いのはうんちくんのeCPMが504円と高いことです。この時点では日本のユーザーが多かったからで、この後グローバル比率が上がるとeCPMは下がっていきます。それでも総額は伸びる。</p>
""",
        "next_actions": [
            "うんちくんの広告面を増やす。記録完了後の画面が候補",
            "うんちくんAndroid版のAdMob設定を最適化する",
            "バイラル狙いの新アプリを仕込む",
        ],
        "closing": "仕込んだ施策が数字で返ってくる。これがこの連載の醍醐味です。",
    },
    {
        "ym": "2026-03", "date": "2026-03-31", "label": "2026年3月",
        "admob": 205320, "appstore": 841236, "play": 3536,
        "total": 1050092, "mom": "+388.4", "rate": "10.50",
        "desc": "2026年3月、月収100万円を突破した。1,050,092円の内訳と、推しアイランドの買い切りプランが217本売れた顛末。",
        "highlights": [
            ("推しアイランド", "¥610,430", "ダウンロード38,595件の大バズ。約3,000円の買い切りプランが217本売れて547,103円。週間プランも1,281件動いた。単月で60万円を超えた。"),
            ("うんちくん", "¥199,091", "App Storeで61,633円、広告で134,126円、Playで3,332円。ダウンロード22,878件と成長が続く。"),
            ("猫背改善と姿勢リマインダー", "¥86,960", "買い切りが32本で81,056円。推しアイランドのバズが姉妹アプリにも波及した。"),
            ("旅行思い出マップ", "¥81,144", "サブスク69,786円。何も起きなくても月8万円を運んでくれる存在になった。"),
        ],
        "analysis": """
<p>1,050,092円。月収100万円を超えました。1000万円への道のりの1割に、一瞬だけ手が届いた月です。</p>
<p>立役者は推しアイランドです。SNSでバズってダウンロードが38,595件まで跳ね、約3,000円の買い切りプランが217本売れました。買い切りの強さは、バズの熱をその場で現金にできることです。サブスクなら初月分しか入らない熱量が、一撃で入ってくる。</p>
<p>AdMobも205,320円で過去最高でした。ただ冷静に見れば、このうち55万円はバズという花火です。花火は必ず消える。消えたあとに何が残るかは、来月の数字が教えてくれます。</p>
""",
        "next_actions": [
            "反動減に備えて、推しアイランドに週間プランの継続価値を残す",
            "うんちくんをバズに頼らないストック収益として育て続ける",
            "配信量が増えたのでAdMobのフォーマット別eCPMを見直す",
        ],
        "closing": "100万円は通過点。でも、この景色は忘れずにいたい。",
    },
    {
        "ym": "2026-04", "date": "2026-04-30", "label": "2026年4月",
        "admob": 117079, "appstore": 240396, "play": 2516,
        "total": 359991, "mom": "-65.7", "rate": "3.60",
        "desc": "2026年4月の収益は359,991円。バズの反動で減ったが、うんちくんが月17万円の柱に育った。花火とストックの違いがはっきり見えた月。",
        "highlights": [
            ("うんちくん", "¥174,115", "App Storeで86,099円、広告で86,231円、Playで1,785円。ダウンロード33,534件。正規の年額プランも32,805円売れて、単体で月17万円の柱になった。"),
            ("旅行思い出マップ", "¥71,527", "サブスク63,802円に広告とPlay分。鉄板の安定感。"),
            ("推しアイランド", "¥37,070", "買い切りは3本まで減ったが、週間プラン299件が残った。バズの置き土産。"),
        ],
        "analysis": """
<p>359,991円。3月の100万円から65.7%減りましたが、これは織り込み済みの反動です。バズ前の2月と比べれば67%増えていて、地力は確実に上がっています。</p>
<p>今月はっきりしたのは花火とストックの違いです。推しアイランドの買い切りは217本から3本まで消えました。一方で週間プラン299件は継続収益として残った。先月、継続課金の価値を残すと書いた施策が効いています。</p>
<p>そしてうんちくんが月17万円の柱に育ちました。バズに頼らず月3万ダウンロードを積み、サブスクと広告の両輪で稼ぐ。この形が理想です。</p>
""",
        "next_actions": [
            "うんちくんにAI機能を足して、単価と継続率を上げる",
            "うんちくんPlay版の課金プランを増やす",
            "月30万円台を下限として固定できるか検証する",
        ],
        "closing": "バズは水物、ストックは資産。両方追います。",
    },
    {
        "ym": "2026-05", "date": "2026-05-31", "label": "2026年5月",
        "admob": 139628, "appstore": 187643, "play": 11023,
        "total": 338294, "mom": "-6.0", "rate": "3.38",
        "desc": "2026年5月の収益は338,294円。うんちくんがAI健康記録アプリに進化し、Google Playは初めて月1万円を超えた。",
        "highlights": [
            ("うんちくん改め UNCHIKUN: Poop Log & AI Health", "¥177,806", "AI健康記録アプリに進化して名前も変えた。App Storeで62,131円、広告で106,284円、Playで9,391円。ダウンロードは36,438件。"),
            ("旅行思い出マップ", "¥76,708", "サブスク64,841円に広告とPlay分。ゴールデンウィークの旅行シーズンも追い風になった。"),
            ("Google Play全体", "¥11,023", "月間で過去最高。うんちくんの特別年額が14件売れた。Androidも売れる場所になってきた。"),
        ],
        "analysis": """
<p>338,294円。前月から6%減りましたが、月30万円台は守りました。</p>
<p>先月の宣言どおり、うんちくんにAI機能を載せてUNCHIKUN: Poop Log & AI Healthに進化させました。名前にAIを入れたことでストアでの見え方が変わり、ダウンロードは36,438件。単体で月17.8万円を稼ぎ、柱の座を固めています。</p>
<p>もうひとつのトピックはGoogle Playの月1万円超えです。1月に102円だったのが、5ヶ月で100倍になりました。特別年額のオファーが14件売れていて、Androidユーザーにも課金意欲はちゃんとあります。</p>
<p>気がかりはうんちくんのeCPMが143円まで下がったことです。2月は504円でした。海外比率が上がった影響なので成長の証ではあるものの、広告フォーマットは見直す余地があります。</p>
""",
        "next_actions": [
            "リワード広告のような高単価フォーマットの比率を上げる",
            "ペイウォールのA/BテストでPremium Monthlyの転換率を上げる",
            "Android版うんちくんの広告マッチ率32%を改善する",
        ],
        "closing": "派手さはないけど、こういう月が下限を作ってくれる。",
    },
    {
        "ym": "2026-06", "date": "2026-06-30", "label": "2026年6月",
        "admob": 141580, "appstore": 195141, "play": 5240,
        "total": 341961, "mom": "+1.1", "rate": "3.42",
        "desc": "2026年6月の収益は341,961円。うんちくんは月5万ダウンロード目前。上半期の合計240万円もあわせて振り返る。",
        "highlights": [
            ("うんちくん", "¥172,736", "ダウンロードがついに月49,363件。App Storeで47,129円、iOS広告で105,988円、Android広告で15,909円、Playで3,710円。"),
            ("旅行思い出マップ", "¥82,348", "サブスク73,086円と復調。サポータープランの安定感が光る。"),
            ("ゼリーセイムパズル", "¥8,502", "ハンマーチケットという消耗型アイテムが売れた。ゲーム内課金という新しいタイプの収益。"),
        ],
        "analysis": """
<p>341,961円。3ヶ月続けて月30万円台に乗り、下限がほぼ固まりました。</p>
<p>うんちくんのダウンロードは月49,363件。iOSとAndroidの広告、iOSとAndroidの課金という4つの財布から収益が入る、理想的なマルチプラットフォームアプリになっています。</p>
<p>ここで2026年上半期のまとめを。1月から6月の合計は2,399,549円、月平均399,925円でした。去年11月の月3.8万円から、半年ちょっとで月平均40万円のラインまで来ています。目標の1000万円にはまだ3.4%ですが、成長率で見れば悪くないペースです。</p>
<p>次の壁ははっきりしています。バズ抜きで月50万円。うんちくんの5万ダウンロードを収益に変える効率と、新しい柱の追加が鍵です。</p>
""",
        "next_actions": [
            "7月に新アプリを複数出す。CarKeepなどを準備中",
            "ASOとローカライズで、うんちくんを月5万から10万ダウンロードへ",
            "eCPM2,609円の実績があるリワードインタースティシャルの配置を広げる",
        ],
        "closing": "上半期240万円。下半期は月50万円の下限を作りに行きます。",
    },
]

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Blog | Ryo Tsuzukihashi</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="個人開発, 収益公開, 月収1000万円, iOSアプリ, AdMob, App Store, Google Play, tsuzuki817">

    <!-- OGP -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tsuzukit.com{url}">
    <meta property="og:image" content="https://tsuzukit.com/assets/images/ogp/blog.png">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-QERPQ1EGLH"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-QERPQ1EGLH');
    </script>

    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8240751277462688"
        crossorigin="anonymous"></script>

    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/blog.css">
    <style>
        .revenue-summary {{
            background: var(--color-surface);
            border: 2px solid var(--color-ink);
            box-shadow: 8px 8px 0 var(--neon-purple);
            padding: var(--spacing-xl);
            border-radius: 20px;
            text-align: center;
            margin: var(--spacing-2xl) 0;
        }}
        .revenue-summary h3 {{ font-family: var(--font-accent); font-style: italic; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--color-secondary); margin-bottom: var(--spacing-sm); }}
        .revenue-number {{ font-family: var(--font-impact); font-style: italic; font-size: 3.6rem; color: var(--color-ink); line-height: 1.1; }}
        .revenue-mom {{ font-size: var(--font-size-md); margin-top: var(--spacing-sm); color: var(--color-secondary); }}
        .goal-progress {{ margin: var(--spacing-lg) auto 0; max-width: 480px; }}
        .goal-progress-label {{ display: flex; justify-content: space-between; font-family: var(--font-accent); font-style: italic; font-weight: 700; font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--color-secondary); margin-bottom: 6px; }}
        .goal-progress-bar {{ background: var(--color-surface); border: 2px solid var(--color-ink); border-radius: 999px; height: 16px; overflow: hidden; }}
        .goal-progress-fill {{ background: var(--neon-purple); height: 100%; border-radius: 999px; min-width: 4px; }}
        .platform-table {{ width: 100%; border-collapse: collapse; margin: var(--spacing-lg) 0; border: 2px solid var(--color-ink); }}
        .platform-table th, .platform-table td {{ padding: 12px 16px; text-align: right; border-bottom: 1px solid var(--color-border); }}
        .platform-table th:first-child, .platform-table td:first-child {{ text-align: left; }}
        .platform-table th {{ background: var(--color-surface-2); font-family: var(--font-accent); font-style: italic; font-weight: 700; letter-spacing: 0.05em; font-size: 13px; color: var(--color-secondary); border-bottom: 2px solid var(--color-ink); }}
        .platform-table .total-row td {{ font-weight: 700; background: var(--color-sun-soft); border-top: 2px solid var(--color-ink); }}
        .app-highlight {{ background: var(--color-surface); border: 2px solid var(--color-ink); box-shadow: 5px 5px 0 var(--color-ink); border-radius: 16px; padding: 20px 24px; margin: 24px 0; }}
        .app-highlight.shadow-purple {{ box-shadow: 5px 5px 0 var(--neon-purple); }}
        .app-highlight.shadow-cyan {{ box-shadow: 5px 5px 0 var(--neon-cyan); }}
        .app-highlight.shadow-pink {{ box-shadow: 5px 5px 0 var(--neon-pink); }}
        .app-highlight.shadow-yellow {{ box-shadow: 5px 5px 0 var(--pop-yellow); }}
        .app-highlight-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }}
        .app-highlight-name {{ font-weight: 700; color: var(--color-primary); }}
        .app-highlight-amount {{ font-family: var(--font-impact); font-style: italic; font-size: 1.5rem; color: var(--color-ink); white-space: nowrap; }}
        .app-highlight p {{ margin: 0; font-size: 14px; color: var(--color-secondary); line-height: 1.7; }}
        .next-action-list {{ list-style: none; padding: 0; margin: var(--spacing-lg) 0; counter-reset: na; }}
        .next-action-list li {{ counter-increment: na; position: relative; background: var(--color-surface); border: 2px solid var(--color-ink); box-shadow: 4px 4px 0 var(--color-ink); border-radius: 12px; padding: 16px 20px 16px 60px; margin-bottom: 16px; font-weight: 500; }}
        .next-action-list li::before {{ content: counter(na); position: absolute; left: 18px; top: 50%; transform: translateY(-50%); width: 28px; height: 28px; border-radius: 50%; background: var(--color-ink); color: #fff; font-family: var(--font-accent); font-style: italic; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 14px; }}
        .notice-box {{ background: var(--color-surface-2); border-left: 4px solid var(--color-ink); padding: 16px 20px; border-radius: 0 8px 8px 0; font-size: 13px; color: var(--color-secondary); line-height: 1.8; margin: var(--spacing-2xl) 0 0; }}
        .series-link {{ display: block; background: var(--color-surface); border: 2px solid var(--color-ink); box-shadow: 4px 4px 0 var(--neon-cyan); border-radius: 12px; padding: 14px 20px; margin: var(--spacing-lg) 0; text-decoration: none; color: var(--color-primary); font-weight: 700; transition: transform 0.3s ease, box-shadow 0.3s ease; }}
        .series-link:hover {{ transform: translate(-3px, -3px); box-shadow: 7px 7px 0 var(--neon-pink); }}
        @media (max-width: 768px) {{
            .revenue-number {{ font-size: 2.6rem; }}
            .platform-table th, .platform-table td {{ padding: 10px 8px; font-size: 13px; }}
        }}
    </style>
</head>
"""

def build_article(i, m):
    prev_m = MONTHS[i - 1] if i > 0 else None
    next_m = MONTHS[i + 1] if i + 1 < len(MONTHS) else None
    title = f"{m['date']} 限界個人開発者の月収１０００万円計画"
    url = f"/blog/posts/income-report-{m['ym']}.html"

    def yen(v):
        return f"¥{v:,}" if v is not None else "—"

    def row(name, cur, prev, total=False):
        mom = ""
        if prev is not None and cur is not None and prev > 0:
            pct = (cur - prev) / prev * 100
            sign = "+" if pct >= 0 else ""
            mom = f"{sign}{pct:.1f}%"
        elif cur is not None and (prev is None or prev == 0):
            mom = "—"
        cls = ' class="total-row"' if total else ""
        return f"""                <tr{cls}>
                    <td>{name}</td>
                    <td>{yen(cur)}</td>
                    <td>{mom}</td>
                </tr>"""

    prev_admob = prev_m["admob"] if prev_m else None
    prev_as = prev_m["appstore"] if prev_m else None
    prev_play = prev_m["play"] if prev_m else None
    prev_total = prev_m["total"] if prev_m else None

    mom_html = ""
    if m["mom"]:
        color = "var(--neon-cyan)" if not m["mom"].startswith("-") else "var(--neon-pink)"
        mom_html = f'<div class="revenue-mom">前月比 <strong style="color:{color};">{m["mom"]}%</strong>（前月 {yen(prev_total)}）</div>'
    else:
        mom_html = '<div class="revenue-mom">シリーズ創刊号</div>'

    shadow_cycle = ["purple", "cyan", "pink", "yellow"]
    highlights_html = "\n".join(
        f"""            <div class="app-highlight shadow-{shadow_cycle[idx % 4]}">
                <div class="app-highlight-head">
                    <span class="app-highlight-name">{name}</span>
                    <span class="app-highlight-amount">{amount}</span>
                </div>
                <p>{desc}</p>
            </div>""" for idx, (name, amount, desc) in enumerate(m["highlights"]))

    actions_html = "\n".join(f"                <li>{a}</li>" for a in m["next_actions"])

    nav_prev = f'<a href="/blog/posts/income-report-{prev_m["ym"]}.html" class="nav-link-wrapper"><span>&larr; {prev_m["label"]}号</span></a>' if prev_m else ""
    nav_next = f'<a href="/blog/posts/income-report-{next_m["ym"]}.html" class="nav-link-wrapper"><span>{next_m["label"]}号 &rarr;</span></a>' if next_m else ""

    intro = ""
    if i == 0:
        intro = """
            <p>
                こんにちは、tsuzuki817（<a href="https://twitter.com/tsuzuki817" target="_blank">@tsuzuki817</a>）です。
            </p>
            <p>
                今月から新しいシリーズを始めます。名前は「限界個人開発者の月収１０００万円計画」。AdMobとApp StoreとGoogle Playの収益を毎月すべて公開して、数字を眺めて、次の一手を決める。月収1000万円に届くまで続けるつもりです。
            </p>
            <p>
                個人開発を始めたのは2016年。10年で50本以上のアプリを出してきて、初めての収益は3年目にあたる2019年7月の21円でした。そこまでの道のりは<a href="/blog/posts/income-report-prehistory.html">前史編</a>に書いています。
            </p>"""
    else:
        intro = f"""
            <p>
                こんにちは、tsuzuki817（<a href="https://twitter.com/tsuzuki817" target="_blank">@tsuzuki817</a>）です。
                収益をぜんぶ公開して次の一手を決める連載「限界個人開発者の月収１０００万円計画」、{m['label']}号です。
            </p>
            <a href="/blog/income-report/" class="series-link">📈 シリーズの全記事と推移グラフは特設ページにあります</a>"""

    play_note = ""
    if m["play"] is None:
        play_note = "Google Playの売上はまだありません。"

    html = HEAD_TEMPLATE.format(title=title, desc=m["desc"], url=url)
    html += f"""<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-container">
            <a href="/" class="nav-logo">Ryo Tsuzukihashi</a>
            <div class="nav-menu">
                <a href="/" class="nav-link">Home</a>
                <a href="/portfolio/" class="nav-link">Portfolio</a>
                <a href="/blog/" class="nav-link">Blog</a>
                <a href="/about/" class="nav-link">About</a>
                <a href="/contact/" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Blog Post -->
    <article class="blog-post">
        <header class="post-header">
            <div class="post-meta">
                <span class="post-date">{m['date'].replace('-', '.')}</span>
                <span class="post-category">月収1000万円計画</span>
                <span class="post-reading-time">5分で読める</span>
            </div>
            <h1 class="post-title">{m['date']}<br>限界個人開発者の月収１０００万円計画</h1>
        </header>

        <div class="post-content">
{intro}

            <div class="revenue-summary">
                <h3>{m['label']}の総収益</h3>
                <div class="revenue-number">¥{m['total']:,}</div>
                {mom_html}
                <div class="goal-progress">
                    <div class="goal-progress-label"><span>目標達成率</span><span>{m['rate']}% / ¥10,000,000</span></div>
                    <div class="goal-progress-bar"><div class="goal-progress-fill" style="width: {min(float(m['rate']), 100)}%;"></div></div>
                </div>
            </div>

            <h1>プラットフォーム別内訳</h1>
            <table class="platform-table">
                <thead>
                    <tr><th>プラットフォーム</th><th>収益</th><th>前月比</th></tr>
                </thead>
                <tbody>
{row('AdMob（広告）', m['admob'], prev_admob)}
{row('App Store（課金）', m['appstore'], prev_as)}
{row('Google Play（課金）', m['play'], prev_play)}
{row('合計', m['total'], prev_total, total=True)}
                </tbody>
            </table>
            <p style="font-size: 13px; color: var(--color-text-light);">{play_note}</p>

            <h1>今月のアプリ別ハイライト</h1>
{highlights_html}

            <h1>分析</h1>
{m['analysis']}

            <h1>NextAction</h1>
            <p>この数字を見て、来月やることを3つ決めました。</p>
            <ol class="next-action-list">
{actions_html}
            </ol>

            <p>{m['closing']}</p>
            <p>それでは、また来月の報告で。</p>

            <div class="notice-box">
                数値について。AdMobは管理画面の推定収益額で、確定額とは数％ずれることがあります。App Storeは手数料を引いた開発者受取額で、外貨分は月末レートで円に換算した概算を含みます。Google Playはサービス手数料を引いた受取額です。締め日の関係で、実際の振込額とは一致しません。
            </div>
        </div>

        <nav class="post-navigation">
            {nav_prev}
            <a href="/blog/income-report/" class="nav-link-wrapper"><span>シリーズ一覧</span></a>
            {nav_next}
        </nav>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3 class="footer-logo">Ryo Tsuzukihashi</h3>
                    <p class="footer-description">思い出&times;テクノロジーで新しい価値を創造</p>
                </div>
                <div class="footer-nav">
                    <a href="/legal/privacy-policy.html">プライバシーポリシー</a>
                    <a href="/legal/terms-of-service.html">利用規約</a>
                    <a href="/legal/commercial-law.html">特定商取引法</a>
                    <a href="/legal/disclaimer.html">免責事項</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Ryo Tsuzukihashi. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""
    return url, html


for i, m in enumerate(MONTHS):
    url, html = build_article(i, m)
    path = REPO + url
    with open(path, "w") as f:
        f.write(html)
    print(f"wrote {path}")

print("done")
