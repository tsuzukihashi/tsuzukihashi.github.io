"""ガチャの見た目の、全ページ共通のヘッダーとフッター。

ページを生成するスクリプトはここの header() / footer() / head_links() を使う。
手で書いたページの殻をまとめて入れ替えるときは:

    python3 scripts/gacha_shell.py blog/posts/*.html

- <nav class="nav" ...>…</nav> を新しいヘッダーに
- <footer class="footer">…</footer> を新しいフッターに
- <head> にガチャの字と gacha.css（と g-post.css）を足し、<body> に class="g" を付ける
すでに入れ替え済みのページは、ヘッダーとフッターだけ最新に揃える。
"""
import re
import sys
import pathlib

FONTS = ('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@500;700;800'
         '&family=RocknRoll+One&display=swap')

NAV = [
    ('/portfolio/', 'アプリ', 'Apps'),
    ('/blog/', '読みもの', 'Reading'),
    ('/about/', '私について', 'About'),
    ('/contact/', 'お問い合わせ', 'Contact'),
]

SNS = [
    ('https://x.com/tsuzuki817', 'X (Twitter)', 'x.png'),
    ('https://www.instagram.com/tsuzuki817/', 'Instagram', 'instagram.png'),
    ('https://www.tiktok.com/@tsuzuki817', 'TikTok', 'tiktok.png'),
    ('https://www.youtube.com/@tsuzuki817', 'YouTube', 'youtube.png'),
    ('https://github.com/tsuzukihashi', 'GitHub', 'github.png'),
]

LEGAL = [
    ('/legal/privacy-policy.html', 'プライバシーポリシー', 'Privacy Policy'),
    ('/legal/terms-of-service.html', '利用規約', 'Terms of Service'),
    ('/legal/commercial-law.html', '特定商取引法', 'Specified Commercial Transactions Act'),
    ('/legal/disclaimer.html', '免責事項', 'Disclaimer'),
]


def bi(ja, en):
    return f'<span class="i18n-ja">{ja}</span><span class="i18n-en">{en}</span>'


def header(active=None):
    """active には NAV の URL（'/blog/' など）を渡すと、そのボタンに印が付く。"""
    cur = ' aria-current="page"'
    links = ''.join(
        f'<a href="{u}" class="nav-link"{cur if u == active else ""}>{bi(ja, en)}</a>'
        for u, ja, en in NAV)
    return (
        '<header class="g-head" id="nav">\n'
        '            <div class="g-wrap">\n'
        '                <a href="/" class="g-logo"><img src="/assets/images/logo/tsuzukit-wordmark.svg" alt="TsuzuKit" width="116" height="36"></a>\n'
        f'                <nav class="nav-menu" id="navMenu" aria-label="メニュー">{links}</nav>\n'
        '                <button type="button" class="g-menu" id="navToggle" aria-controls="navMenu" aria-expanded="false">MENU</button>\n'
        '            </div>\n'
        '        </header>')


def footer():
    sns = ''.join(
        f'<a href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{name}"><img src="/assets/images/sns/{img}" alt="" width="22" height="22"></a>'
        for u, name, img in SNS)
    legal = ''.join(f'<a href="{u}">{bi(ja, en)}</a>' for u, ja, en in LEGAL)
    return (
        '<footer class="g-foot">\n'
        '            <img class="g-foot-peek" src="/assets/images/character-peek.png" alt="" width="320" height="364" loading="lazy">\n'
        '            <div class="g-wrap">\n'
        '                <div><a href="/" class="g-foot-logo"><img src="/assets/images/logo/tsuzukit-wordmark-white.svg" alt="TsuzuKit" width="110" height="34"></a>\n'
        f'                <p class="g-foot-tag">{bi("誰も作らないものを、まじめに作る。", "Making what nobody else will, seriously.") + "<br>Seriously Silly since 2016."}</p></div>\n'
        f'                <div class="g-foot-sns">{sns}</div>\n'
        f'                <div class="g-foot-links"><a href="/contact/">{bi("お問い合わせ", "Contact")}</a>{legal}</div>\n'
        '                <p class="g-foot-copy">© 2026 Ryo Tsuzukihashi / TsuzuKit</p>\n'
        '            </div>\n'
        '        </footer>')


def head_links(extra=()):
    """<head> に入れる字とCSSの行。extra には g-post.css などページ用のCSSのURLを渡す。"""
    css = ''.join(f'\n    <link rel="stylesheet" href="{u}">' for u in ('/assets/css/gacha.css', *extra))
    return (
        '<!-- ガチャの見た目（assets/css/gacha.css・docs/gacha-design.md） -->\n'
        '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'    <link rel="stylesheet" href="{FONTS}">'
        f'{css}\n'
        '    <script src="/assets/js/gacha.js" defer></script>\n'
        '    <!-- /ガチャの見た目 -->')


HEAD_RE = re.compile(r'<!-- ガチャの見た目.*?<!-- /ガチャの見た目 -->', re.S)
OLD_NAV_RE = re.compile(r'<nav class="nav"[^>]*>.*?</nav>', re.S)
NEW_NAV_RE = re.compile(r'<header class="g-head".*?</header>', re.S)
OLD_FOOT_RE = re.compile(r'<footer(?![^>]*g-foot)[^>]*>.*?</footer>', re.S)
NEW_FOOT_RE = re.compile(r'<footer class="g-foot">.*?</footer>', re.S)


def active_for(path):
    p = str(path)
    if '/blog/' in p or p.startswith('blog/'):
        return '/blog/'
    if 'portfolio' in p:
        return '/portfolio/'
    if 'about' in p:
        return '/about/'
    if 'contact' in p:
        return '/contact/'
    return None


def reskin(text, active, extra_css):
    """手で書いたページの殻を入れ替える。中身（本文）には触らない。"""
    head = head_links(extra_css)
    if HEAD_RE.search(text):
        text = HEAD_RE.sub(lambda m: head, text, count=1)
    else:
        text = text.replace('</head>', f'    {head}\n</head>', 1)
    if NEW_NAV_RE.search(text):
        text = NEW_NAV_RE.sub(lambda m: header(active), text, count=1)
    else:
        text, n = OLD_NAV_RE.subn(lambda m: header(active), text, count=1)
        if not n:
            raise SystemExit('ヘッダー（<nav class="nav">）が見つからない')
    if NEW_FOOT_RE.search(text):
        text = NEW_FOOT_RE.sub(lambda m: footer(), text, count=1)
    else:
        text, n = OLD_FOOT_RE.subn(lambda m: footer(), text, count=1)
        if not n:
            raise SystemExit('フッター（<footer>）が見つからない')
    m = re.search(r'<body([^>]*)>', text)
    attrs = m.group(1)
    if 'class="' in attrs:
        if not re.search(r'class="[^"]*\bg\b', attrs):
            attrs = attrs.replace('class="', 'class="g ', 1)
    else:
        attrs += ' class="g"'
    text = text[:m.start()] + f'<body{attrs}>' + text[m.end():]
    return text


if __name__ == '__main__':
    root = pathlib.Path(__file__).resolve().parents[1]
    for arg in sys.argv[1:]:
        p = pathlib.Path(arg)
        rel = p.resolve().relative_to(root)
        extra = ('/assets/css/g-post.css',) if str(rel).startswith('blog/posts/') else ()
        t = p.read_text(encoding='utf-8')
        new = reskin(t, active_for(rel), extra)
        if new != t:
            p.write_text(new, encoding='utf-8')
            print('reskin', rel)
