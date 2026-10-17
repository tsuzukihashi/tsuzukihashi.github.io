#!/usr/bin/env python3
"""英語版の記事でドル表記に使う、月末の為替レート（1ドルあたりの円）を fx_usd.json に保存する。

レートは build_master.py と同じ ECB の月末レート（frankfurter.dev）。
generate_articles.py はこのファイルだけを読み、ネットワークには出ない。
新しい月の記事を作るときは、MONTHS に足す前にこのスクリプトを実行する。

使い方: python3 fetch_fx_usd.py 2026-09 [2026-10 ...]
"""
import calendar
import json
import os
import sys
import urllib.request

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fx_usd.json")


def fetch(ym):
    y, m = map(int, ym.split("-"))
    day = f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]}"
    req = urllib.request.Request(f"https://api.frankfurter.dev/v1/{day}?base=USD&symbols=JPY",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        r = json.load(res)
    return {"date": r["date"], "jpy_per_usd": r["rates"]["JPY"]}


def main():
    data = {}
    if os.path.exists(PATH):
        with open(PATH) as f:
            data = json.load(f)
    for ym in sys.argv[1:]:
        data[ym] = fetch(ym)
        print(ym, data[ym])
    with open(PATH, "w") as f:
        json.dump(dict(sorted(data.items())), f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
