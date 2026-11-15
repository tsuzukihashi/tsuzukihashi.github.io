#!/usr/bin/env python3
"""
検索される問いに答える記事（docs/guides/*.json）から、blog/posts/<slug>.html を作る。

1本 = JSON 1枚。見た目・ナビ・フッター・構造化データはここで揃えるので、
記事を増やすときは JSON を書いて、このスクリプトを流すだけにする。

  python3 scripts/build_guides.py          # 全部作る
  python3 scripts/build_guides.py --check  # 検査だけ（書き出さない）

書き方は docs/guides/README.md。
"""

import glob
import html
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(BASE_DIR, 'docs', 'guides')
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
ILLUSTRATIONS = os.path.join(BASE_DIR, 'docs', 'blog-illustrations.json')
SITEMAP = os.path.join(BASE_DIR, 'sitemap.xml')
SITE = 'https://tsuzukit.com'

# 検索結果の説明文は、日本語だと120字あたりで切られる
DESCRIPTION_MAX = {'ja': 120, 'en': 240}
# 先に答えを渡す箱。長いと答えではなく本文になる
TLDR_MAX = {'ja': 200, 'en': 450}
# サイトの文章ルール（CLAUDE.md の編集プロンプト・skill tsuzuki-voice）で出さないもの
FORBIDDEN_JA = ['…', '結論から言うと', '本記事では', '以下で解説します', '参考になれば幸いです']

LANGS = ('ja', 'en')


def esc(text):
    return html.escape(text, quote=True)


def bi(ja, en):
    return f'<span class="i18n-ja">{esc(ja)}</span><span class="i18n-en">{esc(en)}</span>'


# ============================================================
# 検査
# ============================================================

def check_bilingual(value, where, errors):
    if not isinstance(value, dict) or any(not isinstance(value.get(l), str) or not value.get(l).strip() for l in LANGS):
        errors.append(f'{where}: 日本語と英語の両方が要る')
        return
    for word in FORBIDDEN_JA:
        if word in value['ja']:
            errors.append(f'{where}: 「{word}」は使わない')


def walk_bilingual(node, where, errors):
    """{ja, en} の形をしたものを全部たどって検査する。"""
    if isinstance(node, dict):
        if set(node.keys()) == {'ja', 'en'}:
            check_bilingual(node, where, errors)
            return
        for key, value in node.items():
            walk_bilingual(value, f'{where}.{key}', errors)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk_bilingual(value, f'{where}[{i}]', errors)


def validate(guide, path, illustrations):
    errors = []
    name = os.path.basename(path)
    required = ['slug', 'date_published', 'date_updated', 'search_phrase', 'evidence', 'title', 'description',
                'category', 'reading_minutes', 'author', 'tldr', 'disclosure', 'own_app', 'apps', 'sections',
                'faq', 'closing', 'notes']
    for key in required:
        if key not in guide:
            errors.append(f'{name}: {key} が無い')
    if errors:
        return errors

    slug = guide['slug']
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug):
        errors.append(f'{name}: slug は半角小文字・数字・ハイフンだけ')
    if os.path.splitext(name)[0] != slug:
        errors.append(f'{name}: ファイル名と slug を揃える')
    for key in ('date_published', 'date_updated'):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', guide[key]):
            errors.append(f'{name}: {key} は YYYY-MM-DD')
    if guide['date_updated'] < guide['date_published']:
        errors.append(f'{name}: date_updated が date_published より前')

    walk_bilingual(guide, name, errors)

    for lang in LANGS:
        if len(guide['description'][lang]) > DESCRIPTION_MAX[lang]:
            errors.append(f'{name}: description.{lang} が{len(guide["description"][lang])}字（{DESCRIPTION_MAX[lang]}字まで）')
        if len(guide['tldr'][lang]) > TLDR_MAX[lang]:
            errors.append(f'{name}: tldr.{lang} が{len(guide["tldr"][lang])}字（{TLDR_MAX[lang]}字まで）')

    app_ids = [a['id'] for a in guide['apps']]
    if guide['own_app'] not in app_ids:
        errors.append(f'{name}: own_app が apps に無い')
    for app in guide['apps']:
        for key in ('id', 'name', 'short', 'developer', 'icon', 'store_url', 'android_url', 'rating_count'):
            if key not in app:
                errors.append(f'{name}: apps[{app.get("id")}] に {key} が無い（無いなら null と書く）')

    # 比べたアプリは、全部カードで1回ずつ紹介する（表にだけ出て説明が無いアプリを作らない）
    carded = []
    for s_i, section in enumerate(guide['sections']):
        for b_i, block in enumerate(section['blocks']):
            where = f'{name}: sections[{s_i}].blocks[{b_i}]'
            kind = block.get('type')
            if kind == 'app':
                if block.get('id') not in app_ids:
                    errors.append(f'{where}: apps に無い id {block.get("id")}')
                carded.append(block.get('id'))
            elif kind == 'table':
                width = len(block['head'])
                for r_i, row in enumerate(block['rows']):
                    if len(row) != width:
                        errors.append(f'{where}: rows[{r_i}] の列の数が見出しと違う')
            elif kind not in ('p', 'list'):
                errors.append(f'{where}: 知らない type {kind}')
    for app_id in app_ids:
        if carded.count(app_id) != 1:
            errors.append(f'{name}: アプリ {app_id} のカードが{carded.count(app_id)}枚（1枚にする）')

    image = os.path.join(BASE_DIR, 'assets', 'images', 'posts', f'{slug}.webp')
    if not os.path.exists(image):
        errors.append(f'{name}: イラスト assets/images/posts/{slug}.webp が無い（skill blog-illustration）')
    alt = illustrations.get('alt', {}).get(slug)
    if not alt or len(alt) != 2 or not all(alt):
        errors.append(f'{name}: docs/blog-illustrations.json の alt に {slug} の日英が無い')
    return errors


# ============================================================
# 描画
# ============================================================

def render_app_card(app, own, lang):
    badge = ''
    if own:
        badge = f'<span class="guide-app-own">{"僕が作ったアプリ" if lang == "ja" else "I made this"}</span>'
    count = f'{app["rating_count"]:,}'
    plural = '' if app['rating_count'] == 1 else 's'
    ratings = f'App Storeの評価 {count}件' if lang == 'ja' else f'{count} App Store rating{plural}'
    android = ''
    if app['android_url']:
        label = 'Google Play版' if lang == 'ja' else 'Android version on Google Play'
        android = f'<a class="guide-app-android" href="{esc(app["android_url"])}" target="_blank" rel="noopener noreferrer">{label}</a>'
    href = esc(app['store_url'])
    if lang == 'ja':
        store = f'<a href="{href}" target="_blank" rel="noopener noreferrer"><img class="guide-app-badge" src="/assets/images/download-on-the-appstore.svg" alt="App Storeからダウンロード" width="110" height="40"></a>'
    else:
        # サイトにあるバッジは日本語入りの1枚だけ。英語表示で日本語の画像を出さないため、英語は文字のボタンにする
        store = f'<a class="guide-app-store-text" href="{href}" target="_blank" rel="noopener noreferrer">View on the App Store</a>'
    return f'''
            <div class="guide-app{' guide-app--own' if own else ''}">
                <img class="guide-app-icon" src="{esc(app['icon'])}" width="96" height="96" alt="" loading="lazy">
                <div class="guide-app-body">
                    {badge}
                    <h3 class="guide-app-name">{esc(app['name'][lang])}</h3>
                    <p class="guide-app-meta">{esc(app['developer'])} · {ratings}</p>
                    <div class="guide-app-links">
                        {store}
                        {android}
                    </div>
                </div>
            </div>'''


def render_block(block, apps, own_id, lang):
    kind = block['type']
    if kind == 'p':
        return f'            <p>{esc(block["text"][lang])}</p>'
    if kind == 'list':
        items = ''.join(f'<li>{esc(item[lang])}</li>' for item in block['items'])
        return f'            <ul class="guide-list">{items}</ul>'
    if kind == 'table':
        head = ''.join(f'<th scope="col">{esc(cell[lang])}</th>' for cell in block['head'])
        rows = ''
        for row in block['rows']:
            first = f'<th scope="row">{esc(row[0][lang])}</th>'
            rest = ''.join(f'<td>{esc(cell[lang])}</td>' for cell in row[1:])
            rows += f'<tr>{first}{rest}</tr>'
        return f'''            <div class="guide-table-wrap"><table class="guide-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'''
    if kind == 'app':
        app = next(a for a in apps if a['id'] == block['id'])
        return render_app_card(app, app['id'] == own_id, lang)
    raise ValueError(kind)


def fmt_date(iso, lang):
    y, m, d = iso.split('-')
    return f'{y}.{m}.{d}' if lang == 'ja' else f'{y}-{m}-{d}'


def render_body(guide, lang):
    g = guide
    author = g['author']
    labels = {
        'ja': {'tldr': '先に答え', 'by': '書いた人', 'pub': '公開', 'upd': '更新', 'faq': 'よくある質問', 'back': 'ブログ一覧へ'},
        'en': {'tldr': 'Short answer', 'by': 'Written by', 'pub': 'Published', 'upd': 'Updated', 'faq': 'FAQ', 'back': 'Back to the blog'},
    }[lang]
    handle = f'（@{esc(author["handle"])}）' if lang == 'ja' else f' (@{esc(author["handle"])})'
    parts = [f'''        <div class="post-content guide i18n-{lang}">
            <aside class="guide-tldr">
                <p class="guide-tldr-label">{labels['tldr']}</p>
                <p>{esc(g['tldr'][lang])}</p>
            </aside>
            <div class="guide-byline">
                <img class="guide-byline-face" src="/assets/images/user_profile.webp" alt="" width="512" height="512">
                <div>
                    <p class="guide-byline-name">{labels['by']} <a href="{esc(author['url'])}">{esc(author['name'][lang])}</a>{handle}</p>
                    <p class="guide-byline-bio">{esc(author['bio'][lang])}</p>
                    <p class="guide-byline-date">{labels['pub']} <time datetime="{g['date_published']}">{fmt_date(g['date_published'], lang)}</time> · {labels['upd']} <time datetime="{g['date_updated']}">{fmt_date(g['date_updated'], lang)}</time></p>
                </div>
            </div>
            <p class="guide-disclosure">{esc(g['disclosure'][lang])}</p>''']
    for section in g['sections']:
        parts.append(f'            <h2>{esc(section["heading"][lang])}</h2>')
        for block in section['blocks']:
            parts.append(render_block(block, g['apps'], g['own_app'], lang))
    parts.append(f'            <h2>{labels["faq"]}</h2>')
    parts.append('            <dl class="guide-faq">')
    for item in g['faq']:
        parts.append(f'                <dt>{esc(item["q"][lang])}</dt><dd>{esc(item["a"][lang])}</dd>')
    parts.append('            </dl>')
    parts.append(f'            <p>{esc(g["closing"][lang])}</p>')
    parts.append(f'            <div class="guide-notes">{esc(g["notes"][lang])}</div>')
    parts.append('        </div>')
    return '\n'.join(parts)


def json_ld(guide, illustration_url):
    g = guide
    url = f'{SITE}/blog/posts/{g["slug"]}.html'
    author = g['author']
    person = {'@type': 'Person', 'name': author['name']['ja'], 'alternateName': [author['name']['en'], author['handle']],
              'url': author['url'], 'sameAs': author['same_as']}
    own = next(a for a in g['apps'] if a['id'] == g['own_app'])
    graph = [
        {
            '@type': 'Article',
            'headline': g['title']['ja'],
            'description': g['description']['ja'],
            'image': illustration_url,
            'datePublished': g['date_published'],
            'dateModified': g['date_updated'],
            'inLanguage': 'ja',
            'author': person,
            'publisher': person,
            'mainEntityOfPage': url,
            'about': [{'@type': 'SoftwareApplication', 'name': a['name']['ja'], 'url': a['store_url'],
                       'operatingSystem': 'iOS'} for a in g['apps']],
        },
        {
            '@type': 'SoftwareApplication',
            'name': own['name']['ja'],
            'operatingSystem': 'iOS',
            'applicationCategory': 'HealthApplication',
            'url': own['store_url'],
            'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'JPY'},
            'author': person,
        },
        {
            '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': f['q']['ja'],
                            'acceptedAnswer': {'@type': 'Answer', 'text': f['a']['ja']}} for f in g['faq']],
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': f'{SITE}/blog/'},
                {'@type': 'ListItem', 'position': 3, 'name': g['title']['ja'], 'item': url},
            ],
        },
    ]
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)
    # </script> を本文に含めないように
    return data.replace('</', '<\\/')


def render_page(guide, alt):
    g = guide
    slug = g['slug']
    url = f'{SITE}/blog/posts/{slug}.html'
    image_path = f'/assets/images/posts/{slug}.webp'
    image_url = f'{SITE}{image_path}'
    title_ja = f'{g["title"]["ja"]} - Blog | Ryo Tsuzukihashi'
    title_en = f'{g["title"]["en"]} - Blog | Ryo Tsuzukihashi'
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="/assets/js/lang.js"></script>
    <!-- このページは scripts/build_guides.py が docs/guides/{slug}.json から作る。直すのは JSON のほう -->
    <title>{esc(title_ja)}</title>
    <meta name="description" content="{esc(g['description']['ja'])}">
    <meta name="title-en" content="{esc(title_en)}">
    <meta name="description-en" content="{esc(g['description']['en'])}">
    <link rel="canonical" href="{url}">

    <!-- OGP -->
    <meta property="og:title" content="{esc(g['title']['ja'])}">
    <meta property="og:description" content="{esc(g['description']['ja'])}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{image_url}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{image_url}">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png">
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

    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8240751277462688"
        crossorigin="anonymous"></script>

    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/blog.css">
    <link rel="stylesheet" href="/assets/css/guide.css">

    <script type="application/ld+json">
{json_ld(g, image_url)}
    </script>
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-container">
            <a href="/" class="nav-logo">TsuzuKit</a>
            <div class="nav-menu">
                <a href="/" class="nav-link">Home</a>
                <a href="/portfolio/" class="nav-link">Portfolio</a>
                <a href="/blog/" class="nav-link active">Blog</a>
                <a href="/about/" class="nav-link">About</a>
                <a href="/contact/" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Blog Post -->
    <article class="blog-post">
        <header class="post-header">
            <div class="post-meta">
                <span class="post-date">{fmt_date(g['date_published'], 'ja')}</span>
                <span class="post-category">{bi(g['category']['ja'], g['category']['en'])}</span>
                <span class="post-reading-time">{bi(f"{g['reading_minutes']}分で読める", f"{g['reading_minutes']} min read")}</span>
            </div>
            <h1 class="post-title">{bi(g['title']['ja'], g['title']['en'])}</h1>
        </header>
        <figure class="post-illustration guide-illustration"><img src="{image_path}" width="1200" height="800" alt="{esc(alt[0])}" data-en-alt="{esc(alt[1])}" fetchpriority="high"></figure>

{render_body(g, 'ja')}

{render_body(g, 'en')}

        <nav class="post-navigation">
            <img class="tk-char tk-char--post" src="/assets/images/character-hang.png" alt="" width="381" height="208">
            <a href="/blog/" class="nav-link-wrapper"><span>&larr; {bi('ブログ一覧へ', 'Back to the blog')}</span></a>
        </nav>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <img class="footer-peek" src="/assets/images/character-peek.png" alt="" width="320" height="364">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3 class="footer-logo">Ryo Tsuzukihashi</h3>
                    <p class="footer-description">{bi('誰も作らないものを、まじめに作る', 'I make things nobody else would, and I make them seriously')}</p>
                </div>
                <div class="footer-nav">
                    <a href="/legal/privacy-policy.html">{bi('プライバシーポリシー', 'Privacy Policy')}</a>
                    <a href="/legal/terms-of-service.html">{bi('利用規約', 'Terms of Service')}</a>
                    <a href="/legal/commercial-law.html">{bi('特定商取引法', 'Specified Commercial Transactions Act')}</a>
                    <a href="/legal/disclaimer.html">{bi('免責事項', 'Disclaimer')}</a>
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


def update_sitemap(slug, lastmod):
    """記事の <url> が無ければ足し、あれば lastmod だけ揃える。"""
    with open(SITEMAP, encoding='utf-8') as f:
        text = f.read()
    loc = f'{SITE}/blog/posts/{slug}.html'
    pattern = re.compile(rf'(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[^<]*(</lastmod>)')
    if pattern.search(text):
        new = pattern.sub(rf'\g<1>{lastmod}\g<2>', text)
    else:
        entry = (f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n'
                 f'    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n')
        new = text.replace('</urlset>', entry + '</urlset>')
    if new != text:
        with open(SITEMAP, 'w', encoding='utf-8') as f:
            f.write(new)


def main():
    check_only = '--check' in sys.argv
    with open(ILLUSTRATIONS, encoding='utf-8') as f:
        illustrations = json.load(f)
    paths = sorted(glob.glob(os.path.join(GUIDES_DIR, '*.json')))
    if not paths:
        print('docs/guides/ に JSON がありません')
        return 1

    guides, errors = [], []
    for path in paths:
        with open(path, encoding='utf-8') as f:
            guide = json.load(f)
        errors += validate(guide, path, illustrations)
        guides.append(guide)
    if errors:
        print('止めました。直してからもう一度流してください:')
        for e in errors:
            print(f'  - {e}')
        return 1
    if check_only:
        print(f'{len(guides)}本とも検査を通りました')
        return 0

    for guide in guides:
        slug = guide['slug']
        out = os.path.join(POSTS_DIR, f'{slug}.html')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(render_page(guide, illustrations['alt'][slug]))
        update_sitemap(slug, guide['date_updated'])
        print(f'書き出し: blog/posts/{slug}.html')
    return 0


if __name__ == '__main__':
    sys.exit(main())
