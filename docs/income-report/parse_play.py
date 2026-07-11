#!/usr/bin/env python3
"""Google Play earnings CSV を月次集計する"""
import csv
import json
import os
import sys
from collections import defaultdict

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PLAY_DIR = os.path.join(SCRATCH, "play")

result = {}

for month_dir in sorted(os.listdir(PLAY_DIR)):
    dir_path = os.path.join(PLAY_DIR, month_dir)
    if not os.path.isdir(dir_path):
        continue
    month_key = f"{month_dir[:4]}-{month_dir[4:6]}"
    apps = defaultdict(lambda: {"title": "", "gross_jpy": 0, "fee_jpy": 0, "tax_jpy": 0, "net_jpy": 0, "transactions": 0})
    totals = {"gross_jpy": 0, "fee_jpy": 0, "tax_jpy": 0, "net_jpy": 0}

    for fname in os.listdir(dir_path):
        if not fname.endswith(".csv"):
            continue
        with open(os.path.join(dir_path, fname), encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pkg = row["Package ID"]
                ttype = row["Transaction Type"]
                amount = int(row["Amount (Merchant Currency)"])
                app = apps[pkg]
                if not app["title"]:
                    app["title"] = row["Product Title"]
                if ttype in ("Charge", "Charge refund"):
                    app["gross_jpy"] += amount
                    totals["gross_jpy"] += amount
                    if ttype == "Charge":
                        app["transactions"] += 1
                elif ttype in ("Google fee", "Google fee refund"):
                    app["fee_jpy"] += amount
                    totals["fee_jpy"] += amount
                elif "Tax" in ttype:
                    app["tax_jpy"] += amount
                    totals["tax_jpy"] += amount
                else:
                    # 想定外の取引種別も net に反映されるよう記録
                    app["tax_jpy"] += amount
                    totals["tax_jpy"] += amount
                    print(f"  note: unknown type '{ttype}' {amount} JPY", file=sys.stderr)
                app["net_jpy"] = app["gross_jpy"] + app["fee_jpy"] + app["tax_jpy"]

    totals["net_jpy"] = totals["gross_jpy"] + totals["fee_jpy"] + totals["tax_jpy"]
    result[month_key] = {"totals": totals, "apps": dict(apps)}
    print(f"{month_key}: gross={totals['gross_jpy']} fee={totals['fee_jpy']} tax={totals['tax_jpy']} net={totals['net_jpy']} JPY, apps={len(apps)}")

out_path = os.path.join(SCRATCH, "play_monthly.json")
with open(out_path, "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved to {out_path}")
