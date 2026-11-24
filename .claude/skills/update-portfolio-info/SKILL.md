---
name: update-portfolio-info
description: tsuzukit.com のアプリの情報と数字を全部最新にする。App Store Connect から全公開アプリの情報を取って新規アプリの追加・スクショ・アプリ数/評価/レビュー数を直し、ダウンロードランキング（App Store のユニット数と Google Play の累計インストール）を取り直して、ガチャのレア度・トップと私についての総ダウンロード・代表作のDL数までそろえ、確かめて push する。最後に GitHub のプロフィール（tsuzukihashi/tsuzukihashi の README と画像）も同じ数字で作り直して push する。「ポートフォリオを最新に」「新しいアプリを追加」「アプリ情報を更新」「ランキングを更新」や /update-portfolio-info のときに使う。
---

# ポートフォリオ最新化スキル

**呼ばれたら、1章から8章まで毎回全部やる。** ランキングとDL数の更新を「必要なら」で飛ばさない。
ユーザーに頼むのはログインだけ（ASC の Playwright のログインと `! gcloud auth login`）。
ログインを待つあいだに、ログインの要らない章（1・2・3）を先に終わらせる。
**ログインのコマンドはこちらで起動しておく（2026-11-23「ログインして欲しいならコマンド用意しろ」）。** gcloud は `run_in_terminal` で `gcloud auth login` を Terminal パネルに出して起動し、本人はブラウザで承認するだけにする。`! ` を貼らせない。頼んだあとも返答を終えずに他の章を進める。

| 章 | やること | 自分で直す数字・ファイル |
|---|---|---|
| 1 | App Store の公開情報を取る | `apps_public.json` |
| 2 | apps.json へ同期 | アプリ数・評価・レビュー数（portfolio・トップ・私について・アプリのページ） |
| 3 | 新しいアプリの LP を撮る（新規があったとき） | トップのシートの絵 |
| 4 | App Store の全期間のユニット数を取る（Playwright） | `app-ranking.json` の apps |
| 5 | Google Play の累計インストールを取る | `app-ranking.json` の android |
| 6 | ランキングを作り、数字を全部そろえる | ランキングのページ・レア度・総ダウンロード・代表作のDL数 |
| 7 | 画面で確かめて、コミットして push | |
| 8 | GitHub のプロフィールを同じ数字で作り直して push | `tsuzukihashi/tsuzukihashi` の README・画像 |

## 前提・場所
- リポジトリルート: `/Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com`
- 描画元: `assets/data/apps.json`（`assets/js/portfolio-renderer.js` と `scripts/build_top_apps.py` が読む）
- fastlane 認証情報: `fastlane/.env`（**設定済み**。ASC_KEY_ID / ASC_ISSUER_ID / ASC_KEY_FILEPATH / VENDOR_NUMBER。`.p8` は `~/Documents/TsuzuKit/fastlane API COnnect Key/`）
  - ⚠️ `grep '^[A-Z_]+='` だと値が表示されず「空」と誤認する。値の有無は中身を見て判断すること。

## 1. App Store から最新情報を取得（apps_public.json 再生成）
```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com/fastlane && bundle exec fastlane fetch_public_info > /tmp/fl.log 2>&1; grep -iE "Saved|Screenshots:|error" /tmp/fl.log | tail
```
- 全公開アプリの公開情報＋スクショを取得し `assets/data/apps_public.json` に保存。
- スクショURLは **`626x0w.webp` 形式**で出力される（`bb` クロップは HTTP 400 になるため使わない。2026-06-19 修正済み）。
- **iPhone Duo のスクショ（ASC の `APP_IPHONE_DUO` の組）は使わない（2026-11-02 指示）。** 横長でカードに合わない。
  Fastfile は `APP_IPHONE_65 → 67 → 61 → 58 → 55 …` の順に**中身が1枚以上ある組**を選ぶ。
- 取り直したら、各アプリの1枚目の縦横比を測って**横長（高さ÷幅が1未満）と低解像度（`320x480bb.jpg`）が無いことを確かめる**。

## 2. apps.json へ同期＋統計数値を更新
```bash
cd /Users/tsuzuki817/workspace/TsuzuKit/tsuzukit.com && python3 .claude/skills/update-portfolio-info/sync_portfolio.py
```
このスクリプトが自動で行うこと（冪等）:
- 既存アプリの公開フィールド（スクショ/評価/レビュー数/バージョン/説明 等）を最新化。**手動キュレーション項目（`id` / `google_play_url` / `download_count`）は保持**。
- apps_public にあって apps.json に無いアプリ＝**新規として追加**（`download_count` は 0 で入り、6章で入る）。
- `total_apps` / `categories` / 平均評価 / 総レビュー数 を再計算し、`portfolio/index.html`・`portfolio/apps/*.html`・`index.html`（`scripts/build_top_apps.py`）・`about/index.html` に反映。
- スクショに `0bb.webp`（400になる形式）が混ざっていたら **exit 1 で警告**。

出力の「新規追加」「⚠️要確認」を必ず読むこと。
**新規アプリが Android 版も持つなら**、その場で apps.json に `google_play_url` を足す（このスクリプトは iOS の情報だけ）。

## 3. 新しいアプリの LP を撮る（2章で新規追加があったとき・LP を作り直したとき）
トップでアイコンを押すと出るシートは、ASC に登録した「マーケティングURL」の最初の画面を見切れさせて出す（LP が無いアプリはストアのスクショ）。
```bash
cd fastlane && bundle exec ruby ../scripts/fetch_app_urls.rb && cd ..   # ASC の LP とサポートの URL → assets/data/app_urls.json
node scripts/capture_lp_shots.mjs <新しいアプリの App Store の ID>   # 引数なしなら全部撮る
python3 scripts/build_top_apps.py
```
playwright が無い環境では `PLAYWRIGHT_MODULE=<playwright の index.mjs>` を付けて動かす。撮った画像（`assets/images/lp/`）は目で見てから入れる。

## 4. App Store の全期間のユニット数（Playwright で ASC の画面から）

**API では取れない。** 月次 salesReports は直近8ヶ月、YEARLY は2025年しか返らない。画面から取る。
ログイン画面が出たら、Playwright のウィンドウでログインしてもらう（Claude in Chrome は使わない）。

1. `https://appstoreconnect.apple.com/trends/sales` を開く
2. 指標を **ユニット数**、期間を **全期間（配信開始日から昨日まで）**、**コンテンツ** タブにする。画面に出る「〜まで」の日を控える（`--until` に使う）
3. フィルタの **コンテンツタイプ** を「iOS, watchOS, tvOS, and visionOS App Purchases」にする（URL に `filter_content_type=22` が付く）。課金商品の行を外すため
4. `browser_run_code_unsafe` で「さらに表示」を押し切る:
   ```js
   async (page) => { for (let i = 0; i < 20; i++) { const b = page.getByText('さらに表示', { exact: true }); if (!(await b.count())) break; await b.first().click(); await page.waitForTimeout(2000); } return await page.locator('tr').count(); }
   ```
5. `browser_evaluate` に `filename: ".playwright-mcp/asc-units-all.json"` を付けて表を書き出す（`run_code` の中では `require('fs')` が使えない）:
   ```js
   () => JSON.stringify([...document.querySelectorAll('tr')].map(tr => [...tr.querySelectorAll('td,th')].map(c => c.innerText.replace(/\s+/g, ' ').trim())))
   ```
6. **ASC の表は上から100行で切れる。** 100行あったら、期間を **過去30日間** にして 4〜5 をもう一度やり、`.playwright-mcp/asc-units-30d.json` に書き出す（最近出したアプリの数をここから取る）
7. 取り込む:
   ```bash
   python3 scripts/merge_asc_units.py .playwright-mcp/asc-units-all.json --until <控えた日> --recent .playwright-mcp/asc-units-30d.json
   ```
   - 開発者名が **Ryo Tsudukihashi の App 行だけ**を入れる（預かりアプリ9本と課金商品は入れない）
   - 表から切れたアプリは、30日以内に出したものは30日の表の数、それ以外は前回の数（全期間の数は減らない）
   - 「⚠️ 配信終了のアプリが新しく入った」が出たら、`app-ranking.json` のその名前を日本語に直し、`docs/build_ranking.py` の `NAMES_EN` に英語名を足す
   - 画面の数は3桁に丸められている（`211K` など）。入る値も概数

## 5. Google Play の累計インストール
```bash
python3 scripts/fetch_play_installs.py
```
- Play Console のインストール レポート（GCS の `stats/installs/*_overview.csv`）を全部読み、`Daily User Installs` の全期間の合計を累計インストール、最新日の `Active Device Installs` を稼働台数にして、`app-ranking.json` の android を作り直す
- 「gcloud のトークンが取れない」で止まったら、`run_in_terminal` で `gcloud auth login` を Terminal パネルに起動し、ブラウザで承認だけしてもらう。
  ⚠️ このマシンでは `gcloud storage` も `gsutil` も動かない（Python 3.9 で落ちる）ので、スクリプトはトークンだけ借りて GCS の JSON API を読んでいる
- Play だけのアプリ（iOS 版なし）の名前とアイコンは Play のページから取る。⚠️ が出たら `NAMES_EN` に英語名を足す
- `Active Device Installs` は Play Console の一覧に出る「インストール済みユーザー数」で、累計ではない。累計 < 稼働台数のアプリもある（1人が複数端末に入れた）。矛盾ではない

## 6. ランキングを作り、数字を全部そろえる
```bash
python3 docs/build_ranking.py
```
これ1本で次を全部やる:
- `/portfolio/ranking/` のページを作る（App Store の合計・Google Play の合計・両方の合算 `grand_total`）
- `scripts/apply_ranking_downloads.py` … apps.json の `download_count` に「App Store のユニット数＋Play の累計インストール」を入れる。ガチャのレア度（SSR 10万・SR 1万・R 1000）と並び順はこの数で決まる
- `scripts/apply_download_totals.py` … トップと私についての総ダウンロード（「81万+」「810K+」）、トップの代表作のDL数（「290,000+」）、私についての「流れるメモ帳が◯万、全部合わせて◯万ダウンロード」を直す。数は切り捨てて「+」を付ける
- `scripts/build_top_apps.py` … トップのガチャ（レア度の一覧・回すデータ）を作り直す

出力の「⚠️」を読む。**代表作の絵（`assets/images/works/*.webp`）には「◯万DL」が焼き込まれている。** 出力の代表作の数と絵の数字が合っているかを目で見て、ずれていたら絵を作り直す。

## 7. 確かめて、コミットして push
- ローカルサーバ（`python3 -m http.server 8765` を裏で）を立て、Playwright で PC 幅（1280）とスマホ幅（390）の `/`・`/portfolio/`・`/portfolio/ranking/`・`/about/` を開く
  - 横はみ出し（`scrollWidth - innerWidth`）が0、壊れた画像（`src` があって `naturalWidth` が0）が無い
  - トップのレア度の一覧・総ダウンロード・ランキングの合計が 6章の出力と同じ
  - 新しいアプリがカードに出ていて、スクショが出ている
  - `portfolio-renderer.js` は `apps.json` を fetch するので、URL に `?cb=<時刻>` を付けて開く
- 撮った絵は SendUserFile で会話に出す
- 自分が触ったファイルだけをコミットして push する（聞かない。skill `commit-only-my-changes`）:
```bash
git add assets/data/apps.json assets/data/apps_public.json assets/data/app-ranking.json \
  index.html about/index.html portfolio/index.html portfolio/ranking/index.html portfolio/apps docs/build_ranking.py
# LP を撮ったなら
git add assets/data/app_urls.json assets/data/lp_shots.json assets/images/lp
git diff --cached --stat   # 他の作業の変更が混ざっていないか見る
git commit -m "feat(portfolio): アプリ情報とランキングを最新化（新規Nアプリ・合計◯万）" -- <上で add したパス>
git push origin master
```
- コミットメッセージ末尾に `Co-Authored-By: 実行したモデル名 <noreply@anthropic.com>` を付ける。
- 報告には、新規アプリ・公開数・App Store と Play と合計の変化・レア度が変わったアプリを書く。

## 8. GitHub のプロフィールを作り直す（tsuzukihashi/tsuzukihashi）
https://github.com/tsuzukihashi の README。サイトと同じガチャの見た目で、数字は 6章までで出来たサイトのデータ（`apps.json`・`app-ranking.json`）から作る。
置き場所はサイトのリポジトリの隣の `tsuzukihashi`。無ければ clone する。
```bash
SITE="$(git rev-parse --show-toplevel)"; PROFILE="$(dirname "$SITE")/tsuzukihashi"
[ -d "$PROFILE" ] || gh repo clone tsuzukihashi/tsuzukihashi "$PROFILE"
cd "$PROFILE" && git pull --ff-only origin master
python3 design/sync.py --site "$SITE"
git diff --quiet -- README.md design/data.js && echo "プロフィールの数字は変わらない"
```
- 「変わらない」と出たら、画像は作り直さずに終わる（コミットしない）
- 変わったら画像を作り直す:
```bash
bash design/render.sh
```
- `sync.py` が直すもの … 公開アプリ数、総ダウンロード、個人開発の年数、レア度ごとの種類数とカプセルのアイコン、大当たり4本（うんちくん・流れるメモ帳・旅行思い出マップ・推しアイランド）のレア度・DL数・評価
- README は `design/README.template.md` の `{{key}}` を埋めて作る。**README.md を直接直さない。** 文を変えたいときはテンプレートを直す
- 数はサイトと同じく切り捨てて「+」を付ける。評価は 4.0 未満なら出さない
- `render.sh` は Chrome（`/Applications/Google Chrome.app`）で `design/cards.html` を2倍の透過 PNG にする。フォントは Google Fonts から読むのでネットが要る
- 書き出した `assets/hero.png`・`assets/lineup.png`・`assets/pick-*.png` を Read で見て、数字がサイトと合っていること、文字が枠からはみ出していないことを確かめる。絵は SendUserFile で会話に出す
- 大当たりの4本を入れ替えるときは、`design/sync.py` の `PICKS`、`design/cards.html` の `PICKS`（名前・一言・アイコン）、`README.template.md` のリンクと alt を一緒に直す。「⚠️ apps.json に無い」が出たらそのアプリが外れたということなので、本人に聞く
- 10年のあゆみの中身（各年の出来事）と実績の文は手書き。このスキルでは触らない
- 7章と同じく、聞かずにコミットして push する:
```bash
git add README.md assets design/data.js
git diff --cached --stat
git commit -m "docs: プロフィールの数字を tsuzukit.com にそろえる（◯本・◯万DL）"   # 末尾に Co-Authored-By
git push origin master
```
- 報告に、プロフィールで変わった数字を書く

## 注意点（重要）
- **DL数を推定で増やさない。** 2026-09-15、全期間の累計値に直近10ヶ月ぶんを足して水増しした
  （流れるメモ帳を18万にしたが実測は16.7万）。数字は 4・5章で取った実測だけを使い、手で書き足さない。
- トップの「使命」の節にある「うんちくんは21万人」「猫背リマインダーに3,640人」は出どころが別（ランキングではない）。このスキルでは触らない。
- 譲渡(9)/配信停止(6)の数は `sync_portfolio.py` 冒頭の定数 `TRANSFERRED` / `RETIRED`。変わったら更新する。
- `apps.json` にあるが App Store に無いアプリは「要確認」として表示するだけで**自動削除しない**（譲渡/配信停止の扱いは手動判断）。
- ポートフォリオのアーカイブ節（`portfolio/index.html` 内の「アーカイブしたアプリ」）は **手書きHTML**で、apps.json とは別管理。
