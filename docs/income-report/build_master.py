#!/usr/bin/env python3
"""asc_detail.json からアプリ単位の月次集計を作り、AdMob/Playと統合する"""
import json
import os
import urllib.request
from collections import defaultdict
from datetime import date

SCRATCH = os.path.dirname(os.path.abspath(__file__))

STATIC_RATES_JPY = {
    "TWD": 5.0, "KZT": 0.30, "AED": 40.6, "SAR": 39.8, "EGP": 3.1,
    "RUB": 1.85, "CLP": 0.16, "QAR": 41.0, "COP": 0.037, "PEN": 41.0,
    "VND": 0.0057, "NGN": 0.095, "PKR": 0.53, "TZS": 0.057,
}

fx_cache = {}

def month_end(ym):
    y, m = map(int, ym.split("-"))
    if m == 12:
        return f"{y}-12-31"
    return str(date.fromordinal(date(y, m + 1, 1).toordinal() - 1))

def fx_rates(ym):
    if ym in fx_cache:
        return fx_cache[ym]
    url = f"https://api.frankfurter.dev/v1/{month_end(ym)}?base=JPY"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (revenue-report-script)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        fx_cache[ym] = json.load(r)["rates"]
    return fx_cache[ym]

def to_jpy(amount, currency, ym):
    if currency == "JPY":
        return amount
    rates = fx_rates(ym)
    if currency in rates:
        return amount / rates[currency]
    if currency in STATIC_RATES_JPY:
        return amount * STATIC_RATES_JPY[currency]
    print(f"  WARN: unknown currency {currency}")
    return 0

APP_TYPES = {"1", "1F", "1T", "3", "3F", "F1", "F1-B"}  # アプリ本体（新規DL）
UPDATE_TYPES = {"7", "7F", "7T", "F7"}  # アップデート

with open(os.path.join(SCRATCH, "asc_detail.json")) as f:
    detail = json.load(f)

master_as = {}
for ym, rows in detail.items():
    # アプリSKU→タイトルのマップ（アプリ本体行から構築）
    sku_to_title = {}
    for r in rows:
        if r["product_type"] in APP_TYPES or r["product_type"] in UPDATE_TYPES:
            sku_to_title[r["sku"]] = r["title"]

    apps = defaultdict(lambda: {"downloads": 0, "proceeds_jpy": 0.0, "iap_units": 0, "iap_names": defaultdict(float)})
    unattributed = defaultdict(float)

    for r in rows:
        proceeds = r["proceeds_per_unit"] * r["units"]
        jpy = to_jpy(proceeds, r["currency"], ym) if proceeds else 0
        if r["product_type"] in APP_TYPES:
            apps[r["title"]]["downloads"] += r["units"]
            apps[r["title"]]["proceeds_jpy"] += jpy  # 有料アプリの売上もここに乗る
        elif r["product_type"] in UPDATE_TYPES:
            pass
        else:
            # IAP/サブスク → 親アプリに帰属
            parent = r.get("parent_id") or ""
            app_title = sku_to_title.get(parent)
            if app_title:
                apps[app_title]["proceeds_jpy"] += jpy
                apps[app_title]["iap_units"] += r["units"]
                if jpy:
                    apps[app_title]["iap_names"][r["title"]] += jpy
            else:
                unattributed[r["title"]] += jpy
                apps["(不明: " + r["title"] + ")"]["proceeds_jpy"] += jpy
                apps["(不明: " + r["title"] + ")"]["iap_units"] += r["units"]

    result = []
    for title, a in apps.items():
        result.append({
            "title": title,
            "downloads": a["downloads"],
            "iap_units": a["iap_units"],
            "proceeds_jpy": round(a["proceeds_jpy"]),
            "top_products": sorted(
                [{"name": n, "jpy": round(v)} for n, v in a["iap_names"].items()],
                key=lambda x: -x["jpy"])[:5],
        })
    result.sort(key=lambda x: -x["proceeds_jpy"])
    total_jpy = round(sum(a["proceeds_jpy"] for a in apps.values()))
    total_dl = sum(a["downloads"] for a in apps.values())
    master_as[ym] = {"proceeds_jpy": total_jpy, "total_downloads": total_dl, "apps": result}
    if unattributed:
        print(f"{ym} 未帰属IAP: " + ", ".join(f"{k}=¥{round(v):,}" for k, v in unattributed.items() if v > 100))

with open(os.path.join(SCRATCH, "play_monthly.json")) as f:
    play = json.load(f)
with open(os.path.join(SCRATCH, "admob_monthly.json")) as f:
    admob = json.load(f)

admob_by_app = defaultdict(list)
for row in admob["by_month_app_top50_2025-11_to_2026-07"]:
    admob_by_app[row["month"]].append(row)

months = sorted(master_as.keys())
master = {}
for ym in months:
    a = admob["monthly_total"].get(ym, 0)
    s = master_as[ym]["proceeds_jpy"]
    p = play.get(ym, {}).get("totals", {}).get("net_jpy", 0)
    master[ym] = {
        "admob_jpy": a,
        "appstore_jpy": s,
        "play_jpy": p,
        "total_jpy": a + s + p,
        "appstore_detail": master_as[ym],
        "play_detail": play.get(ym),
        "admob_apps": sorted(admob_by_app.get(ym, []), key=lambda r: -r["jpy"]),
    }

out = os.path.join(SCRATCH, "revenue_master.json")
with open(out, "w") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print(f"\n{'月':8} {'AdMob':>10} {'AppStore':>10} {'Play':>8} {'合計':>10}")
for ym, d in master.items():
    print(f"{ym:8} {d['admob_jpy']:>10,} {d['appstore_jpy']:>10,} {d['play_jpy']:>8,} {d['total_jpy']:>10,}")

print("\n--- アプリ別トップ5（月毎） ---")
for ym, d in master.items():
    print(f"[{ym}]")
    for a in d["appstore_detail"]["apps"][:5]:
        if a["proceeds_jpy"] > 0:
            tops = ", ".join(f"{p['name']}¥{p['jpy']:,}" for p in a["top_products"][:2])
            print(f"  {a['title'][:38]}: ¥{a['proceeds_jpy']:,} (DL{a['downloads']:,}) [{tops}]")
print(f"\nSaved to {out}")
