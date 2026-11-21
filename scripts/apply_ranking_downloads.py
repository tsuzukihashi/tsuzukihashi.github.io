#!/usr/bin/env python3
"""ランキング（assets/data/app-ranking.json）の数字を、apps.json の download_count に入れる。

ガチャのレア度（トップ・/portfolio/）と並び順は download_count で決まる。
ランキングを更新したら、このスクリプトで apps.json をそろえ、build_top_apps.py でトップを作り直す。
docs/build_ranking.py の最後で呼ばれる。

数え方: App Store の全期間のユニット数 + Google Play の累計インストール（同じアプリなら足す）。
Play の行は google_play_url のパッケージ名 → bundle_id → 名前の頭 の順で iOS のアプリに結びつける。
"""
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(REPO, "assets", "data", "apps.json")
RANK = os.path.join(REPO, "assets", "data", "app-ranking.json")


def head(name):
    """名前の頭（区切りの記号の手前）。もくもく - 読書銀行… → もくもく"""
    return re.split(r"[\s\-:：~〜（(|｜]", name.strip())[0]


def main():
    apps = json.load(open(APPS, encoding="utf-8"))
    rank = json.load(open(RANK, encoding="utf-8"))

    ios = {int(r["app_id"]): r["units"] for r in rank["apps"] if r.get("app_id")}

    by_pkg = {}
    for a in apps["apps"]:
        m = re.search(r"id=([\w.]+)", a.get("google_play_url") or "")
        if m:
            by_pkg[m.group(1)] = a
        if a.get("bundle_id"):
            by_pkg.setdefault(a["bundle_id"], a)
    by_head = {head(a["name"]): a for a in apps["apps"]}

    play = {}
    for p in rank["android"]["apps"]:
        a = by_pkg.get(p["package"]) or by_head.get(head(p["name"]))
        if a:
            play[a["id"]] = p["installs"]
            print(f"  Play {p['package']} ({p['installs']:,}) → {a['name'][:24]}")
        else:
            print(f"  Play {p['package']} ({p['installs']:,}) → iOS 版なし（Play だけのアプリ）")

    missing = []
    changed = 0
    for a in apps["apps"]:
        if a["id"] not in ios:
            missing.append(a["name"])
            continue
        n = ios[a["id"]] + play.get(a["id"], 0)
        if a.get("download_count") != n:
            a["download_count"] = n
            changed += 1
    if missing:
        print("⚠️  ランキングに無いアプリ（download_count はそのまま）:", ", ".join(missing))

    with open(APPS, "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)
    print(f"apps.json の download_count を {changed} 本更新")


if __name__ == "__main__":
    main()
