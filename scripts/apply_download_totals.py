#!/usr/bin/env python3
"""トップと「私について」に書いてある DL 数を、ランキングの数字にそろえる。

- 総ダウンロード（「81万+」「810K+」）… app-ranking.json の grand_total（App Store＋Google Play）
- トップの代表作（.t-work の「290,000+」）… apps.json の download_count（apply_ranking_downloads.py が入れる）
- 私についての一文（「流れるメモ帳が16万、全部合わせて81万ダウンロード」）

数は切り捨てて「+」を付ける（実測より大きく見せない）。
代表作の絵（assets/images/works/*.webp）には数字が焼き込まれているので、ここでは直せない。最後に一覧を出す。
docs/build_ranking.py の最後で呼ばれる。
"""
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANK = os.path.join(REPO, "assets", "data", "app-ranking.json")
APPS = os.path.join(REPO, "assets", "data", "apps.json")
INDEX = os.path.join(REPO, "index.html")
ABOUT = os.path.join(REPO, "about", "index.html")
MEMO = 1598380826  # 流れるメモ帳（私についての一文）


def man(n):
    return n // 10000  # 81万


def en_total(n):
    if n >= 1_000_000:
        return f"{n // 100_000 / 10:g}M"
    return f"{n // 10_000 * 10}K"


def work(n):
    step = 10_000 if n >= 100_000 else 1_000
    return f"{n // step * step:,}+"


def write(path, text, before, changes):
    if text != before:
        open(path, "w", encoding="utf-8").write(text)
        changes.append(os.path.relpath(path, REPO))


def main():
    grand = json.load(open(RANK, encoding="utf-8"))["grand_total"]
    dl = {a["id"]: a.get("download_count") or 0 for a in json.load(open(APPS, encoding="utf-8"))["apps"]}
    total = (f'<span class="i18n-ja">{man(grand)}万+</span>'
             f'<span class="i18n-en">{en_total(grand)}+</span>')
    pat_total = r'<span class="i18n-ja">\d+万\+</span><span class="i18n-en">[\d.]+[KM]\+</span>'
    changes, kv = [], []

    t = before = open(INDEX, encoding="utf-8").read()
    t, n = re.subn(pat_total, total, t)
    if n != 1:
        print(f"⚠️  index.html の総ダウンロードが {n} か所（1か所のはず）")

    def fix_work(m):
        aid = int(m.group(2))
        v = work(dl.get(aid, 0))
        kv.append((aid, v))
        return re.sub(r"(<ul><li><b>)[\d,]+\+(</b>)", lambda x: x.group(1) + v + x.group(2), m.group(0), count=1)

    t = re.sub(r'(<a [^>]*class="t-work g-panel" data-app="(\d+)".*?</a>)', fix_work, t, flags=re.S)
    write(INDEX, t, before, changes)

    t = before = open(ABOUT, encoding="utf-8").read()
    t, n = re.subn(pat_total, total, t)
    if n != 1:
        print(f"⚠️  about/index.html の総ダウンロードが {n} か所（1か所のはず）")
    memo = dl.get(MEMO, 0)
    t, n1 = re.subn(r"流れるメモ帳が\d+万、全部合わせて\d+万ダウンロード",
                    f"流れるメモ帳が{man(memo)}万、全部合わせて{man(grand)}万ダウンロード", t)
    t, n2 = re.subn(r"Floating Notepad has reached [\d,]+ downloads, and all my apps together have reached [\d,]+\.",
                    f"Floating Notepad has reached {man(memo) * 10000:,} downloads, and all my apps together "
                    f"have reached {man(grand) * 10000:,}.", t)
    if not (n1 and n2):
        print("⚠️  about/index.html の「流れるメモ帳が◯万、全部合わせて◯万」の一文が見つからない")
    write(ABOUT, t, before, changes)

    print(f"総ダウンロード: {man(grand)}万+ / {en_total(grand)}+（{grand:,}）")
    for aid, v in kv:
        print(f"  代表作 {aid}: {v}")
    print("書き換えたファイル:", ", ".join(changes) or "なし")
    print("代表作の絵（assets/images/works/*.webp）に焼き込んだ「◯万DL」が上の数と合っているか、目で見ること")


if __name__ == "__main__":
    main()
