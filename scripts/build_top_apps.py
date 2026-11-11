"""トップページの「アプリを探す」と信頼の数字を、アプリのデータから作り直す。

    python3 scripts/build_top_apps.py

読むもの
- assets/data/apps.json      … 名前・アイコン・評価・スクショ・ストアのURL（ポートフォリオ更新で作る）
- assets/data/apps_en.json   … 英語の名前・ジャンル・英語のスクショ
- assets/data/app_urls.json  … ASC のサポートURLとLP（scripts/fetch_app_urls.rb）
- assets/data/lp_shots.json  … LP の最初の画面を撮った画像（scripts/capture_lp_shots.mjs）

index.html の次の印のあいだを書きかえる
- <!-- TOP-TRUST:START --> … <!-- TOP-TRUST:END -->   公開中の本数と評価
- <!-- TOP-APPS:START --> … <!-- TOP-APPS:END -->     アイコンの一覧とシート用のデータ
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
FIRST_SHOWN = 12  # 検索していないときに見せる本数（ダウンロードの多い順）


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


apps = sorted(apps, key=lambda x: -(x.get('download_count') or 0))
data = []
for x in apps:
    sid = str(x['id'])
    en = apps_en.get(sid, {})
    u = urls.get(sid, {})
    shot = shots.get(sid)
    ss_en = en.get('screenshots') or []
    if isinstance(ss_en, str):
        ss_en = []
    data.append({
        'id': sid,
        'n': x['name'],
        'ne': en.get('name') or x['name'],
        'i': icon(x['icon_url'], 256),
        'r': round(x['rating'] or 0, 1),
        'rc': x['rating_count'],
        'g': (x.get('genres') or [''])[0],
        'ge': en.get('genre') or x.get('primary_genre') or '',
        's': x['app_store_url'],
        'p': clean_url(x.get('google_play_url')),
        'su': {'ja': clean_url((u.get('support_url') or {}).get('ja')),
               'en': clean_url((u.get('support_url') or {}).get('en'))},
        'lp': shot and {'url': shot['url'], 'img': shot['shots']},
        'ss': x.get('screenshots', [])[:3],
        'sse': ss_en[:3],
    })

rc = sum(x['rating_count'] for x in apps)
avg = sum((x['rating'] or 0) * x['rating_count'] for x in apps) / rc
e = html.escape

trust = f'''
                    <div class="trust-item">
                        <span class="trust-number"><span class="i18n-ja">{len(apps)}本</span><span class="i18n-en">{len(apps)}</span></span>
                        <span class="trust-label"><span class="i18n-ja">公開中のアプリ</span><span class="i18n-en">live apps</span></span>
                    </div>
                    <div class="trust-item">
                        <span class="trust-number">★{avg:.1f}</span>
                        <span class="trust-label"><span class="i18n-ja">{rc:,}件の評価</span><span class="i18n-en">{rc:,} ratings</span></span>
                    </div>
                    '''

items = []
for n, d in enumerate(data):
    extra = ' is-extra' if n >= FIRST_SHOWN else ''
    ja, en_ = short_name(d['n']), short_name(d['ne'])
    label = f'<span class="i18n-ja">{e(ja)}</span><span class="i18n-en">{e(en_)}</span>' if ja != en_ else e(ja)
    items.append(
        f'''                    <li class="app-tile{extra}"><button type="button" class="app-tile-btn" data-app="{d['id']}">'''
        f'''<img src="{e(d['i'])}" alt="" width="64" height="64" loading="lazy">'''
        f'''<span class="app-tile-name">{label}</span></button></li>''')

blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
apps_block = '\n' + '\n'.join(items) + '\n                '

src = INDEX.read_text()


def put(src, name, body):
    pat = re.compile(rf'(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)', re.S)
    if not pat.search(src):
        raise SystemExit(f'index.html に {name} の印が無い')
    return pat.sub(lambda m: m.group(1) + body + m.group(3), src)


src = put(src, 'TOP-TRUST', trust)
src = put(src, 'TOP-APPS', apps_block)
src = put(src, 'TOP-APPS-DATA', f'<script type="application/json" id="appsData">{blob}</script>')
INDEX.write_text(src)
print(f'apps={len(data)} lp={sum(1 for d in data if d["lp"])} support={sum(1 for d in data if d["su"]["ja"])} rating={avg:.2f} ({rc})')
