#!/usr/bin/env python3
"""assets/data/app-ranking.json から /portfolio/ranking/ のページを生成する

データの取り方:
  App Store Connect → トレンド → 売上 → ユニット数 → 期間「全期間」→ コンテンツ
  の一覧をコピーして、開発者名が Ryo Tsudukihashi の App 行だけを JSON に落とす。
  Appleの画面表示は3桁に丸められている（211K など）ので、ここでの数値も概数。
"""
import html
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "portfolio", "ranking", "index.html")

with open(os.path.join(REPO, "assets", "data", "app-ranking.json"), encoding="utf-8") as f:
    DATA = json.load(f)


# 英語表示のアプリ名。US ストアの英語名（assets/data/apps_en.json）を app_id で引き、
# id の無い Android の行や配信終了のアプリは下の表から引く
with open(os.path.join(REPO, "assets", "data", "apps_en.json"), encoding="utf-8") as f:
    APPS_EN = json.load(f)["apps"]
NAMES_EN = {
    "パンケーキ屋さん": "Pancake Shop",
    "星防衛": "Star Defense",
    "うんちくん": "UNCHIKUN",
    "あなたレシート": "YOU Receipt",
    "旅行思い出マップ": "TravelMemoryMap",
    "nokki - 音楽ジャーナル": "nokki - Music Journal",
    "猫背改善と姿勢リマインダー": "Posture Reminder: Cat Coach",
    "Yattayo やったよボード": "Yattayo: Slider To-Do Board",
    "Monivo 声で起こし合うアラーム": "Monivo: Wake Up by Voice",
    "パタパタ推し時計": "Oshi Clock: Flip Photo Widget",
    "集中電鉄": "Focus Railway - Study Timer",
    "足利工業大学スクールバス": "Ashikaga Tech School Bus",
}


def app_name(a):
    """日本語の名前は英語名と並べる。英語名が無いまま日本語を出すと WARN を出す"""
    en = APPS_EN.get(str(a.get("app_id")), {}).get("name") or NAMES_EN.get(a["name"])
    if not en:
        if any("\u3040" <= ch <= "\u9fff" for ch in a["name"]):
            print("WARN: 英語名がありません:", a["name"])
        return esc(a["name"])
    if en == a["name"]:
        return esc(en)
    return f'<span class="i18n-ja">{esc(a["name"])}</span><span class="i18n-en">{esc(en)}</span>'


def esc(s):
    return html.escape(str(s or ""))


def jp_units(n):
    """1万以上は「◯.◯万」、それ未満はカンマ区切り"""
    if n >= 10000:
        man = n / 10000
        return f"{man:.1f}万".replace(".0万", "万")
    return f"{n:,}"


def en_units(n):
    """英語表示用。1万以上は千の位で丸めて「◯K」（日本語の「◯.◯万」と同じ細かさ）、それ未満はカンマ区切り"""
    if n >= 10000:
        return f"{round(n / 1000):,}K"
    return f"{n:,}"


def units(n):
    """日本語と英語の両方を並べる（lang.js が片方を隠す）"""
    return f'<span class="i18n-ja">{jp_units(n)}</span><span class="i18n-en">{en_units(n)}</span>'


apps = DATA["apps"]
top = apps[0]["units"]

# 見た目はガチャ（assets/css/gacha.css・g-apps.css、docs/gacha-design.md）。ヘッダーとフッターは scripts/gacha_shell.py
sys.path.insert(0, os.path.join(REPO, "scripts"))
import gacha_shell as gs  # noqa: E402

CAPS = ["var(--g-c3)", "var(--g-c1)", "var(--g-c6)"]


def bi(ja, en):
    return gs.bi(ja, en)


def podium_card(i, a):
    icon = (f'<img src="{esc(a["icon_url"])}" alt="" width="512" height="512" loading="lazy">'
            if a["icon_url"] else '<span class="ga-rk-noicon">—</span>')
    tag, close = ((f'<a class="g-panel ga-podium ga-podium--{a["rank"]}" href="{esc(a["app_store_url"])}" target="_blank" rel="noopener">', "</a>")
                  if a["app_store_url"] else (f'<div class="g-panel ga-podium ga-podium--{a["rank"]}">', "</div>"))
    return f'''                {tag}
                    <span class="ga-podium-rank" style="--c:{CAPS[i]}"><span>{a["rank"]}</span></span>
                    <div class="ga-podium-icon">{icon}</div>
                    <h3>{app_name(a)}</h3>
                    <div class="ga-podium-units">{units(a["units"])}</div>
                    <div class="ga-podium-label">{bi("ダウンロード", "Downloads")}</div>
                {close}'''


top3 = apps[:3]
# PC では 2位・1位・3位の順に並べて、1位を真ん中に置く（スマホでは1位が先頭。g-apps.css）
podium = [podium_card(i, a) for i, a in [(1, top3[1]), (0, top3[0]), (2, top3[2])]]

rows = []
for a in apps[3:]:
    pct = max(a["units"] / top * 100, 0.6)
    icon = (f'<img src="{esc(a["icon_url"])}" alt="" width="512" height="512" loading="lazy">'
            if a["icon_url"] else f'<span class="ga-rk-noicon">{bi("終", "—")}</span>')
    ended = "" if a["icon_url"] else f'<span class="ga-rk-ended">{bi("配信終了", "Discontinued")}</span>'
    inner = f'''<span class="ga-rk-rank">{a["rank"]}</span>
                    <span class="ga-rk-icon">{icon}</span>
                    <span class="ga-rk-name">{app_name(a)}{ended}</span>
                    <span class="ga-rk-bar"><i style="width: {pct:.1f}%;"></i></span>
                    <span class="ga-rk-units">{units(a["units"])}</span>'''
    if a["app_store_url"]:
        rows.append(f'                <a class="ga-rk-row" href="{esc(a["app_store_url"])}" target="_blank" rel="noopener">\n                    {inner}\n                </a>')
    else:
        rows.append(f'                <div class="ga-rk-row ga-rk-row--ended">\n                    {inner}\n                </div>')

AND = DATA.get("android") or {}
android_rows = []
if AND:
    a_top = max(r["installs"] for r in AND["apps"])
    for a in AND["apps"]:
        pct = max(a["installs"] / a_top * 100, 0.6)
        icon = (f'<img src="{esc(a["icon_url"])}" alt="" width="512" height="512" loading="lazy">'
                if a["icon_url"] else '<span class="ga-rk-noicon">—</span>')
        android_rows.append(f'''                <a class="ga-rk-row" href="{esc(a["play_url"])}" target="_blank" rel="noopener">
                    <span class="ga-rk-rank">{a["rank"]}</span>
                    <span class="ga-rk-icon">{icon}</span>
                    <span class="ga-rk-name">{app_name(a)}<span class="ga-rk-sub">{bi(f"いま{a['active_devices']:,}台", f"{a['active_devices']:,} active devices")}</span></span>
                    <span class="ga-rk-bar ga-rk-bar--and"><i style="width: {pct:.1f}%;"></i></span>
                    <span class="ga-rk-units">{units(a["installs"])}</span>
                </a>''')

ANDROID_SECTION = ""
if AND:
    ANDROID_SECTION = f'''
                <div class="g-sh">
                    <h2>Google Play</h2>
                    <small>{bi(f"Android {AND['app_count']}本", f"{AND['app_count']} Android apps")}</small>
                </div>
                <p class="ga-rk-sublead i18n-ja">
                    Androidにも{AND["app_count"]}本出しています。こちらも配信開始からの<strong>累計インストール数</strong>で、
                    合計{AND["total_installs"]:,}。いま動いている端末は{AND["total_active"]:,}台です。
                </p>
                <p class="ga-rk-sublead i18n-en">
                    I've also released {AND["app_count"]} apps on Android. These are <strong>total installs</strong> since launch as well,
                    {AND["total_installs"]:,} in all. {AND["total_active"]:,} devices are running them right now.
                </p>
                <div class="g-panel ga-rk-list">
{chr(10).join(android_rows)}
                </div>
'''

HTML = f'''<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="/assets/js/lang.js"></script>
        <meta name="title-en" content="Download Ranking - Ryo Tsuzukihashi">
        <meta name="description-en" content="The {DATA['app_count']} apps I've released on the App Store, ranked by total downloads. {DATA['total_units']:,} downloads in all.">
        <title>ダウンロードランキング - Ryo Tsuzukihashi</title>
        <meta name="description"
            content="App Storeで配信した{DATA['app_count']}本のアプリを、累計ダウンロード数の多い順に並べました。合計{DATA['total_units']:,}ダウンロード。">
        <meta name="keywords" content="Ryo Tsuzukihashi, iOSアプリ, ダウンロード数, ランキング, 個人開発">

        <!-- OGP -->
        <meta property="og:title" content="ダウンロードランキング - Ryo Tsuzukihashi">
        <meta property="og:description"
            content="{DATA['app_count']}本のアプリを累計ダウンロード数の多い順に。合計{DATA['total_units']:,}ダウンロード。">
        <meta property="og:image" content="https://tsuzukit.com/assets/images/ogp/portfolio.png">
        <meta property="og:image:width" content="1200">
        <meta property="og:image:height" content="630">
        <meta property="og:url" content="https://tsuzukit.com/portfolio/ranking/">
        <meta property="og:type" content="website">

        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@tsuzuki817">
        <meta name="twitter:title" content="ダウンロードランキング - Ryo Tsuzukihashi">
        <meta name="twitter:description" content="{DATA['app_count']}本のアプリを累計ダウンロード数の多い順に。">
        <meta name="twitter:image" content="https://tsuzukit.com/assets/images/ogp/portfolio.png">

        <!-- Favicon -->
        <link rel="icon" type="image/x-icon" href="/favicon.ico">
        <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png">
        <!-- 背景を抜いているので、暗いタブバーでは黒が溶ける。そこだけ白抜きに差し替える -->
        <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-dark-32x32.png" media="(prefers-color-scheme: dark)">
        <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-dark-16x16.png" media="(prefers-color-scheme: dark)">

        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-QERPQ1EGLH"></script>
        <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-QERPQ1EGLH');
    </script>

        <!-- Google AdSense（持ち主の確認だけ。このページに広告は出さない。docs/ads.md） -->
        <meta name="google-adsense-account" content="ca-pub-8240751277462688">

        {gs.head_links(("/assets/css/g-apps.css",)).replace(chr(10) + "    ", chr(10) + "        ")}
    </head>
    <body class="g">
        {gs.header("/portfolio/")}

        <main class="g-main">
            <div class="g-wrap">
                <nav class="g-crumb" aria-label="パンくず" data-en-aria-label="Breadcrumb"><a href="/">{bi("トップ", "Home")}</a><span>＞</span><a href="/portfolio/">{bi("ラインナップ", "Lineup")}</a><span>＞</span><b>{bi("ダウンロードランキング", "Download Ranking")}</b></nav>

                <section class="ga-rk-hero">
                    <div>
                        <h1 class="g-title i18n-ja">どれが一番<br>使われているか</h1>
                        <h1 class="g-title i18n-en">Which ones<br>get used the most</h1>
                        <p class="g-bubble i18n-ja">
                            App Storeに出した{DATA['app_count']}本を、配信開始から今日までの累計ダウンロード数で並べました。<br>
                            Google Playの分も下にまとめています。
                        </p>
                        <p class="g-bubble i18n-en">
                            Here are the {DATA['app_count']} apps I've released on the App Store, ranked by total downloads from launch to today.<br>
                            The Google Play numbers are further down.
                        </p>
                    </div>
                    <div class="g-ypanel ga-rk-total">
                        <span>Total Downloads</span>
                        <b>{DATA['grand_total']:,}</b>
                        <em>App Store {DATA['total_units']:,} ＋ Google Play {DATA['android']['total_installs']:,}</em>
                    </div>
                </section>

                <div class="ga-podiums">
                    <img class="ga-podium-char" src="/assets/images/character-cheer.png" alt="" width="318" height="315">
{chr(10).join(podium)}
                </div>

                <div class="g-panel ga-rk-list">
{chr(10).join(rows)}
                </div>
{ANDROID_SECTION}
                <div class="g-paper ga-rk-note">
                    <p class="i18n-ja">
                        App Store Connectのトレンド（ユニット数・全期間）から取っています。Appleの表示が3桁に丸められているため、
                        1万を超えるものは概数です。アプリ内課金の販売数と、他の開発者名義で預かっているアプリは含めていません。
                        アイコンのない行は配信を終了したアプリです。Google Playの数字はPlay Consoleのインストールレポートを全期間ぶん合算したものです。
                        最終更新は{DATA['generated_at']}。
                    </p>
                    <p class="i18n-en">
                        These figures come from App Store Connect Trends (units, all time). Apple rounds what it shows to three digits,
                        so anything over 10,000 is approximate. In-app purchase sales and apps I look after under other developers' names are not included.
                        Rows without an icon are apps that are no longer available. The Google Play figures are the Play Console install reports added up over all time.
                        Last updated {DATA['generated_at']}.
                    </p>
                    <a class="g-btn" href="/portfolio/">&larr; {bi("ポートフォリオに戻る", "Back to the portfolio")}</a>
                </div>
            </div>
        </main>

        {gs.footer()}
    </body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wrote {OUT}")
print(f"  {DATA['app_count']}本 / 合計 {DATA['total_units']:,}")

# ガチャのレア度（apps.json の download_count）・トップと私についての DL 数を、このランキングの数字にそろえる
import subprocess
subprocess.run([sys.executable, os.path.join(REPO, "scripts", "apply_ranking_downloads.py")], check=True)
subprocess.run([sys.executable, os.path.join(REPO, "scripts", "apply_download_totals.py")], check=True)
subprocess.run([sys.executable, os.path.join(REPO, "scripts", "build_top_apps.py")], check=True)
