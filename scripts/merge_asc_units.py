#!/usr/bin/env python3
"""App Store Connect のトレンド（ユニット数）の表を、assets/data/app-ranking.json の apps に入れる。

表は Playwright で ASC の画面から書き出したもの（手順は .claude/skills/update-portfolio-info/SKILL.md の 4章）。
- 全期間の表: 必須。ASC は上から100行で切るので、100行に入らなかったアプリが出る
- 過去30日間の表: 任意。全期間の表に無いアプリのうち、30日以内に出したアプリはこちらの数を使う

使い方:
  python3 scripts/merge_asc_units.py <全期間の表.json> --until 2026-11-19 [--recent <過去30日間の表.json>]

--until は ASC の画面に出ている「〜まで」の日（全期間の終わり＝昨日）。
"""
import argparse
import datetime
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANK = os.path.join(REPO, "assets", "data", "app-ranking.json")
APPS = os.path.join(REPO, "assets", "data", "apps.json")
DEV = " Ryo Tsudukihashi"


def load_rows(path):
    """browser_evaluate の filename で書き出すと、JSON の文字列がもう1回 JSON で包まれていることがある。"""
    d = json.loads(open(path, encoding="utf-8").read().strip())
    if isinstance(d, str):
        d = json.loads(d)
    head = next(r for r in d if "Apple ID" in r)
    i_name, i_type, i_id, i_units = (head.index(k) for k in ("名前", "タイプ", "Apple ID", "ユニット数"))
    out = {}
    for r in d:
        if r is head or len(r) <= i_units:
            continue
        if not r[i_name].endswith(DEV) or r[i_type] != "App":
            continue  # 預かりアプリ（他の開発者名義）と課金商品は入れない
        out[r[i_id]] = (r[i_name][: -len(DEV)].strip(), units(r[i_units]), r[i_units])
    return out, sum(1 for r in d if r is not head and len(r) > i_units)


def units(s):
    s = s.replace(",", "").strip()
    if s.endswith("K"):
        return round(float(s[:-1]) * 1000)
    if s.endswith("M"):
        return round(float(s[:-1]) * 1000000)
    return int(s or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alltime")
    ap.add_argument("--until", required=True)
    ap.add_argument("--recent")
    args = ap.parse_args()
    until = datetime.date.fromisoformat(args.until)

    table, n_rows = load_rows(args.alltime)
    recent = load_rows(args.recent)[0] if args.recent else {}
    capped = n_rows >= 100
    print(f"全期間の表: {n_rows}行（Ryo Tsudukihashi の App {len(table)}本）{'← 100行で切れている' if capped else ''}")

    rank = json.load(open(RANK, encoding="utf-8"))
    old = {a["app_id"]: a for a in rank["apps"]}
    apps = {str(a["id"]): a for a in json.load(open(APPS, encoding="utf-8"))["apps"]}

    got = {i: (u, disp) for i, (_, u, disp) in table.items()}
    for i, a in apps.items():
        if i in got:
            continue
        released = datetime.date.fromisoformat(a["release_date"][:10])
        if i in recent and (until - released).days <= 31:
            got[i] = recent[i][1:]
            print(f"  過去30日の表から: {a['name'][:24]} {recent[i][1]}")
        elif i in recent:
            print(f"  ⚠️  {a['name'][:24]} は全期間の表から切れていて、30日の表にだけある（{recent[i][1]}）。"
                  "全期間の数は分からないので前回の値を使う")
            got[i] = (old[i]["units"], old[i]["display"]) if i in old else recent[i][1:]
        else:
            got[i] = (old[i]["units"], old[i]["display"]) if i in old and capped else (0, "0")
    # 配信を終えたアプリで、今回の表から切れたもの（全期間の数は減らないので前回のまま）
    for i, o in old.items():
        if i not in got:
            got[i] = (o["units"], o["display"])
            print(f"  表に無いので前回のまま: {o['name'][:24]} {o['units']}")

    out = []
    for i, (u, disp) in got.items():
        a = apps.get(i)
        if a:
            e = {"name": a["name"], "app_id": i, "units": u, "display": disp, "icon_url": a["icon_url"],
                 "app_store_url": a["app_store_url"], "genre": a.get("primary_genre"),
                 "rating": a.get("rating"), "rating_count": a.get("rating_count")}
        elif i in old:
            e = dict(old[i], units=u, display=disp)
        else:
            e = {"name": table[i][0], "app_id": i, "units": u, "display": disp, "icon_url": "",
                 "app_store_url": "", "genre": "", "rating": 0, "rating_count": 0}
            print(f"  ⚠️  配信終了のアプリが新しく入った: {e['name']}（{i}）。名前を日本語に直し、"
                  "docs/build_ranking.py の NAMES_EN に英語名を足す")
        out.append(e)
    out.sort(key=lambda e: (-e["units"], e["name"]))
    for k, e in enumerate(out, 1):
        e["rank"] = k

    rank["apps"] = out
    rank["app_count"] = len(out)
    rank["total_units"] = sum(e["units"] for e in out)
    rank["grand_total"] = rank["total_units"] + rank["android"]["total_installs"]
    rank["generated_at"] = datetime.date.today().isoformat()
    rank["source"] = f"App Store Connect トレンド・ユニット数（全期間：配信開始日から{args.until}まで）"
    with open(RANK, "w", encoding="utf-8") as f:
        json.dump(rank, f, ensure_ascii=False, indent=2)
    for e in out[:10]:
        print(f"  {e['rank']:>2}. {e['name'][:28]:<28} {e['units']:>8,}")
    print(f"App Store: {len(out)}本 / {rank['total_units']:,}（{args.until} まで）/ 合計 {rank['grand_total']:,}")


if __name__ == "__main__":
    main()
