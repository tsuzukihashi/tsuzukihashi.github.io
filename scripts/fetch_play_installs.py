#!/usr/bin/env python3
"""Google Play の累計インストールを取り、assets/data/app-ranking.json の android の欄を作り直す。

Play Console のインストール レポート（GCS の stats/installs/*_overview.csv）を全部読み、
Daily User Installs を全期間で足したものを累計インストール、いちばん新しい日の
Active Device Installs を稼働台数にする。

このマシンでは gcloud storage / gsutil が動かない（Python 3.9 で落ちる）ので、
トークンだけ gcloud から借りて GCS の JSON API を直接読む。
トークンが取れないときは、ユーザーに `! gcloud auth login` を打ってもらう。

使い方: python3 scripts/fetch_play_installs.py
"""
import collections
import csv
import html
import io
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANK = os.path.join(REPO, "assets", "data", "app-ranking.json")
APPS = os.path.join(REPO, "assets", "data", "apps.json")
BUCKET = "pubsite_prod_4900858120458572039"
API = f"https://storage.googleapis.com/storage/v1/b/{BUCKET}/o"


def head(name):
    return re.split(r"[\s\-:：~〜（(|｜]", name.strip())[0]


def get(url, token, timeout=60):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    return urllib.request.urlopen(req, timeout=timeout).read()


def list_overviews(token):
    names, page = [], None
    while True:
        q = {"prefix": "stats/installs/", "fields": "items(name),nextPageToken", "maxResults": "1000"}
        if page:
            q["pageToken"] = page
        d = json.loads(get(API + "?" + urllib.parse.urlencode(q), token))
        names += [i["name"] for i in d.get("items", []) if i["name"].endswith("_overview.csv")]
        page = d.get("nextPageToken")
        if not page:
            return names


def decode(raw):
    for enc in ("utf-16", "utf-8-sig", "utf-8"):
        try:
            t = raw.decode(enc)
        except Exception:
            continue
        if "Date" in t:
            return t
    raise ValueError("CSV が読めない")


def play_page(pkg):
    """Play だけのアプリの名前とアイコンを Play のページから取る。"""
    url = f"https://play.google.com/store/apps/details?id={pkg}&hl=ja"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "ja"})
    t = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    title = re.search(r'<meta property="og:title" content="([^"]+)"', t)
    image = re.search(r'<meta property="og:image" content="([^"]+)"', t)
    name = html.unescape(title.group(1)).replace(" - Google Play のアプリ", "").strip() if title else pkg
    icon = html.unescape(image.group(1)) if image else ""
    if icon:
        icon = re.sub(r"=[^=/]*$", "", icon) + "=s256"
    return name, icon


def main():
    try:
        token = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True,
                               check=True, timeout=60).stdout.strip()
    except Exception as e:
        sys.exit(f"gcloud のトークンが取れない（{e}）。ユーザーに `! gcloud auth login` を打ってもらう")

    total, active, last = collections.Counter(), {}, {}
    for name in sorted(list_overviews(token)):
        pkg = name.split("installs_")[1].rsplit("_", 2)[0]
        rows = csv.DictReader(io.StringIO(decode(get(API + "/" + urllib.parse.quote(name, safe="") + "?alt=media", token))))
        for r in rows:
            total[pkg] += int(r.get("Daily User Installs") or 0)
            d = r["Date"]
            if pkg not in last or d >= last[pkg]:
                last[pkg] = d
                active[pkg] = int(r.get("Active Device Installs") or 0)

    rank = json.load(open(RANK, encoding="utf-8"))
    apps = json.load(open(APPS, encoding="utf-8"))["apps"]
    old = {a["package"]: a for a in rank["android"]["apps"]}
    by_pkg = {}
    for a in apps:
        m = re.search(r"id=([\w.]+)", a.get("google_play_url") or "")
        if m:
            by_pkg[m.group(1)] = a
        if a.get("bundle_id"):
            by_pkg.setdefault(a["bundle_id"], a)
    by_head = {head(a["name"]): a for a in apps}

    out = []
    for pkg, n in total.items():
        if pkg in old:
            r = dict(old[pkg])
        else:
            a = by_pkg.get(pkg)
            if a:
                r = {"name": a["name"], "package": pkg, "icon_url": a["icon_url"], "app_id": str(a["id"])}
            else:
                name, icon = play_page(pkg)
                a = by_head.get(head(name))
                r = {"name": a["name"] if a else name, "package": pkg, "icon_url": a["icon_url"] if a else icon}
                if a:
                    r["app_id"] = str(a["id"])
                else:
                    print(f"  ⚠️  {pkg}（{name}）は iOS 版が見つからない。docs/build_ranking.py の NAMES_EN に英語名を足す")
            print(f"  + 新しく Play の欄に入る: {r['name']} ({pkg})")
        r.update({"installs": n, "active_devices": active[pkg], "display": f"{n:,}",
                  "play_url": f"https://play.google.com/store/apps/details?id={pkg}"})
        out.append(r)
    out.sort(key=lambda r: -r["installs"])
    for i, r in enumerate(out, 1):
        r["rank"] = i

    until = max(last.values())
    a = rank["android"]
    a["apps"] = out
    a["app_count"] = len(out)
    a["total_installs"] = sum(r["installs"] for r in out)
    a["total_active"] = sum(r["active_devices"] for r in out)
    a["source"] = ("Play Console のインストール レポート（installs_*_overview.csv の Daily User Installs を"
                   f"全期間合算。{until} まで）")
    rank["grand_total"] = rank["total_units"] + a["total_installs"]
    with open(RANK, "w", encoding="utf-8") as f:
        json.dump(rank, f, ensure_ascii=False, indent=2)

    for r in out:
        print(f"  {r['rank']:>2}. {r['name'][:28]:<28} {r['installs']:>8,}")
    print(f"Google Play: {len(out)}本 / 累計 {a['total_installs']:,}（{until} まで）/ 合計 {rank['grand_total']:,}")


if __name__ == "__main__":
    main()
