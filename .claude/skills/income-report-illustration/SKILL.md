---
name: income-report-illustration
description: 収益公開（月収1000万円計画）の各号に、その月だけのイラストを1枚作って記事とブログ一覧に出す。Playwright MCP で ChatGPT の画像生成を動かし、サイトのキャラクターがその月の出来事を演じる絵を作り、WebP にして置く。文字は入れない（日英で同じ絵を使うため）。monthly-income-report の途中で毎月かならず実行する。「収益記事の画像」「イラストを作って」「アイキャッチ」と言われたときも使う。
---

# 収益公開のイラスト

毎号1枚、その月の出来事を絵にして、記事の見出しの下とブログ一覧のカードに出す。
**来月からは monthly-income-report の中で、聞かずにこのスキルを回す。**（2026-10-17 ユーザー指定）

## 役目（中身を決める前に読む）

- 見る人は、Xやブログ一覧から来た個人開発者。ブログ一覧で号を見分け、記事を開いた瞬間に「その月に何があったか」の空気をつかむ
- だから絵は**その号だけの出来事**を描く。毎月同じ「コインの山」にしない。その月の desc と分析の山場から場面を1つ選ぶ
  （例: 2026-03 推しアイランドのバズ → ドット絵のハートの花火。2026-07 新作5本が売上ゼロ → 動かない紙の舟5つ）
- **文字・数字・ロゴは絶対に入れない。** 日本語と英語の両方で同じ絵を出すため。看板や画面やレシートも線と形だけにさせる
- 主役はサイトのキャラクター（黒いまるいキャラ）。毎号同じキャラが出ることで連載に見える。**参照画像を毎回添付する**

## 手順

### 1. 場面を書く

`docs/income-report/illustrations.json` に号のキーで2つ足す。

- `scenes["YYYY-MM"]`: 場面の説明（日本語、1〜3文）。キャラが何をしているか、何が置かれているか。
  共通の指示（キャラの形・色・文字禁止・3:2）は `common` に入っているので書かない
- `alt["YYYY-MM"]`: `[日本語の代替テキスト, 英語の代替テキスト]`

### 2. 生成する

```bash
python3 docs/income-report/illustration.py script YYYY-MM
```

出てきた `.playwright-mcp/gen/gen-YYYY-MM.js` を、Playwright MCP の `browser_run_code_unsafe` に `filename` で渡す。
新しい会話を開き、参照画像（`docs/income-report/mascot-ref.png`）を添付して1枚作り、
`.playwright-mcp/gen/YYYY-MM.png`（1536x1024）に保存する。1枚40〜70秒。

- ブラウザは Playwright MCP だけ。Claude in Chrome は使わない
- ChatGPT が未ログインなら、Playwright のままログインしてもらう
- **1枚ごとに新しい会話。** 同じ会話で続けると、前の絵に引きずられてキャラがずれる

### 3. 検品する（飛ばさない）

原寸で開いて目で見る。

- **文字が入っていないか。** 看板・画面・紙・本の背表紙・グラフを拡大して見る。1文字でもあれば作り直す
- キャラが参照画像どおりか（まっ黒・輪郭線なし・白い楕円の目2つだけ・口なし）
- 前の号と並べて、絵柄と色（クリーム地・紫が中心）がそろっているか
- 前の号と同じ絵を掴んでいないか（`shasum` で確かめる）

だめなら場面の文を直して2からやり直す。

### 4. WebP にして置く

```bash
python3 docs/income-report/illustration.py webp YYYY-MM
```

1200x800・品質72で `assets/images/income-report/YYYY-MM.webp` に置く。1枚20〜55KBになる（元のPNGは1.3MB前後）。

### 5. 表示する

- 記事: `generate_articles.py` が、画像と `alt` があれば見出しの下に自動で入れる。再生成するだけでよい
- ブログ一覧（`blog/index.html`）: 新しい号のカードの `post-card-image` を、前の号のカードと同じ形にする

```html
<div class="post-card-image" style="height: auto; aspect-ratio: 3 / 2;">
    <img src="/assets/images/income-report/YYYY-MM.webp" width="1200" height="800" loading="lazy"
         alt="日本語の代替テキスト" data-en-alt="英語の代替テキスト" style="width: 100%; height: 100%; object-fit: cover; display: block;">
</div>
```

カードの高さを 3:2 にしているのは、通常の128pxだと上下が切れてキャラの頭が隠れるため。

### 6. 確認

ローカルで記事とブログ一覧を日本語・英語の両方で開き、スクリーンショットで絵が出ていることを見る。

## これまでの号

2025-11〜2026-09 の11号と前史編（prehistory）は 2026-10-17 に作成済み。場面はすべて `illustrations.json` にある。
