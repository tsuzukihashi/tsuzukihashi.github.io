"""トップページ（ガチャ）の、アプリのデータから作る部分を作り直す。

    python3 scripts/build_top_apps.py

読むもの
- assets/data/apps.json      … 名前・アイコン・評価・ダウンロード数・スクショ・ストアのURL（ポートフォリオ更新で作る）
- assets/data/apps_en.json   … 英語の名前・ジャンル・英語のスクショ
- assets/data/app_urls.json  … ASC のサポートURLとLP（scripts/fetch_app_urls.rb）
- assets/data/lp_shots.json  … LP の最初の画面を撮った画像（scripts/capture_lp_shots.mjs）
- blog/index.html            … 「おまけの冊子」に出す新しい読みもの（上から順に）

index.html の次の印のあいだを書きかえる
- TOP-TRUST  … 公開中の本数と評価
- TOP-GLOBE  … 機械の玉の中のカプセル
- TOP-ODDS   … 排出のめやす（レア度ごとの本数）
- TOP-APPS   … ラインナップ（レア度ごとの段。押すとシートが出る）
- TOP-FRESH  … 新しく入ったカプセル
- TOP-BOOKS  … おまけの冊子
- TOP-APPS-DATA … シートと回す処理が読むデータ

レア度はダウンロード数（SSR 10万以上・SR 1万以上・R 1000以上・N それ以外）。docs/gacha-design.md
"""
import html
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
BLOG = ROOT / 'blog' / 'index.html'
GLOBE_N = 22      # 機械の玉に入れる数
TIER_SHOWN = 8    # スマホで、検索していないときに段ごとに見せる数
FRESH_N = 6
e = html.escape


def load(name, default):
    p = ROOT / 'assets/data' / name
    return json.loads(p.read_text()) if p.exists() else default


apps = load('apps.json', {})['apps']
apps_en = load('apps_en.json', {}).get('apps', {})
urls = load('app_urls.json', {})
shots = load('lp_shots.json', {})


def icon(url, size):
    return re.sub(r'/\d+x\d+bb\.(jpg|png|webp)$', f'/{size}x{size}bb.jpg', url)


def short_name(name):
    # ストアの名前は「アプリ名 - 説明」「アプリ名：説明」の形が多い。一覧では頭だけ出す
    s = re.split(r'\s*[~～〜：:｜|]|\s+[-–—]\s*|　', name, maxsplit=1)[0]
    s = re.split(r'-(?=[^\x00-\x7f])', s, maxsplit=1)[0]  # RelayChat-オフライン… の形
    return s.strip() or name


def clean_url(u):
    u = (u or '').strip()
    return u or None


def rarity(dl):
    if dl >= 100000:
        return 'SSR'
    if dl >= 10000:
        return 'SR'
    if dl >= 1000:
        return 'R'
    return 'N'


def dl_text(dl):
    """16.9万 / 169K のような、ざっくりした数。"""
    if dl >= 10000:
        ja = f'{dl / 10000:.1f}'.rstrip('0').rstrip('.') + '万'
    else:
        ja = f'{dl:,}'
    en = f'{dl / 1000:.1f}'.rstrip('0').rstrip('.') + 'K' if dl >= 1000 else f'{dl:,}'
    return ja, en


def bi(ja, en):
    return f'<span class="i18n-ja">{ja}</span><span class="i18n-en">{en}</span>' if ja != en else ja


apps = sorted(apps, key=lambda x: (-(x.get('download_count') or 0), x['release_date']))
data = []
for k, x in enumerate(apps):
    sid = str(x['id'])
    en = apps_en.get(sid, {})
    u = urls.get(sid, {})
    shot = shots.get(sid)
    ss_en = en.get('screenshots') or []
    if isinstance(ss_en, str):
        ss_en = []
    dl = x.get('download_count') or 0
    data.append({
        'id': sid,
        'n': x['name'],
        'ne': en.get('name') or x['name'],
        'sn': short_name(x['name']),
        'sne': short_name(en.get('name') or x['name']),
        'i': icon(x['icon_url'], 256),
        'r': round(x['rating'] or 0, 1),
        'rc': x['rating_count'],
        'd': dl,
        'k': rarity(dl),
        'c': k % 6 + 1,
        'g': (x.get('genres') or [''])[0],
        'ge': en.get('genre') or x.get('primary_genre') or '',
        'rd': x['release_date'][:10],
        's': x['app_store_url'],
        'p': clean_url(x.get('google_play_url')),
        'su': {'ja': clean_url((u.get('support_url') or {}).get('ja')),
               'en': clean_url((u.get('support_url') or {}).get('en'))},
        'lp': shot and {'url': shot['url'], 'img': shot['shots']},
        'ss': x.get('screenshots', [])[:3],
        'sse': ss_en[:3],
    })


def rot(d):
    return int(d['id']) % 50 - 25


def cap(d, size_cls=''):
    return (f'<span class="g-cap g-cap--{d["c"]}{size_cls}" style="--rot:{rot(d)}deg">'
            f'<img src="{e(d["i"])}" alt="" width="64" height="64" loading="lazy"></span>')


def label(d):
    return bi(e(d['sn']), e(d['sne']))


def line(d):
    """「出た！」の札の説明。ジャンル・評価・ダウンロード数（どれも apps.json の値）。"""
    ja, en = dl_text(d['d'])
    parts_ja, parts_en = [d['g']] if d['g'] else [], [d['ge']] if d['ge'] else []
    if d['rc'] > 0:
        parts_ja.append(f'★{d["r"]:.1f}（{d["rc"]:,}件）')
        parts_en.append(f'★{d["r"]:.1f} ({d["rc"]:,} ratings)')
    if d['d'] > 0:
        parts_ja.append(f'{ja}ダウンロード')
        parts_en.append(f'{en} downloads')
    return '・'.join(parts_ja), ' · '.join(parts_en)


# ---------------------------------------------------------------- 信頼の数字
rc = sum(x['rating_count'] for x in apps)
avg = sum((x['rating'] or 0) * x['rating_count'] for x in apps) / rc
trust = f'''
                        <li><b>{len(apps)}<small>{bi('本', '')}</small></b><span>{bi('公開中のアプリ', 'live apps')}</span></li>
                        <li><b>★{avg:.1f}</b><span>{bi(f'{rc:,}件の評価', f'{rc:,} ratings')}</span></li>
                        '''

# ---------------------------------------------------------------- 出た！
# ---------------------------------------------------------------- 機械の玉
def pile(n, d):
    """半径 50 の円の中に、直径 d のカプセルを下から積む（0〜100 の座標）。"""
    pts, row, y = [], 0, 100 - d / 2 - 1.5
    while len(pts) < n and y > 20:
        half = math.sqrt(max(0, 50 ** 2 - (y - 50) ** 2)) - d / 2 - 1
        x = 50 - half + ((d / 2) if row % 2 else 0)
        while x <= 50 + half + 0.01 and len(pts) < n:
            pts.append((x, y))
            x += d * 0.98
        y -= d * 0.84
        row += 1
    return pts


globe = ''.join(
    f'<span class="g-cap g-cap--{d["c"]}" style="left:{x:.1f}%;top:{y:.1f}%;width:19%;--rot:{rot(d)}deg">'
    f'<img src="{e(d["i"])}" alt="" width="64" height="64" loading="lazy"></span>'
    for (x, y), d in zip(pile(GLOBE_N, 19), data))

# ---------------------------------------------------------------- 段
TIERS = [
    ('SSR', '10万DL以上', '100K+ downloads'),
    ('SR', '1万DL以上', '10K+ downloads'),
    ('R', '1000DL以上', '1K+ downloads'),
    ('N', 'これから育つ', 'Still growing'),
]
by_tier = {t: [d for d in data if d['k'] == t] for t, _, _ in TIERS}
odds = ''.join(
    f'<li><span class="g-rare g-rare--{t}">{t}</span>{bi(ja, en)}<b>{bi(f"{len(by_tier[t])}種", str(len(by_tier[t])))}</b></li>'
    for t, ja, en in TIERS)

tiers = ''
for t, ja, en in TIERS:
    lst = by_tier[t]
    if not lst:
        continue
    tiles = ''.join(
        f'<li class="app-tile{" is-extra" if n >= TIER_SHOWN else ""}"><button type="button" class="g-mini app-tile-btn" data-app="{d["id"]}">'
        f'{cap(d)}<span>{label(d)}</span></button></li>'
        for n, d in enumerate(lst))
    tiers += f'''
                    <div class="t-tier" data-tier="{t}">
                        <div class="t-tier-lb"><b class="g-rare--{t}">{t}</b><small>{bi(f'{ja}<br> {len(lst)}種', f'{en}<br> · {len(lst)}')}</small></div>
                        <ul class="t-tier-caps">{tiles}</ul>
                    </div>'''
tiers += '\n                    '

# ---------------------------------------------------------------- 新しく入った
fresh = ''.join(
    f'''
                    <li><button type="button" class="t-fresh-card g-panel" data-app="{d["id"]}"><span class="t-new">NEW</span>'''
    f'''<img src="{e(d["i"])}" alt="" width="72" height="72" loading="lazy"><span class="t-fresh-name">{label(d)}</span>'''
    f'''<time datetime="{d["rd"]}">{d["rd"].replace("-", ".")}</time></button></li>'''
    for d in sorted(data, key=lambda d: d['rd'], reverse=True)[:FRESH_N]) + '\n                '


# ---------------------------------------------------------------- おまけの冊子
def books_from_blog():
    src = BLOG.read_text()
    cards = re.findall(r'<article class="post-card"[^>]*>(.*?)</article>', src, re.S)
    out = []
    for c in cards:
        href = re.search(r'<a href="(/blog/posts/[^"]+)"', c)
        img = re.search(r'<img src="([^"]+)"', c)
        date = re.search(r'class="post-date">([^<]+)<', c)
        cat = re.search(r'class="post-category">(.*?)</span>\s*</div>', c, re.S)
        title = re.search(r'class="post-card-title">\s*<a [^>]*>(.*?)</a>', c, re.S)
        if not (href and img and title):
            continue
        out.append(dict(href=href.group(1), img=img.group(1), date=(date.group(1).strip() if date else ''),
                        cat=(cat.group(1).strip() if cat else ''), title=title.group(1).strip()))
    return out


posts = books_from_blog()
income = [p for p in posts if '/income-report-' in p['href']][:1]
others = sorted([p for p in posts if '/income-report-' not in p['href']], key=lambda p: p['date'], reverse=True)[:3]
books = ''.join(
    f'''
                    <a class="g-book g-panel" href="{p["href"]}"><img src="{e(p["img"])}" alt="" width="1200" height="800" loading="lazy">'''
    f'''<div><small>{p["cat"]}</small><h3>{p["title"]}</h3><time>{e(p["date"])}</time></div></a>'''
    for p in income + others) + '\n                '

blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

src = INDEX.read_text()


def put(src, name, body):
    pat = re.compile(rf'(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)', re.S)
    if not pat.search(src):
        raise SystemExit(f'index.html に {name} の印が無い')
    return pat.sub(lambda m: m.group(1) + body + m.group(3), src)


src = put(src, 'TOP-TRUST', trust)
src = put(src, 'TOP-GLOBE', globe)
src = put(src, 'TOP-ODDS', odds)
src = put(src, 'TOP-APPS', tiers)
src = put(src, 'TOP-FRESH', fresh)
src = put(src, 'TOP-BOOKS', books)
src = put(src, 'TOP-APPS-DATA', f'<script type="application/json" id="appsData">{blob}</script>')
INDEX.write_text(src)
print(f'apps={len(data)} ' + ' '.join(f'{t}={len(by_tier[t])}' for t, _, _ in TIERS)
      + f' lp={sum(1 for d in data if d["lp"])} support={sum(1 for d in data if d["su"]["ja"])} rating={avg:.2f} ({rc}) books={len(income + others)}')
