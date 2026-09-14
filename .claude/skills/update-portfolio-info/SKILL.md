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

### 4. ダウンロードランキングの更新（/portfolio/ranking/）

データは `assets/data/app-ranking.json`、ページは `python3 docs/build_ranking.py` で生成する。

#### App Store（全期間のユニット数）

App Store Connect → トレンド → 売上 → **ユニット数** → 期間「全期間（配信開始日から昨日まで）」→ **コンテンツ**タブ。
一覧（名前・タイプ・Apple ID・ユニット数）をコピーして JSON に落とす。

- 開発者名が **Ryo Tsudukihashi の App 行だけ**を採用する。他の開発者名義（預かりアプリ9本）と
  `In App`（課金商品）は除く
- 画面表示は3桁に丸められている（`211K` など）。JSONに入れる値も概数になる
- **APIでは取れない。** 月次 salesReports は直近8ヶ月、YEARLY は2025年しか返らない

#### Google Play（全期間の累計インストール）

⚠️ **このマシンでは `gcloud storage` も `gsutil` も動かない**（Python 3.9 非対応で
`module 'importlib.metadata' has no attribute 'packages_distributions'` になる）。
**トークンだけ gcloud から借りて、curl で GCS の JSON API を叩く。**

```bash
# 認証が切れていたら「Reauthentication failed」になる。
# その場合はユーザーに ! gcloud auth login を打ってもらう（対話が要るのでこちらからは実行できない）
TOKEN=$(gcloud auth print-access-token)

# ① インストールレポートの一覧（*_overview.csv がアプリ×月ぶん並ぶ）
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://storage.googleapis.com/storage/v1/b/pubsite_prod_4900858120458572039/o?prefix=stats/installs/&fields=items(name)&maxResults=1000"

# ② 個別ファイルの取得（オブジェクト名は / を %2F にエンコードして、alt=media を付ける）
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://storage.googleapis.com/storage/v1/b/pubsite_prod_4900858120458572039/o/stats%2Finstalls%2Finstalls_com.tsuzukit.poopcounter_202609_overview.csv?alt=media"
```

CSVはUTF-16のことがあるので `utf-16 → utf-8-sig → utf-8` の順にデコードを試す。列の意味:

| 列 | 意味 |
|---|---|
| `Daily User Installs` | その日の新規ユーザー。**全期間合算したものが累計インストール数**（App Storeのユニット数に相当） |
| `Active Device Installs` | いま動いている端末数。**Play Console の一覧に出る「インストール済みユーザー数」はこれ**で、累計ではない |
| `Total User Installs` | 値が入っていない（0）。使えない |

- ユーザー数とデバイス数は単位が違うので、**累計 < 稼働台数**になるアプリもある（1人が複数端末に入れた場合）。矛盾ではない
- Play Console の画面から手で落とす場合は「レポートのダウンロード → 統計情報」。
  ダウンロードURLは `https://storage.cloud.google.com/pubsite_prod_4900858120458572039/stats/installs/installs_{パッケージ名}_{YYYYMM}_overview.csv?authuser=1`

#### 生成

```bash
python3 docs/build_ranking.py
```

App Store の合計・Google Play の合計・両方の合算（`grand_total`）がページに出る。
`index.html` の「総ダウンロード」と代表作のDL数も、この数字に合わせて直すこと。

### 5. 報告 → コミット＆プッシュ
- スクリプトの出力（新規アプリ名・総数の変化）をユーザーに報告。
- コミット対象: `assets/data/apps.json`, `assets/data/apps_public.json`, 変更された各HTML（必要なら）。
- 例:
```bash
git add assets/data/apps.json assets/data/apps_public.json portfolio/index.html index.html about/index.html
# ランキングも更新したなら
git add assets/data/app-ranking.json portfolio/ranking/index.html docs/build_ranking.py
git commit -m "feat(portfolio): アプリ情報を最新化（新規Nアプリ追加・統計更新）"
git push origin master
```
- コミットメッセージ末尾に `Co-Authored-By: 実行したモデル名 <noreply@anthropic.com>` を付ける。

## 注意点（重要）
- **ダウンロード数は手順4で別に更新する。** `index.html` / `about/index.html` の「総ダウンロード」「◯万ダウンロード」「KV画像の◯万DL」も、ランキングと同じ数字に合わせること。
  KV画像（`assets/images/works/*.webp`）は**画像の中に数字が焼き込まれている**ので、数字を変えたら作り直しが要る。
- **既存の「◯万DL」を推定で増やさない。** 2026-09-15、全期間の累計値に直近10ヶ月ぶんを足して水増しした
  （流れるメモ帳を18万にしたが実測は16.7万）。既存値がいつ時点のものか分からないときは、実測が取れるまで触らない。
- **新規アプリが Android 版も持つ場合**、`google_play_url` は手動で apps.json に追加が必要（このスキルは iOS情報のみ）。
- 譲渡(9)/配信停止(6)の数は `sync_portfolio.py` 冒頭の定数 `TRANSFERRED` / `RETIRED`。変わったら更新する。
- `apps.json` にあるが App Store に無いアプリは「要確認」として表示するだけで**自動削除しない**（譲渡/配信停止の扱いは手動判断）。
- ポートフォリオのアーカイブ節（`portfolio/index.html` 内の「アーカイブしたアプリ」）は **手書きHTML**で、apps.json とは別管理。
