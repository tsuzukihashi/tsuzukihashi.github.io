#!/usr/bin/env python3
"""
43アプリのブログ紹介ページを生成する。
App Storeの説明文(description)をそのまま忠実にHTMLに変換する。
嘘や創作は一切含めない。
"""

import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'assets/data/apps.json')) as f:
    data = json.load(f)

APPS = data['apps']

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

def description_to_html(desc):
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
        return '        <p>アプリの詳細はApp Storeをご覧ください。</p>'

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

        # 箇条書き: - xxx / ・xxx / ● xxx
        m = re.match(r'^[-・▪●]\s*(.+)', line)
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

    return '\n'.join(html_lines)


# ============================================================
# ページ生成
# ============================================================

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
                        <span class="count">({rating_count:,}件)</span>
                    </div>'''

    # Screenshots HTML
    ss_html = ""
    if screenshots:
        ss_items = "\n".join([
            f'            <img src="{url}" alt="{escape_html(name)} スクリーンショット {i+1}" loading="lazy">'
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
    article_body = description_to_html(description)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(name)} - アプリ紹介 | Ryo Tsuzukihashi</title>
    <meta name="description" content="{meta_desc}">

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
            <img src="{icon_url}" alt="{escape_html(name)}" class="app-hero-icon">
            <div class="app-hero-text">
                <h1 class="app-hero-title">{escape_html(name)}</h1>
                <div class="app-hero-meta">
                    <span class="app-hero-badge">{escape_html(genre_jp)}</span>
                    <span class="app-hero-badge">{escape_html(price)}</span>{rating_html}
                </div>
                <div class="app-hero-download">
                    <a href="{app_store_url}" target="_blank" rel="noopener noreferrer">
                        <img src="/assets/images/download-on-the-appstore.svg" alt="App Storeからダウンロード">
                    </a>
                </div>
            </div>
        </div>
    </section>
{ss_html}

    <!-- Article -->
    <article class="app-article">
{article_body}

        <!-- App Info -->
        <div class="app-info-section">
            <h2>アプリ情報</h2>
            <div class="app-info-grid">
                <div class="app-info-item">
                    <div class="app-info-label">カテゴリ</div>
                    <div class="app-info-value">{escape_html(genre_jp)}</div>
                </div>
                <div class="app-info-item">
                    <div class="app-info-label">価格</div>
                    <div class="app-info-value">{escape_html(price)}</div>
                </div>
                <div class="app-info-item">
                    <div class="app-info-label">バージョン</div>
                    <div class="app-info-value">{escape_html(version)}</div>
                </div>
                <div class="app-info-item">
                    <div class="app-info-label">リリース日</div>
                    <div class="app-info-value">{release_jp}</div>
                </div>
            </div>
        </div>

        <!-- CTA -->
        <div class="app-cta-section">
            <h2>ダウンロードはこちら</h2>
            <p>気になった方はぜひお試しください</p>
            <a href="{app_store_url}" target="_blank" rel="noopener noreferrer" class="app-cta-btn">
                App Storeで見る
            </a>
        </div>
    </article>

    <!-- Footer -->
    <div class="app-post-footer">
        <a href="/blog/">← ブログ一覧に戻る</a>
    </div>

    <footer style="background: var(--color-primary); color: var(--color-background); padding: 3rem 0; text-align: center;">
        <div class="container">
            <p style="color: var(--color-background); opacity: 0.8; margin-bottom: 1rem;">
                &copy; 2025 Ryo Tsuzukihashi. All rights reserved.
            </p>
            <div style="margin-top: 1rem;">
                <a href="/legal/privacy-policy.html" style="color: var(--color-background); opacity: 0.6; margin: 0 1rem; text-decoration: none;">プライバシーポリシー</a>
                <a href="/legal/terms-of-service.html" style="color: var(--color-background); opacity: 0.6; margin: 0 1rem; text-decoration: none;">利用規約</a>
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
