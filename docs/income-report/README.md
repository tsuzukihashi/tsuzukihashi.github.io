# 限界個人開発者の月収１０００万円計画 - データパイプライン

月次収益レポート記事（`/blog/posts/income-report-YYYY-MM.html`）と
特設ページ（`/blog/income-report/`）を更新するためのデータとスクリプト。

## 毎月の更新手順

### 1. App Store（自動）

```bash
cd fastlane
SCRATCH=/path/to/workdir bundle exec ruby ../docs/income-report/fetch_asc_detail.rb
```

- `fetch_asc_detail.rb` 内の `months` 配列に対象月を追加してから実行する
- 認証は `fastlane/.env`（ASC_KEY_ID / ASC_ISSUER_ID / ASC_KEY_FILEPATH / VENDOR_NUMBER）
- 出力: `asc_detail.json`（SKU・Parent Identifier付きの明細。IAP→親アプリ帰属に必要）
- 注意: AppleのMONTHLYレポートは概ね直近8ヶ月しか取得できない（それ以前は410 GONE）

### 2. Google Play（手動ダウンロード or ブラウザ）

- Play Console → レポートのダウンロード → 売上 → 収益レポート → 対象月のzipをダウンロード
- GCSバケット: `gs://pubsite_prod_4900858120458572039/earnings/`
  （`earnings_YYYYMM_*.zip`。gcloud認証があれば `gcloud storage cp` でも可）
- zipを `play/YYYYMM/` に展開して `parse_play.py` を実行 → `play_monthly.json`

### 3. AdMob（ブラウザで読み取り）

- AdMob管理画面 → レポート → AdMobネットワーク → 期間指定＋ディメンション「月」
- 月合計と、ディメンション「月＋アプリ」の上位を `admob_monthly.json` に追記
- 使う指標は「推定収益額」（JPY）

### 4. 統合と記事生成

```bash
python3 build_master.py       # → revenue_master.json（3ソース統合・円換算）
python3 generate_articles.py  # → blog/posts/income-report-*.html を生成
```

- `generate_articles.py` の `MONTHS` 配列に新月のデータ＋分析文＋NextActionを追記してから実行
- 為替は frankfurter.dev（ECB月末レート）。ECB非対応通貨は `STATIC_RATES_JPY` の概算値

### 5. 手動更新が必要なファイル

| ファイル | 内容 |
|---|---|
| `blog/income-report/index.html` | 最新月ステータスカード・グラフのバー・レポート一覧に1件追加 |
| `blog/index.html` | 月収1000万円計画セクションにカード追加＋バナーの最新月数値 |
| `sitemap.xml` | 新記事のURL追加・blogのlastmod更新 |

## データの注意点

- AdMob = 推定収益額（確定額と数%ずれる）
- App Store = Developer Proceeds（手数料控除後）。外貨は月末レート換算の概算
- Google Play = Charge - Google fee（Merchant Currency: JPY）
- 目標: 月収 ¥10,000,000。達成率 = 月合計 / 1000万

## 前史編（2019〜2025）について - 2026-07-11 追記

- 記事: `blog/posts/income-report-prehistory.html`、データ: `prehistory.json`
- **初収益は 2019-07 の AdMob ¥21**（表示254回・クリック3回）
- AdMobの月次は全期間取得可能（admob_monthly.json に2019-07から収録済み）
- **App Storeの過去データは取得不可**: 月次salesReportsは直近約8ヶ月のみ（それ以前は410/404）、
  YEARLYは2025のみ存在（¥77,323≒11-12月分）、financeReportsもFY2026-P3以前は404
  → 前史期間のApp Store課金収益は実質ゼロと確認
- AdMob管理画面の期間カスタム入力（開始日/終了日のテキスト入力）はPlaywrightからだと
  値が確定せずリセットされる。**プリセット「全期間」を使って後からフィルタする**方が確実
