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

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "portfolio", "ranking", "index.html")

with open(os.path.join(REPO, "assets", "data", "app-ranking.json"), encoding="utf-8") as f:
    DATA = json.load(f)


def esc(s):
    return html.escape(str(s or ""))


def jp_units(n):
    """1万以上は「◯.◯万」、それ未満はカンマ区切り"""
    if n >= 10000:
        man = n / 10000
        return f"{man:.1f}万".replace(".0万", "万")
    return f"{n:,}"


apps = DATA["apps"]
top = apps[0]["units"]

medal_shadow = ["var(--rk-purple)", "var(--rk-cyan)", "var(--rk-pink)"]

podium = []
for i, a in enumerate(apps[:3]):
    icon = (f'<img src="{esc(a["icon_url"])}" alt="" loading="lazy">'
            if a["icon_url"] else '<span class="rk-noicon">—</span>')
    link_open = f'<a class="rk-podium" href="{esc(a["app_store_url"])}" target="_blank" rel="noopener">' if a["app_store_url"] else '<div class="rk-podium">'
    link_close = "</a>" if a["app_store_url"] else "</div>"
    podium.append(f'''                {link_open}
                    <div class="rk-podium-rank">{a["rank"]}</div>
                    <div class="rk-podium-icon">{icon}</div>
                    <h3 class="rk-podium-name">{esc(a["name"])}</h3>
                    <div class="rk-podium-units">{jp_units(a["units"])}</div>
                    <div class="rk-podium-label">ダウンロード</div>
                {link_close}''')

rows = []
for a in apps[3:]:
    pct = max(a["units"] / top * 100, 0.6)
    icon = (f'<img src="{esc(a["icon_url"])}" alt="" loading="lazy">'
            if a["icon_url"] else '<span class="rk-noicon">終</span>')
    ended = "" if a["icon_url"] else '<span class="rk-ended">配信終了</span>'
    name = esc(a["name"])
    inner = f'''<span class="rk-rank">{a["rank"]}</span>
                    <span class="rk-icon">{icon}</span>
                    <span class="rk-name">{name}{ended}</span>
                    <span class="rk-bar"><i style="width: {pct:.1f}%;"></i></span>
                    <span class="rk-units">{jp_units(a["units"])}</span>'''
    if a["app_store_url"]:
        rows.append(f'                <a class="rk-row" href="{esc(a["app_store_url"])}" target="_blank" rel="noopener">\n                    {inner}\n                </a>')
    else:
        rows.append(f'                <div class="rk-row rk-row--ended">\n                    {inner}\n                </div>')

AND = DATA.get("android") or {}
android_rows = []
if AND:
    a_top = max(r["installs"] for r in AND["apps"])
    for a in AND["apps"]:
        pct = max(a["installs"] / a_top * 100, 0.6)
        icon = (f'<img src="{esc(a["icon_url"])}" alt="" loading="lazy">'
                if a["icon_url"] else '<span class="rk-noicon">—</span>')
        android_rows.append(f'''                <a class="rk-row" href="{esc(a["play_url"])}" target="_blank" rel="noopener">
                    <span class="rk-rank">{a["rank"]}</span>
                    <span class="rk-icon">{icon}</span>
                    <span class="rk-name">{esc(a["name"])}<span class="rk-sub">いま{a["active_devices"]:,}台</span></span>
                    <span class="rk-bar"><i class="rk-bar--and" style="width: {pct:.1f}%;"></i></span>
                    <span class="rk-units">{jp_units(a["installs"])}</span>
                </a>''')

ANDROID_SECTION = ""
if AND:
    ANDROID_SECTION = f'''
                <h2 class="rk-subtitle">Google Play</h2>
                <p class="rk-subnote">
                    Androidにも{AND["app_count"]}本出しています。こちらも配信開始からの<strong>累計インストール数</strong>で、
                    合計{AND["total_installs"]:,}。いま動いている端末は{AND["total_active"]:,}台です。
                </p>
                <div class="rk-list rk-list--android">
{chr(10).join(android_rows)}
                </div>
'''

HTML = f'''<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
            href="https://fonts.googleapis.com/css2?family=Anton&family=Saira+Condensed:wght@600;700;800&family=Noto+Sans+JP:wght@400;500;700;900&display=swap"
            rel="stylesheet">

        <!-- CSS -->
        <link rel="stylesheet" href="../../assets/css/memories-tech.css">

        <!-- Favicon -->
        <link rel="icon" href="../../favicon.ico">

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

        <style>
            :root {{
                --rk-bg: #f6f2ea;
                --rk-ink: #14110c;
                --rk-muted: #57514a;
                --rk-purple: #8b3df5;
                --rk-cyan: #0bb4c4;
                --rk-pink: #ff3d7f;
                --rk-yellow: #ffc107;
            }}
            .rk-page {{ background: var(--rk-bg); color: var(--rk-ink); }}
            .rk-wrap {{ max-width: 960px; margin: 0 auto; padding: 0 20px; }}

            .rk-hero {{ padding: 120px 0 56px; text-align: center; }}
            .rk-badge {{
                display: inline-block; font-family: 'Saira Condensed', sans-serif; font-style: italic;
                font-weight: 800; letter-spacing: 0.16em; font-size: 0.85rem; color: var(--rk-purple);
                margin-bottom: 14px;
            }}
            .rk-title {{
                font-family: 'Anton', 'Noto Sans JP', sans-serif; font-style: italic;
                font-size: clamp(2.4rem, 6vw, 4rem); line-height: 1.05; margin-bottom: 18px;
            }}
            .rk-lead {{ color: var(--rk-muted); font-size: 1rem; line-height: 1.8; }}
            .rk-total {{
                display: inline-block; margin-top: 26px; background: #fff;
                border: 2px solid var(--rk-ink); border-radius: 18px; box-shadow: 8px 8px 0 var(--rk-ink);
                padding: 18px 30px;
            }}
            .rk-total b {{
                display: block; font-family: 'Anton', sans-serif; font-style: italic;
                font-size: 2.6rem; line-height: 1;
            }}
            .rk-total span {{
                font-family: 'Saira Condensed', sans-serif; font-style: italic; font-weight: 700;
                letter-spacing: 0.1em; font-size: 0.8rem; color: var(--rk-muted); text-transform: uppercase;
            }}

            .rk-total em {{ display: block; margin-top: 8px; font-style: normal; font-size: 0.78rem; color: var(--rk-muted); }}
            .rk-sub {{ display: block; font-size: 0.72rem; color: var(--rk-muted); margin-top: 2px; }}
            .rk-podiums {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 10px 0 50px; }}
            .rk-podium {{
                background: #fff; border: 2px solid var(--rk-ink); border-radius: 20px;
                padding: 26px 18px 22px; text-align: center; text-decoration: none; color: inherit;
                position: relative; display: block; transition: transform 0.2s ease;
            }}
            .rk-podium:nth-child(1) {{ box-shadow: 9px 9px 0 var(--rk-ink); }}
            .rk-podium:nth-child(2) {{ box-shadow: 9px 9px 0 var(--rk-ink); }}
            .rk-podium:nth-child(3) {{ box-shadow: 9px 9px 0 var(--rk-ink); }}
            .rk-podium:hover {{ transform: translateY(-4px); }}
            .rk-podium-rank {{
                font-family: 'Anton', sans-serif; font-style: italic; font-size: 2.2rem;
                line-height: 1; color: var(--rk-ink); margin-bottom: 12px;
            }}
            .rk-podium-icon img {{ width: 84px; height: 84px; border-radius: 20px; border: 2px solid var(--rk-ink); display: block; margin: 0 auto 14px; }}
            .rk-podium-name {{ font-size: 0.95rem; font-weight: 700; line-height: 1.5; margin-bottom: 10px; min-height: 2.9em; }}
            .rk-podium-units {{ font-family: 'Anton', sans-serif; font-style: italic; font-size: 1.9rem; line-height: 1; }}
            .rk-podium-label {{
                font-family: 'Saira Condensed', sans-serif; font-style: italic; font-weight: 700;
                font-size: 0.72rem; letter-spacing: 0.1em; color: var(--rk-muted);
                text-transform: uppercase; margin-top: 6px;
            }}

            .rk-list {{
                background: #fff; border: 2px solid var(--rk-ink); border-radius: 20px;
                box-shadow: 8px 8px 0 var(--rk-ink); overflow: hidden;
            }}
            .rk-row {{
                display: grid; grid-template-columns: 44px 44px minmax(0, 1fr) 150px 84px;
                align-items: center; gap: 14px; padding: 12px 20px;
                border-bottom: 1px solid rgba(20, 17, 12, 0.1);
                text-decoration: none; color: inherit;
            }}
            .rk-row:last-child {{ border-bottom: none; }}
            .rk-row:hover {{ background: #faf7f1; }}
            .rk-row--ended {{ color: var(--rk-muted); }}
            .rk-rank {{ font-family: 'Anton', sans-serif; font-style: italic; font-size: 1.15rem; text-align: right; }}
            .rk-icon img {{ width: 40px; height: 40px; border-radius: 10px; border: 1px solid rgba(20,17,12,0.16); display: block; }}
            .rk-noicon {{
                display: flex; align-items: center; justify-content: center; width: 40px; height: 40px;
                border-radius: 10px; border: 1px dashed rgba(20,17,12,0.3); font-size: 0.75rem; color: var(--rk-muted);
            }}
            .rk-name {{ font-size: 0.92rem; font-weight: 500; line-height: 1.45; overflow-wrap: anywhere; }}
            .rk-ended {{
                display: inline-block; margin-left: 8px; font-size: 0.68rem; padding: 1px 7px;
                border: 1px solid rgba(20,17,12,0.25); border-radius: 999px; color: var(--rk-muted); white-space: nowrap;
            }}
            .rk-bar {{ display: block; height: 10px; background: rgba(20,17,12,0.08); border-radius: 999px; overflow: hidden; }}
            .rk-bar i {{ display: block; height: 100%; background: var(--rk-ink); border-radius: 999px; }}
            .rk-units {{ font-family: 'Saira Condensed', sans-serif; font-style: italic; font-weight: 800; font-size: 1rem; text-align: right; white-space: nowrap; }}

            .rk-subtitle {{
                font-family: 'Anton', 'Noto Sans JP', sans-serif; font-style: italic;
                font-size: clamp(1.6rem, 4vw, 2.2rem); margin: 56px 0 10px;
            }}
            .rk-subnote {{ color: var(--rk-muted); font-size: 0.9rem; line-height: 1.8; margin-bottom: 20px; }}
            .rk-subnote strong {{ color: var(--rk-ink); }}
            .rk-list--android {{ box-shadow: 8px 8px 0 var(--rk-ink); }}
            .rk-bar--and {{ background: var(--rk-cyan) !important; }}
            .rk-note {{ margin: 28px 0 90px; font-size: 0.8rem; line-height: 1.9; color: var(--rk-muted); }}
            .rk-back {{ display: inline-block; margin-top: 18px; font-weight: 700; color: var(--rk-purple); text-decoration: none; }}
            .rk-back:hover {{ text-decoration: underline; }}

            @media (max-width: 720px) {{
                .rk-hero {{ padding: 100px 0 40px; }}
                .rk-podiums {{ grid-template-columns: 1fr; gap: 16px; margin-bottom: 36px; }}
                .rk-podium-name {{ min-height: 0; }}
                .rk-row {{ grid-template-columns: 34px 36px minmax(0, 1fr) 68px; gap: 10px; padding: 11px 14px; }}
                .rk-bar {{ display: none; }}
                .rk-icon img, .rk-noicon {{ width: 36px; height: 36px; }}
                .rk-name {{ font-size: 0.86rem; }}
                .rk-units {{ font-size: 0.9rem; }}
            }}
        </style>
    </head>
    <body class="rk-page">
        <!-- Navigation -->
        <nav class="nav" id="nav">
            <div class="nav-container">
                <a href="/" class="nav-logo">TsuzuKit</a>
                <div class="nav-menu" id="navMenu">
                    <a href="/portfolio/" class="nav-link active">Portfolio</a>
                    <a href="/about/" class="nav-link">About</a>
                    <a href="/blog/" class="nav-link">Blog</a>
                    <a href="/contact/" class="nav-link">Contact</a>
                </div>
                <div class="nav-toggle" id="navToggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </nav>

        <main>
            <section class="rk-hero">
                <div class="rk-wrap">
                    <span class="rk-badge">Download Ranking</span>
                    <h1 class="rk-title">どれが一番<br>使われているか</h1>
                    <p class="rk-lead">
                        App Storeに出した{DATA['app_count']}本を、配信開始から今日までの累計ダウンロード数で並べました。<br>
                        Google Playの分も下にまとめています。
                    </p>
                    <div class="rk-total">
                        <b>{DATA['grand_total']:,}</b>
                        <span>Total Downloads</span>
                        <em>App Store {DATA['total_units']:,} ＋ Google Play {DATA['android']['total_installs']:,}</em>
                    </div>
                </div>
            </section>

            <div class="rk-wrap">
                <div class="rk-podiums">
{chr(10).join(podium)}
                </div>

                <div class="rk-list">
{chr(10).join(rows)}
                </div>
{ANDROID_SECTION}

                <p class="rk-note">
                    App Store Connectのトレンド（ユニット数・全期間）から取っています。Appleの表示が3桁に丸められているため、
                    1万を超えるものは概数です。アプリ内課金の販売数と、他の開発者名義で預かっているアプリは含めていません。
                    アイコンのない行は配信を終了したアプリです。Google Playの数字はPlay Consoleのインストールレポートを全期間ぶん合算したものです。
                    最終更新は{DATA['generated_at']}。
                    <br>
                    <a class="rk-back" href="/portfolio/">&larr; ポートフォリオに戻る</a>
                </p>
            </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-container">
                <div class="footer-content">
                    <div class="footer-brand">
                        <a href="/" class="footer-logo">TsuzuKit</a>
                        <p class="footer-tagline">Memories × Technology</p>
                    </div>
                    <div class="footer-links">
                        <a href="/portfolio/">Portfolio</a>
                        <a href="/about/">About</a>
                        <a href="/blog/">Blog</a>
                        <a href="/contact/">Contact</a>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p>&copy; 2026 Ryo Tsuzukihashi. All rights reserved.</p>
                </div>
            </div>
        </footer>
    </body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wrote {OUT}")
print(f"  {DATA['app_count']}本 / 合計 {DATA['total_units']:,}")
