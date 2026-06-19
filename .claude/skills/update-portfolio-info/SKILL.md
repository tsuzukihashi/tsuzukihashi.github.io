---
name: update-portfolio-info
description: tsuzukit.com のポートフォリオを最新化する。App Store Connectから全公開アプリ情報を取得し、新規アプリの追加・スクリーンショット反映・統計数値（アプリ数/評価/レビュー数）更新までを一括で行う。「ポートフォリオを最新に」「新しいアプリを追加」「アプリ情報を更新」や /update-portfolio-info のときに使う。
---

# ポートフォリオ最新化スキル

App Store の最新情報を取り込み、`assets/data/apps.json`（サイト描画元）と各HTMLの統計数値を一括更新する。

## 前提・場所
- リポジトリルート: `/Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com`
- 描画元: `assets/data/apps.json`（`assets/js/portfolio-renderer.js` が読み込む）
- fastlane 認証情報: `fastlane/.env`（**設定済み**。ASC_KEY_ID / ASC_ISSUER_ID / ASC_KEY_FILEPATH / VENDOR_NUMBER。`.p8` は `~/Documents/TsuzuKit/fastlane API COnnect Key/`）
  - ⚠️ `grep '^[A-Z_]+='` だと値が表示されず「空」と誤認する。値の有無は中身を見て判断すること。

## 手順

### 1. App Storeから最新情報を取得（apps_public.json 再生成）
```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com/fastlane && bundle exec fastlane fetch_public_info
```
- 全公開アプリの公開情報＋スクショを取得し `assets/data/apps_public.json` に保存。
- スクショURLは **`626x0w.webp` 形式**で出力される（Fastfile L242 で `w` クロップを生成。`bb` クロップは HTTP 400 になるため使わない。2026-06-19 修正済み）。
- 出力末尾に fastlane の更新バナーが出て結果が隠れることがある。`> /tmp/fl.log 2>&1` でログに落とし、`grep -iE "Saved|Screenshots:|error"` で確認すると良い。

### 2. apps.json へ同期＋統計数値を更新
```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com && python3 .claude/skills/update-portfolio-info/sync_portfolio.py
```
このスクリプトが自動で行うこと（冪等）:
- 既存アプリの公開フィールド（スクショ/評価/レビュー数/バージョン/説明 等）を最新化。**手動キュレーション項目（`id` / `google_play_url` / `download_count`）は保持**。
- apps_public にあって apps.json に無いアプリ＝**新規として追加**（`id` は App Store URL から抽出、`icon_url_60` は icon_url から生成）。
- `total_apps` / `categories` / 平均評価 / 総レビュー数 を再計算。
- 統計数値を各HTMLへ反映：
  - `portfolio/index.html`（title / meta×2 / ヒーロー / Published・Rating・Reviews / 件表示中）
  - `index.html`（公開中アプリ / 開発アプリ総数）
  - `about/index.html`（◯個以上のiOSアプリ / 現在◯個公開中 / History の◯個）
- スクショに `0bb.webp`（400になる形式）が混ざっていたら **exit 1 で警告**。

出力の「新規追加」「公開アプリ数（旧→新）」「⚠️要確認」を必ず読むこと。

### 3. 確認（新規アプリやスクショ変更があった場合は推奨）
- ローカルサーバ: `python3 -m http.server 8000`（未起動なら）
- Playwright で `http://localhost:8000/portfolio/` を開く。
- 注意: `portfolio-renderer.js` は `apps.json` を fetch するためブラウザがキャッシュする。最新を見るには CSSと apps.json をキャッシュバスト（`fetch('/assets/data/apps.json?cb='+Date.now(), {cache:'no-store'})`）するか、ハードリロード。
- 新規アプリがカードに出ているか、スクショが表示されるか（壊れ画像が無いか）を確認。

### 4. 報告 → コミット＆プッシュ
- スクリプトの出力（新規アプリ名・総数の変化）をユーザーに報告。
- コミット対象: `assets/data/apps.json`, `assets/data/apps_public.json`, 変更された各HTML（必要なら）。
- 例:
```bash
git add assets/data/apps.json assets/data/apps_public.json portfolio/index.html index.html about/index.html
git commit -m "feat(portfolio): アプリ情報を最新化（新規Nアプリ追加・統計更新）"
git push origin master
```
- コミットメッセージ末尾に `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` を付ける。

## 注意点（重要）
- **ダウンロード数（総ダウンロード等）はこのスキルの対象外。** iTunes の売上CSV（App Store Connect からDL）＋ Android(Playの数値) を合算して別途更新する。`index.html` / `about/index.html` の「総ダウンロード」「◯万ダウンロード」「KV画像の◯万DL」がそれ。
- **新規アプリが Android 版も持つ場合**、`google_play_url` は手動で apps.json に追加が必要（このスキルは iOS情報のみ）。Play Console の「インストール済みユーザー数」をDL合算にも反映する。
- 譲渡(9)/配信停止(6)の数は `sync_portfolio.py` 冒頭の定数 `TRANSFERRED` / `RETIRED`。変わったら更新する。
- `apps.json` にあるが App Store に無いアプリは「要確認」として表示するだけで**自動削除しない**（譲渡/配信停止の扱いは手動判断）。
- ポートフォリオのアーカイブ節（`portfolio/index.html` 内の「アーカイブしたアプリ」）は **手書きHTML**で、apps.json とは別管理。
