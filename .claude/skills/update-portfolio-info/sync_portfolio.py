#!/usr/bin/env python3
"""
sync_portfolio.py — tsuzukit.com ポートフォリオ同期スクリプト

前提: 先に `cd fastlane && bundle exec fastlane fetch_public_info` を実行し、
      assets/data/apps_public.json を最新化しておくこと（スクショは 626x0w 形式で出力される）。

このスクリプトがやること:
  1) apps_public.json（App Storeの最新公開情報・全公開アプリ）を読む
  2) apps.json（サイト描画元）の既存アプリの公開フィールド（スクショ/評価/バージョン等）を最新化
     ※ 手動キュレーション項目（id / google_play_url / download_count）は保持
  3) apps_public にあって apps.json に無いアプリ＝新規 として追加（id は App Store URL から抽出）
  4) total_apps / categories / 評価 / レビュー数 を再計算
  5) 各HTMLの統計数値（アプリ数・公開中・開発総数・評価・レビュー数）を更新
  6) 変更サマリを出力

冪等: 何度実行しても同じ結果。新規が無く数値も最新なら「変更なし」になる。
"""
import json
import os
import re
import sys
import datetime

# --- データ外の固定値（変わったらここを更新） ---
TRANSFERRED = 9   # 企業へ譲渡済みのアプリ数
RETIRED = 6       # ストア配信停止中のアプリ数

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
APPS = os.path.join(ROOT, "assets", "data", "apps.json")
PUBLIC = os.path.join(ROOT, "assets", "data", "apps_public.json")

# apps_public から取り込む公開フィールド（毎回上書きして最新化）
# ※ bundle_id を含めることで build_new で追加した新規アプリにも bundle_id が入り、
#   かつ既存アプリへ backfill される（過去 bundle_id 無しで追加された分の補完）。
PUBLIC_FIELDS = [
    "name", "bundle_id", "app_store_url", "icon_url", "screenshots", "ipad_screenshots",
    "price", "currency", "genres", "primary_genre", "rating", "rating_count",
    "version", "release_date", "current_version_release_date",
    "description", "release_notes", "content_advisory_rating",
    "minimum_os_version", "developer_name", "seller_name",
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def id_from_url(url):
    m = re.search(r"/id(\d+)", url or "")
    return int(m.group(1)) if m else None


def icon60(icon_url):
    # .../512x512bb.jpg -> .../60x60bb.jpg
    return re.sub(r"/\d+x\d+bb\.(jpg|png)$", r"/60x60bb.\1", icon_url or "")


def build_new(pub):
    """apps_public のエントリから apps.json 用の完全エントリを生成"""
    e = {"id": id_from_url(pub.get("app_store_url"))}
    for k in PUBLIC_FIELDS:
        e[k] = pub.get(k)
    e["icon_url_60"] = icon60(pub.get("icon_url"))
    e["download_count"] = 0
    return e


def sub_count(text, pattern, value, changes, label):
    """pattern は (接頭)(数値)(接尾) の3グループ。数値(group2)を value に置換し、前後は維持。"""
    new, n = re.subn(pattern, lambda m: f"{m.group(1)}{value}{m.group(3)}", text)
    if n == 0:
        changes.append(f"   ⚠️  パターン未検出（HTML構造変更の可能性）: {label}")
    return new


def update_html(published, developed, reviews, rating, changes):
    rev = f"{reviews:,}"
    rat = f"{rating:.1f}"

    pf = os.path.join(ROOT, "portfolio", "index.html")
    t = open(pf, encoding="utf-8").read()
    before = t
    t = sub_count(t, r"(\| )(\d+)( Apps on App Store)", published, changes, "portfolio <title>")
    t = sub_count(t, r"(開発した)(\d+)(のiOSアプリ)", published, changes, "portfolio meta(開発した)")
    t = sub_count(t, r'(content=")(\d+)(のiOSアプリ、平均評価)', published, changes, "portfolio meta(twitter)")
    t = sub_count(t, r"(平均評価)([\d.]+)([。、])", rat, changes, "portfolio meta(平均評価)")
    t = sub_count(t, r"()([\d,]+)(件のレビュー)", rev, changes, "portfolio meta(レビュー)")
    t = sub_count(t, r'(<span class="text-gradient">)(\d+)(</span> Apps)', published, changes, "portfolio hero")
    t = sub_count(t, r'(<div class="portfolio-stat-number">)(\d+)(</div>\s*<div class="portfolio-stat-label">Published)', published, changes, "portfolio stat Published")
    t = sub_count(t, r'(<div class="portfolio-stat-number">)([\d.]+)(</div>\s*<div class="portfolio-stat-label">Rating)', rat, changes, "portfolio stat Rating")
    t = sub_count(t, r'(<div class="portfolio-stat-number">)([\d,]+)(</div>\s*<div class="portfolio-stat-label">Reviews)', rev, changes, "portfolio stat Reviews")
    t = sub_count(t, r'(id="filterResults">)(\d+)(件表示中)', published, changes, "portfolio filterResults")
    if t != before:
        open(pf, "w", encoding="utf-8").write(t)
        changes.append("   ✏️  portfolio/index.html")

    ix = os.path.join(ROOT, "index.html")
    t = open(ix, encoding="utf-8").read()
    before = t
    t = sub_count(t, r'(<div class="stat-number">)(\d+)(</div>\s*<div class="stat-label">公開中アプリ)', published, changes, "index 公開中アプリ")
    t = sub_count(t, r'(<div class="stat-number">)(\d+)(\+</div>\s*<div class="stat-label">開発アプリ総数)', developed, changes, "index 開発アプリ総数")
    if t != before:
        open(ix, "w", encoding="utf-8").write(t)
        changes.append("   ✏️  index.html")

    ab = os.path.join(ROOT, "about", "index.html")
    t = open(ab, encoding="utf-8").read()
    before = t
    t = sub_count(t, r"(これまでに<strong>)(\d+)(個以上のiOSアプリ</strong>)", developed, changes, "about 開発個数")
    t = sub_count(t, r"(現在<strong>)(\d+)(個</strong>がApp)", published, changes, "about 公開中個数")
    t = sub_count(t, r"()(\d+)(個以上のアプリを開発し、多くの挑戦)", developed, changes, "about History 個数")
    if t != before:
        open(ab, "w", encoding="utf-8").write(t)
        changes.append("   ✏️  about/index.html")


def main():
    pub = load(PUBLIC)
    app = load(APPS)
    # 照合キーは App Store の数値 id（apps.json は全件 id を保持、apps_public は
    # app_store_url から導出できる）。bundle_id は過去に build_new で追加した
    # アプリで欠落しうるため、照合キーには使わない（重複追加の原因になる）。
    pub_by_id = {}
    for src in pub["apps"]:
        aid = src.get("id") or id_from_url(src.get("app_store_url"))
        if aid is not None:
            pub_by_id[aid] = src

    refreshed, new_added, stale = [], [], []
    seen = set()

    # 既存アプリの公開フィールドを最新化（キュレーション項目は保持）
    for a in app["apps"]:
        aid = a.get("id") or id_from_url(a.get("app_store_url"))
        src = pub_by_id.get(aid)
        if not src:
            stale.append(a.get("name"))
            continue
        seen.add(aid)
        changed = False
        for k in PUBLIC_FIELDS:
            if k in src and a.get(k) != src.get(k):
                a[k] = src.get(k)
                changed = True
        new60 = icon60(a.get("icon_url"))
        if a.get("icon_url_60") != new60:
            a["icon_url_60"] = new60
            changed = True
        if changed:
            refreshed.append(a.get("name"))

    # 新規アプリを追加（id で照合済みなので既存とは重複しない）
    for aid, src in pub_by_id.items():
        if aid in seen:
            continue
        entry = build_new(src)
        app["apps"].append(entry)
        new_added.append(f"{entry['name']} (id={entry['id']}, shots={len(entry.get('screenshots') or [])})")

    # 集計の再計算
    app["total_apps"] = len(app["apps"])
    cats = {}
    for a in app["apps"]:
        g = a.get("primary_genre") or "Unknown"
        cats[g] = cats.get(g, 0) + 1
    app["categories"] = cats
    app["generated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    published = app["total_apps"]
    developed = published + TRANSFERRED + RETIRED
    rc = sum((a.get("rating_count") or 0) for a in app["apps"])
    rating = (sum((a.get("rating") or 0) * (a.get("rating_count") or 0) for a in app["apps"]) / rc) if rc else 0.0

    with open(APPS, "w", encoding="utf-8") as f:
        json.dump(app, f, ensure_ascii=False, indent=2)

    changes = []
    update_html(published, developed, rc, rating, changes)

    # サマリ出力
    print("=" * 64)
    print("ポートフォリオ同期 完了")
    print("=" * 64)
    print(f"公開アプリ数 (total_apps): {published}")
    print(f"開発総数 (公開{published} + 譲渡{TRANSFERRED} + 停止{RETIRED}): {developed}")
    print(f"平均評価: {rating:.1f}  /  総レビュー数: {rc:,}")
    print(f"\n新規追加: {len(new_added)}")
    for s in new_added:
        print(f"  + {s}")
    print(f"\n情報更新された既存アプリ: {len(refreshed)}")
    for s in refreshed[:30]:
        print(f"  ~ {s}")
    if stale:
        print(f"\n⚠️  apps.json にあるが App Store に見当たらない（要確認・自動削除しない）: {len(stale)}")
        for s in stale:
            print(f"  ? {s}")
    print("\nHTML更新:")
    for c in changes:
        print(c)
    # スクショ形式チェック（bb=400 になる事故防止）
    bad = sum(1 for a in app["apps"] for s in (a.get("screenshots") or []) if "0bb.webp" in s)
    if bad:
        print(f"\n❌ 警告: 400になるスクショURL(...0bb.webp)が {bad}件。Fastfileのクロップ符号(w)を確認！")
        sys.exit(1)
    print("\n✅ スクショURLは全て正常形式(626x0w)。")


if __name__ == "__main__":
    main()
