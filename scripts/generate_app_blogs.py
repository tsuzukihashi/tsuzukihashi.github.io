#!/usr/bin/env python3
"""
43アプリのブログ紹介ページを生成する。
App Storeの説明文(description)をそのまま忠実にHTMLに変換する。
嘘や創作は一切含めない。

日本語と英語を1ページに並べて出す（出し分けは assets/js/lang.js、決めごとは docs/i18n.md）。
英語の名前と説明文は assets/data/apps_en.json（scripts/fetch_apps_en.py で US ストアから取得）を使う。
US ストアに英語の説明文が無いアプリだけ、日本語を英訳したものが "source": "translated" で入っている。
"""

import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'assets/data/apps.json')) as f:
    data = json.load(f)

APPS = data['apps']

with open(os.path.join(BASE_DIR, 'assets/data/apps_en.json'), encoding='utf-8') as f:
    APPS_EN = json.load(f)['apps']

# ============================================================
# スラッグ定義（ファイル名用）
# ============================================================

SLUG_MAP = {
    "見守りリマインダー - みまもり": "mimamori-reminder",
    "記念日リマインダー - メモリア": "memoria-anniversary",
    "猫背改善と姿勢リマインダー：猫背は猫だけで充分にゃ。": "nekoze-posture-reminder",
    "推しアイランド": "oshi-island",
    "目薬リマインダー ~ EyeDrop 点眼管理 ~": "eyedrop-reminder",
    "思い出カレンダー - 1日1枚フォト日記": "omoide-calendar",
    "ShellLens - 貝殻AI図鑑": "shelllens",
    "BeautyMed - 美容医療リマインダー": "beautymed",
    "BirdLens - 野鳥AI図鑑": "birdlens",
    "GeoLens - 岩石・鉱物AI図鑑": "geolens",
    "馬券ジェネレーター": "baken-generator",
    "お薬リマインダー 服用管理": "okusuri-reminder",
    "リマインダー 記憶を呼び起こす": "memory-reminder",
    "FocusDrive - 集中タイマー": "focusdrive",
    "空想旅行カメラ - AIで世界をスナップ": "daydream-camera",
    "スワイポン - スワイプで写真と動画を簡単整理": "swaipon",
    "Today -今日は令和何年で何の日？-": "today-app",
    "Cook-it -冷蔵庫の中を撮るだけでAIレシピ提案-": "cook-it",
    "言の葉箱 〜大切な手紙を簡単に記録〜": "kotonohabako",
    "RelayChat (リレーチャット) ~オフライン会話~": "relaychat",
    "ゼリーセイムパズル": "jelly-same-puzzle",
    "フチドリ！ ~背景透過と縁取り~": "fuchidori",
    "mono ~お迎えした喜びを分かち合うアプリ~": "mono",
    "旬のお魚カレンダー": "shun-fish-calendar",
    "Music Snapshot 〜あなたの音楽を一枚に〜": "music-snapshot",
    "バースデームーン": "birthday-moon",
    "π ~ Pi　円周率を楽しむアプリ": "pi-app",
    "旅行思い出マップ - 旅の記憶を、地図に描く": "travel-memory-map",
    "フォトガード": "photoguard",
    "ClockWidget ~個性豊かな時計ウィジェットアプリ~": "clockwidget",
    "Simple Touch The Numbers": "simple-touch-numbers",
    "ikaQR ~QRコードを爆速で読み込もう~": "ikaqr",
    "らくタグ": "rakutag",
    "TicketMania": "ticketmania",
    "AlwaysOnTimer　- いつでもタイマー": "alwaysontimer",
    "ながらカウンター ~別のアプリを使っていてもカウントできる~": "nagara-counter",
    "PictIn": "pictin",
    "PIPMP": "pipmp",
    "流れるメモ帳": "nagareru-memo",
    "WidgetZenn": "widgetzenn",
    "WidgetQiita": "widgetqiita",
    "SkyCode": "skycode",
    "BookBank(読書銀行) あなたの知識を記帳しよう": "bookbank",
}

# ============================================================
# ユーティリティ
# ============================================================

def escape_html(text):
    if not text:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def bi(ja, en):
    """日本語と英語を並べる（docs/i18n.md）。同じ文字列なら1つだけ出す。"""
    if ja == en:
        return ja
    return f'<span class="i18n-ja">{ja}</span><span class="i18n-en">{en}</span>'

MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

def format_date_en(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return f"{MONTHS_EN[dt.month - 1]} {dt.day}, {dt.year}"
    except:
        return ""

def rating_count_en(count):
    return "1 rating" if count == 1 else f"{count:,} ratings"

def price_en(price):
    return "Free" if price == "無料" else price

def format_date_jp(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except:
        return ""

GENRE_MAP = {
    "Lifestyle": "ライフスタイル",
    "Health & Fitness": "ヘルスケア/フィットネス",
    "Entertainment": "エンターテインメント",
    "Reference": "辞書/辞典/その他",
    "Photo & Video": "写真/ビデオ",
    "Graphics & Design": "グラフィック/デザイン",
    "Utilities": "ユーティリティ",
    "Medical": "メディカル",
    "Productivity": "仕事効率化",
    "Food & Drink": "フード/ドリンク",
    "Social Networking": "ソーシャルネットワーキング",
    "Games": "ゲーム",
    "Music": "ミュージック",
    "Education": "教育",
    "Travel": "旅行",
    "News": "ニュース",
    "Book": "ブック",
}


# ============================================================
# App Store説明文 → HTML変換
# ============================================================

EN_LINK_LABEL = re.compile(
    r'^[-•・*]?\s*(terms|privacy|support|contact|eula|commercial|specified commercial|legal|disclaimer)[^.!?]{0,50}$',
    re.IGNORECASE)

def clean_english_description(desc):
    """英語の説明文から、リンク・サポート・規約の行を除く（日本語側の除去と同じ目的）。"""
    lines = desc.replace('**', '').split('\n')
    url_line = [bool(re.search(r'https?://', l)) for l in lines]
    kept = []
    for i, line in enumerate(lines):
        s = line.strip()
        if url_line[i]:
            continue
        if s and EN_LINK_LABEL.match(s):
            continue
        kept.append(line)
    return '\n'.join(kept)

def drop_trailing_headings(html_lines):
    """リンク行を除いたあとに中身が残らなかった見出し（「■ Legal」など）を末尾から外す。"""
    while html_lines and html_lines[-1].strip().startswith('<h2>'):
        html_lines.pop()
    return html_lines

def description_to_html(desc, lang):
    """App Storeの説明文をそのままHTMLに変換する。
    構造を忠実に保持し、創作は一切しない。

    変換ルール:
    - 【...】 → <h2>
    - ■ ... / ▼ ... / □ ... / ◆ ... / ▸ ... → <h3>
    - - xxx / ・xxx → <li>（連続する場合は<ul>でまとめる）
    - 空行区切りの通常テキスト → <p>
    - --- 区切り線 → 無視
    - URLやリンクセクション → 除去
    """
    if not desc:
        if lang == 'en':
            return '        <p>See the App Store for details about this app.</p>'
        return '        <p>アプリの詳細はApp Storeをご覧ください。</p>'

    if lang == 'en':
        desc = clean_english_description(desc)

    # リンク・URL・サポート情報セクションを除去
    desc = re.sub(r'\n*【リンク】.*$', '', desc, flags=re.DOTALL)
    desc = re.sub(r'\n*▼\s*リンク.*$', '', desc, flags=re.DOTALL)
    desc = re.sub(r'\n*-+\n*▼\s*リンク.*$', '', desc, flags=re.DOTALL)
    desc = re.sub(r'\n*サポート・お問い合わせ:\s*\nhttps://.*$', '', desc, flags=re.DOTALL)
    desc = re.sub(r'\n*サポート:\s*\nhttps://.*$', '', desc, flags=re.DOTALL)
    desc = re.sub(r'\n*\[サポート\].*$', '', desc, flags=re.DOTALL)
    desc = re.sub(r'\n*◆\s*お問い合わせ.*$', '', desc, flags=re.DOTALL)
    # 末尾のURLリンクを除去
    desc = re.sub(r'\n利用規約[：:]?\s*https?://[^\n]*', '', desc)
    desc = re.sub(r'\nプライバシーポリシー[：:]?\s*https?://[^\n]*', '', desc)
    desc = re.sub(r'\n特定商取引法[：:]?\s*https?://[^\n]*', '', desc)
    desc = re.sub(r'\nサポート[：:]?\s*https?://[^\n]*', '', desc)
    desc = re.sub(r'\nhttps?://tsuzukit\.com/[^\n]*', '', desc)
    desc = re.sub(r'\nhttps?://tsuzuki817\.com/[^\n]*', '', desc)
    desc = desc.strip()

    lines = desc.split('\n')
    html_lines = []
    in_list = False
    is_first_paragraph = True

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 空行
        if not line:
            if in_list:
                html_lines.append('        </ul>')
                in_list = False
            i += 1
            continue

        # 装飾区切り線（---）は無視
        if re.match(r'^-{3,}$', line):
            i += 1
            continue

        # 【...】 → h2
        m = re.match(r'^【(.+?)】$', line)
        if m:
            if in_list:
                html_lines.append('        </ul>')
                in_list = False
            html_lines.append(f'        <h2>{escape_html(m.group(1))}</h2>')
            i += 1
            continue

        # ■ / ▼ / □ / ◆ / ▸ → h2（【】と同レベル）
        m = re.match(r'^[■▼□◆▸]\s*(.+)', line)
        if m:
            if in_list:
                html_lines.append('        </ul>')
                in_list = False
            html_lines.append(f'        <h2>{escape_html(m.group(1))}</h2>')
            i += 1
            continue

        # 箇条書き: - xxx / ・xxx / ● xxx（英語は • も）
        bullet = r'^[-・▪●•]\s*(.+)' if lang == 'en' else r'^[-・▪●]\s*(.+)'
        m = re.match(bullet, line)
        if m:
            if not in_list:
                html_lines.append('        <ul>')
                in_list = True
            html_lines.append(f'            <li>{escape_html(m.group(1))}</li>')
            i += 1
            continue

        # URLのみの行はスキップ
        if re.match(r'^https?://', line):
            i += 1
            continue

        # 通常テキスト → p（最初の段落はlead）
        if in_list:
            html_lines.append('        </ul>')
            in_list = False

        if is_first_paragraph:
            html_lines.append(f'        <p class="lead">{escape_html(line)}</p>')
            is_first_paragraph = False
        else:
            html_lines.append(f'        <p>{escape_html(line)}</p>')

        i += 1

    # リストが閉じていない場合
    if in_list:
        html_lines.append('        </ul>')

    if lang == 'en':
        html_lines = drop_trailing_headings(html_lines)

    return '\n'.join(html_lines)


# ============================================================
# ページ生成
# ============================================================


def screenshot_img(url, i, name, en_name, en_screenshots):
    """スクショ1枚分の <img>。英語のスクショがあれば data-en-src で差し替え、無い枠は英語表示で隠す。"""
    if not en_screenshots:
        en_attr = ''
    elif i < len(en_screenshots):
        en_attr = f' data-en-src="{en_screenshots[i]}"'
    else:
        en_attr = ' class="i18n-ja"'
    return (f'            <img src="{url}"{en_attr} alt="{escape_html(name)} スクリーンショット {i+1}" '
            f'data-en-alt="{escape_html(en_name)} screenshot {i+1}" loading="lazy">')

def generate_page(app, slug):
    name = app['name']
    icon_url = app.get('icon_url', '')
    app_store_url = app.get('app_store_url', '')
    screenshots = app.get('screenshots', [])
    genre_jp = GENRE_MAP.get(app.get('primary_genre', ''), app.get('primary_genre', ''))
    price = app.get('formatted_price', '無料')
    rating = app.get('rating', 0)
    rating_count = app.get('rating_count', 0)
    release_date = app.get('release_date', '')
    version = app.get('version', '')
    release_jp = format_date_jp(release_date)
    description = app.get('description', '')

    # 英語（App Store US の公式情報。無いアプリは英訳。どちらも無ければ日本語名と「App Storeを見て」）
    en = APPS_EN.get(str(app.get('id')))
    if en is None:
        print(f"WARN: no English data for {name} (id {app.get('id')}); run scripts/fetch_apps_en.py")
    en_name = en['name'] if en and en.get('name') else name
    en_description = en['description'] if en else ''
    genre_en = app.get('primary_genre', '')
    genre_html = bi(escape_html(genre_jp), escape_html(genre_en))
    price_html = bi(escape_html(price), escape_html(price_en(price)))
    release_html = bi(release_jp, format_date_en(release_date))
    name_html = bi(escape_html(name), escape_html(en_name))

    en_clean = re.sub(r'\s+', ' ', clean_english_description(en_description)).strip()
    meta_desc_en = escape_html(en_clean[:160])

    # meta description用: 説明文の冒頭から
    desc_clean = re.sub(r'\n+', ' ', description).strip()
    desc_clean = re.sub(r'\s+', ' ', desc_clean)
    meta_desc = escape_html(desc_clean[:160])

    # Rating HTML
    rating_html = ""
    if rating and rating > 0:
        stars_count = int(round(rating))
        rating_html = f'''
                    <div class="app-hero-rating">
                        <span class="stars">{"★" * stars_count}{"☆" * (5 - stars_count)}</span>
                        <span>{round(rating, 1)}</span>
                        <span class="count">({bi(f"{rating_count:,}件", rating_count_en(rating_count))})</span>
                    </div>'''

    # 英語表示では US ストアの英語スクショに差し替える。英語の枚数が足りない枠は英語表示で隠す
    en_screenshots = (en or {}).get('screenshots', [])

    # Screenshots HTML
    ss_html = ""
    if screenshots:
        ss_items = "\n".join([
            screenshot_img(url, i, name, en_name, en_screenshots)
            for i, url in enumerate(screenshots[:6])
        ])
        ss_html = f'''
    <!-- Screenshots -->
    <section class="app-screenshots-section">
        <div class="app-screenshots-track">
{ss_items}
        </div>
    </section>'''

    # 記事本文（App Storeの説明文をそのままHTML化）
    article_body = description_to_html(description, 'ja')
    article_body_en = description_to_html(en_description, 'en')

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="/assets/js/lang.js"></script>
    <title>{escape_html(name)} - アプリ紹介 | Ryo Tsuzukihashi</title>
    <meta name="title-en" content="{escape_html(en_name)} - App Spotlight | Ryo Tsuzukihashi">
    <meta name="description" content="{meta_desc}">
    <meta name="description-en" content="{meta_desc_en}">

    <!-- OGP -->
    <meta property="og:title" content="{escape_html(name)} - アプリ紹介">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:image" content="{icon_url}">
    <meta property="og:url" content="https://tsuzukit.com/blog/posts/app-{slug}.html">
    <meta property="og:type" content="article">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">

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
    <link rel="stylesheet" href="/assets/css/app-intro.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-container">
            <a href="/" class="nav-logo">TsuzuKit</a>
            <div class="nav-menu" id="navMenu">
                <a href="/portfolio/" class="nav-link">Portfolio</a>
                <a href="/about/" class="nav-link">About</a>
                <a href="/blog/" class="nav-link active">Blog</a>
                <a href="/contact/" class="nav-link">Contact</a>
            </div>
            <div class="nav-toggle" id="navToggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="app-hero-section">
        <div class="app-hero-inner">
            <img src="{icon_url}" alt="{escape_html(name)}" data-en-alt="{escape_html(en_name)}" class="app-hero-icon">
            <div class="app-hero-text">
                <h1 class="app-hero-title">{name_html}</h1>
                <div class="app-hero-meta">
                    <span class="app-hero-badge">{genre_html}</span>
                    <span class="app-hero-badge">{price_html}</span>{rating_html}
                </div>
                <div class="app-hero-download">
                    <a href="{app_store_url}" target="_blank" rel="noopener noreferrer">
                        <img src="/assets/images/download-on-the-appstore.svg" alt="App Storeからダウンロード" data-en-alt="Download on the App Store">
                    </a>
                </div>
            </div>
        </div>
    </section>
{ss_html}

    <!-- Article -->
    <article class="app-article">
        <div class="app-description i18n-ja">
{article_body}
        </div>
        <div class="app-description i18n-en">
{article_body_en}
        </div>

        <!-- App Info -->
        <div class="app-info-section">
            <h2>{bi("アプリ情報", "App Info")}</h2>
            <div class="app-info-grid">
                <div class="app-info-item">
                    <div class="app-info-label">{bi("カテゴリ", "Category")}</div>
                    <div class="app-info-value">{genre_html}</div>
                </div>
                <div class="app-info-item">
                    <div class="app-info-label">{bi("価格", "Price")}</div>
                    <div class="app-info-value">{price_html}</div>
                </div>
                <div class="app-info-item">
                    <div class="app-info-label">{bi("バージョン", "Version")}</div>
                    <div class="app-info-value">{escape_html(version)}</div>
                </div>
                <div class="app-info-item">
                    <div class="app-info-label">{bi("リリース日", "Release Date")}</div>
                    <div class="app-info-value">{release_html}</div>
                </div>
            </div>
        </div>

        <!-- CTA -->
        <div class="app-cta-section">
            <h2>{bi("ダウンロードはこちら", "Get the App")}</h2>
            <p>{bi("気になった方はぜひお試しください", "If it caught your eye, give it a try.")}</p>
            <a href="{app_store_url}" target="_blank" rel="noopener noreferrer" class="app-cta-btn">
                {bi("App Storeで見る", "View on the App Store")}
            </a>
        </div>
    </article>

    <!-- Footer -->
    <div class="app-post-footer">
        <img class="tk-char tk-char--post" src="/assets/images/character-hang.png" alt="" width="381" height="208">
        <a href="/blog/">{bi("← ブログ一覧に戻る", "← Back to Blog")}</a>
    </div>

    <footer style="background: var(--color-primary); color: var(--color-background); padding: 3rem 0; text-align: center;">
        <div class="container">
            <p style="color: var(--color-background); opacity: 0.8; margin-bottom: 1rem;">
                &copy; 2025 Ryo Tsuzukihashi. All rights reserved.
            </p>
            <div style="margin-top: 1rem;">
                <a href="/legal/privacy-policy.html" style="color: var(--color-background); opacity: 0.6; margin: 0 1rem; text-decoration: none;">{bi("プライバシーポリシー", "Privacy Policy")}</a>
                <a href="/legal/terms-of-service.html" style="color: var(--color-background); opacity: 0.6; margin: 0 1rem; text-decoration: none;">{bi("利用規約", "Terms of Service")}</a>
            </div>
        </div>
    </footer>

    <script>
        const navToggle = document.getElementById('navToggle');
        const navMenu = document.getElementById('navMenu');
        if (navToggle) {{
            navToggle.addEventListener('click', function() {{
                navToggle.classList.toggle('active');
                navMenu.classList.toggle('active');
            }});
        }}
    </script>
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, f'blog/posts/app-{slug}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


# ============================================================
# メイン実行
# ============================================================
generated = 0
missing = []

for app in APPS:
    name = app['name']
    if name in SLUG_MAP:
        slug = SLUG_MAP[name]
        filepath = generate_page(app, slug)
        generated += 1
        ss_count = len(app.get('screenshots', []))
        print(f"OK: {name} (SS:{ss_count}) -> {os.path.basename(filepath)}")
    else:
        missing.append(name)
        print(f"MISSING SLUG: {name}")

print(f"\nGenerated: {generated}/{len(APPS)}")
if missing:
    print(f"Missing: {len(missing)} apps")
    for m in missing:
        print(f"  - {m}")
