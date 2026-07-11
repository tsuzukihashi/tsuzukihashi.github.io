---
name: monthly-income-report
description: 連載「限界個人開発者の月収１０００万円計画」の月次レポート記事を作成する。AdMob・App Store・Google Playの前月収益を取得し、記事生成・特設ページ更新・sitemap更新までを一括で行う。「今月の収益レポート」「◯月号を作って」「月収レポート更新」や /monthly-income-report のときに使う。
---

# 月収1000万円計画 月次レポート作成スキル

前月の収益データを3ソースから集め、記事＋特設ページ＋ブログトップを更新する。
データとスクリプトの本体は `docs/income-report/`（READMEも参照）。

## 前提・場所

- リポジトリルート: `/Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com`
- 作業ディレクトリ = `docs/income-report/`。スクリプト群は**自分のいるディレクトリのJSONを読み書きする**ので、基本ここで完結する
- fastlane 認証情報: `fastlane/.env`（設定済み。ASC_KEY_ID / ASC_ISSUER_ID / ASC_KEY_FILEPATH / VENDOR_NUMBER）
- AdMob と Play Console は API 認証が無い。**Playwright(MCP) のブラウザプロファイルが Google ログイン済み**なのでブラウザ経由で取得する（Play Console は authuser=1）
- 対象月 = 原則「先月」。Apple の月次レポートは月初5日前後に確定する

## 手順

### 1. App Store（自動）

`docs/income-report/fetch_asc_detail.rb` の `months` 配列に対象月（例 `2026-07`）を**追加**してから:

```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com/fastlane && \
SCRATCH=/Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com/docs/income-report \
bundle exec ruby ../docs/income-report/fetch_asc_detail.rb
```

- 出力: `asc_detail.json`（SKU・Parent Identifier付き明細。IAP→親アプリ帰属に必須）
- ⚠️ **AppleのMONTHLYレポートは直近約8ヶ月しか取れない**（それ以前は410/404）。毎月必ず取得すること。過去分が消えても `revenue_master.json` に集計済みなら問題ない

### 2. Google Play（ブラウザ）

1. Playwright で `https://play.google.com/console/u/1/developers/4900858120458572039/download-reports/financial` を開く
2. 収益レポート → 年 → 対象月の行を展開 → 「レポートをダウンロードしてください」リンクをクリック（zipが `.playwright-mcp/` に落ちる）
   - gcloud 認証が生きていれば `gcloud storage cp gs://pubsite_prod_4900858120458572039/earnings/earnings_YYYYMM_*.zip .` でも可
3. zip を `docs/income-report/play/YYYYMM/` に展開して `python3 parse_play.py` → `play_monthly.json` 更新
4. ⚠️ **展開した生CSV（play/ディレクトリ）はコミット禁止**。購入者の国・郵便番号を含む。コミットするのは集計済み `play_monthly.json` だけ

### 3. AdMob（ブラウザ読み取り）

1. `https://admob.google.com/v2/reports/ads-activity-admob-network/view` を開く
2. ⚠️ **期間のカスタム日付入力はPlaywrightだと値が確定せずリセットされる。プリセット（先月/全期間）だけ使う**
3. 月合計: 期間「先月」のままディメンション「月」→ 対象月の推定収益額を読む
4. アプリ内訳: ディメンション「月」＋「アプリ」（詳細オプション内）、表示行数50で上位を読む
5. `admob_monthly.json` を更新:
   - `monthly_total` に `"YYYY-MM": 金額` を追加（前月の `_partial` エントリがあれば確定値に置き換え）
   - `by_month_app_top50_2025-11_to_2026-07` 配列に対象月の上位アプリ行を追加（**キー名は歴史的なもの。build_master.py が参照しているので変えない**）
6. コピー操作が必要なときは `navigator.clipboard.readText()` を使わない（権限ダイアログで30分固まる）。**コピー後に `pbpaste` で読む**

### 4. 統合と検証

```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com/docs/income-report && python3 build_master.py
```

- 月別テーブルが出る。対象月の AdMob / App Store / Play / 合計を確認
- 為替は frankfurter.dev のECB月末レート（User-Agentヘッダ必須）。ECB非対応通貨は `STATIC_RATES_JPY` の概算
- 前月比 = (今月-前月)/前月、達成率 = 合計/10,000,000（目標は月収1000万円）

### 5. 記事生成

`generate_articles.py` の `MONTHS` 配列の**末尾に対象月のエントリを追加**して実行（全記事を冪等に再生成する）:

```bash
python3 generate_articles.py
```

エントリに書くもの: ym / date（月末日）/ label / admob / appstore / play / total / mom / rate / desc / highlights（アプリ別、revenue_master.json の appstore_detail・admob_apps・play_detail から合算）/ analysis / next_actions（3つ）/ closing。

- **文章は CLAUDE.md「文章スタイル【全文章共通・絶対遵守】」の編集ルールを通すこと**。前置き宣言・太字乱用・矢印・スラッシュ・（）多用の禁止、一人称は僕
- 分析は「何が起きたか」をデータで語り、NextActionは前号との連続性を持たせる（前号のNextActionの結果に触れる）
- 数字の捏造は絶対禁止。metaのdescも同ルール

### 6. 手動更新ファイル

| ファイル | 更新箇所 |
|---|---|
| `blog/income-report/index.html` | ①profile-status「達成率 X%」 ②goal-progress（ラベルとwidth） ③マーキーの MONTHLY ¥（**2箇所**） ④statsカード（最新月収、最高月収を超えたら差し替え） ⑤月次チャートにバー追加（高さ% = 合計/最高月収×100。最高月収が更新されたら**全バー再計算**、peakクラス移動） ⑥career-timeline の先頭に新しい号を追加 |
| `blog/index.html` | ①バナーの「最新の◯月は¥Xで達成率Y%」 ②シリーズセクションの posts-grid 先頭に新カード追加 |
| `sitemap.xml` | 新記事URL追加＋ `/blog/` と `/blog/income-report/` の lastmod 更新 |

### 7. デザイン規約（About準拠・絶対）

- 特設ページは about.css の既存クラス（about-hero / marquee / intro-stat / career-timeline）を使う
- 白カード＋インク2px枠＋色違いベタ影（purple/cyan/pink/yellow）。金額は `--font-impact` イタリックのインク色
- **虹グラデ（--grad-neon / --ab-grad）は使わない**。バーは紫単色、ピークだけ黄色
- 旧紫 #667eea 系と旧記事（2025-app-releases等）はコピー元にしない

### 8. 確認 → 報告

```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com && python3 -m http.server 8899
```

- Playwright で新記事・特設ページ・ブログトップをフルページスクリーンショットで確認
- ユーザーに月次サマリー（3ソース内訳・前月比・ハイライト）を報告
- **コミット＆プッシュはユーザーの指示があってから**:

```bash
git add blog/posts/income-report-*.html blog/income-report/index.html blog/index.html sitemap.xml \
  docs/income-report/*.json docs/income-report/fetch_asc_detail.rb docs/income-report/generate_articles.py
git commit -m "feat(blog): 月収1000万円計画 YYYY年M月号を追加"
git push origin master
```

コミットメッセージ末尾に `Co-Authored-By:` 行（実行モデル名）を付ける。

## 注意点（重要）

- AdMobは「推定収益額」、App Storeは Developer Proceeds（外貨は概算円換算）、Playは手数料控除後。この注記は記事テンプレートに組み込み済み
- 記事タイトルは「YYYY-MM-DD（月末日） 限界個人開発者の月収１０００万円計画」形式で固定
- `generate_articles.py` は全号を再生成する。過去号を手で直した場合は**必ずジェネレーター側にも反映**しておくこと（そうしないと再生成で消える）
- 収益の歴史・落とし穴の詳細は `docs/income-report/README.md` と `docs/income-report/prehistory.json` を参照
