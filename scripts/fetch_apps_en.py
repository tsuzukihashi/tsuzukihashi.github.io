#!/usr/bin/env python3
"""
アプリ紹介ページ（blog/posts/app-*.html）の英語版に使う、App Store の英語の公式情報を取ってくる。

iTunes Lookup API の US ストア（country=us&lang=en_us）から、アプリごとに
英語名・英語の説明文・英語のカテゴリ・英語のスクリーンショットを取り、assets/data/apps_en.json に保存する。
generate_app_blogs.py はこのファイルだけを読み、ネットワークには出ない。

- 取れたもの: "source": "app_store_us"
- US ストアに無い、または英語の説明文が無い（日本語が返る）もの:
  手で英訳して "source": "translated" を付ける。このスクリプトは既存の translated を上書きしない
  （取り直したときに英語の公式説明が出てくれば、そちらに置き換わる）

使い方: python3 scripts/fetch_apps_en.py
"""

import json
import os
import re
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_PATH = os.path.join(BASE_DIR, 'assets/data/apps.json')
OUT_PATH = os.path.join(BASE_DIR, 'assets/data/apps_en.json')

JA_CHARS = re.compile(r'[぀-ヿ一-鿿]')


def looks_japanese(text):
    """かな・漢字が全体の1割を超えていれば、英語の説明文ではないとみなす。"""
    if not text:
        return True
    return len(JA_CHARS.findall(text)) > len(text) * 0.1


def hi_res(url):
    """lookup が返す低解像度（320x480bb.jpg 等）を、サイトで使っている 626x0w.webp に置き換える。"""
    return re.sub(r'/\d+x\d+bb\.\w+$', '/626x0w.webp', url)


def lookup(ids):
    url = ('https://itunes.apple.com/lookup?id=' + ','.join(str(i) for i in ids)
           + '&country=us&lang=en_us')
    req = urllib.request.Request(url, headers={'User-Agent': 'tsuzukit.com fetch_apps_en'})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res).get('results', [])


def main():
    with open(APPS_PATH, encoding='utf-8') as f:
        apps = json.load(f)['apps']

    existing = {}
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH, encoding='utf-8') as f:
            existing = json.load(f).get('apps', {})

    ids = [a['id'] for a in apps]
    results = {}
    for start in range(0, len(ids), 50):
        for r in lookup(ids[start:start + 50]):
            results[str(r['trackId'])] = r

    out = {}
    need_translation = []
    for app in apps:
        key = str(app['id'])
        r = results.get(key)
        if r and not looks_japanese(r.get('description', '')):
            out[key] = {
                'name': r.get('trackName', ''),
                'description': r.get('description', ''),
                'genre': r.get('primaryGenreName', ''),
                'screenshots': [hi_res(u) for u in r.get('screenshotUrls', [])],
                'source': 'app_store_us',
            }
            continue
        prev = existing.get(key)
        if prev and prev.get('source') == 'translated':
            out[key] = prev
            continue
        need_translation.append((key, app['name'], 'not in US store' if not r else 'Japanese only'))
        if prev:
            out[key] = prev

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump({'apps': out}, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'Saved {len(out)} apps -> {os.path.relpath(OUT_PATH, BASE_DIR)}')
    if need_translation:
        print(f'\nNo English App Store description ({len(need_translation)}); add a "translated" entry by hand:')
        for key, name, why in need_translation:
            print(f'  {key}  {name}  ({why})')


if __name__ == '__main__':
    main()
