---
name: blog-illustration
description: ブログ記事（blog/posts/）に、その記事だけのイラストを1枚作って記事とブログ一覧のカードに出す。Playwright MCP で ChatGPT の画像生成を動かし、サイトのキャラクター（黒いまるいキャラ）が記事の中身を演じる絵を作り、WebP にして置く。文字は入れない（日英で同じ絵を使うため）。新しい記事を作るとき（収益公開の月次レポート、アプリ紹介、開発記など）は毎回かならず実行する。「記事の画像」「イラストを作って」「アイキャッチ」と言われたときも使う。
---

# ブログ記事のイラスト

**記事は全部イラスト付き。** 新しい記事を作ったら、聞かずにこのスキルを回す（2026-10-17 ユーザー指定「記事は全部画像入れて欲しい」）。
収益公開の月次レポート（monthly-income-report）からも呼ばれる。

## 役目（中身を決める前に読む）

- 見る人は、Xやブログ一覧から来た人。一覧で記事を見分け、開いた瞬間に「何の記事か」の空気をつかむ
- だから絵は**その記事だけの場面**を描く。使い回しの「コインの山」「パソコンに向かう姿」で済ませない
  - 収益公開: その月の山場（例: 2026-03 推しアイランドのバズ → ドット絵のハートの花火。2026-07 新作5本が売上ゼロ → 動かない紙の舟5つ）
  - アプリ紹介: そのアプリで何ができるかを、キャラが使っている場面で（例: 猫背リマインダー → 机で猫に見張られて背筋を伸ばす）
  - 開発記・読み物: 記事の山場
- **文字・数字・ロゴは絶対に入れない。** 日本語と英語で同じ絵を出すため。看板、画面、紙、レシート、名札も線と形だけにさせる
- 主役はサイトのキャラクター。どの記事にも同じキャラが出ることでサイトの絵に見える。**参照画像を毎回添付する**
- 他社のキャラ（うんちくんのうんち等）は描かせない。参照画像が無いと崩れるので、ハートや小物で表す

## 手順

キーは記事のファイル名（`blog/posts/<key>.html` の `<key>`。収益公開は `income-report-YYYY-MM`）。

### 1. 場面を書く

`docs/blog-illustrations.json` にキーで2つ足す。

- `scenes[key]`: 場面の説明（日本語、1〜3文）。キャラが何をしているか、何が置かれているか。
  共通の指示（キャラの形・色・文字禁止・3:2）は `common` に入っているので書かない
- `alt[key]`: `[日本語の代替テキスト, 英語の代替テキスト]`

### 2. 生成する

```bash
python3 scripts/blog_illustration.py script <key>
```

出てきた `.playwright-mcp/gen/gen-<key>.js` を、Playwright MCP の `browser_run_code_unsafe` に `filename` で渡す。
新しい会話を開き、参照画像（`docs/mascot-ref.png`）を添付して1枚作り、
`.playwright-mcp/gen/<key>.png`（1536x1024）に保存する。1枚40〜90秒。

- ブラウザは Playwright MCP だけ。Claude in Chrome は使わない
- ChatGPT が未ログインなら、Playwright のままログインしてもらう
- **1枚ごとに新しい会話**（スクリプトがそうしている）。同じ会話で続けると前の絵に引きずられてキャラがずれる
- `page.goto: net::ERR_ABORTED` で落ちることがある。同じスクリプトをもう一度流せば通る

### 3. 検品する（飛ばさない）

- 何枚か作ったら `magick montage` で一覧にして、キャラ（まっ黒・輪郭線なし・白い楕円の目2つ・口なし）と絵柄がそろっているかを見る
  （このマシンの magick montage はラベル用フォントが無いと終了コード1を返すが、画像はできている）
- **文字が入っていないか。** 画面・看板・紙・本の背表紙・グラフは原寸で切り出して見る。1文字でもあれば作り直す
- 前の絵と同じものを掴んでいないか（`shasum -a 256` で重複を見る）

だめなら場面の文を直して2からやり直す。

### 4. WebP にして置く

```bash
python3 scripts/blog_illustration.py webp <key>
```

1200x800・品質72で `assets/images/posts/<key>.webp` に置く。1枚20〜60KB（元のPNGは1.3MB前後）。

### 5. 表示する

- **記事本文**
  - 収益公開: `docs/income-report/generate_articles.py` が自動で見出しの下に入れる。再生成するだけ
  - アプリ紹介（`app-*`）: `scripts/generate_app_blogs.py` がヒーローの下に入れる。ただしこのスクリプトを全体で回すと手直し済みの日本語が上書きされる（docs/i18n.md 参照）ので、既存ページには下の `<figure>` を手で足す
  - 手書きの記事: `</header>` の直後に足す

```html
        <figure class="post-illustration"><img src="/assets/images/posts/<key>.webp" width="1200" height="800" alt="日本語" data-en-alt="English" fetchpriority="high"></figure>
```

  スタイルは `assets/css/style.css` の `.post-illustration`。

- **ブログ一覧（`blog/index.html`）のカード**: `post-card-image` をこの形にする

```html
<div class="post-card-image" style="height: auto; aspect-ratio: 3 / 2;">
    <img src="/assets/images/posts/<key>.webp" width="1200" height="800" loading="lazy"
         alt="日本語" data-en-alt="English" style="width: 100%; height: 100%; object-fit: cover; display: block;">
</div>
```

  カードの高さを 3:2 にしているのは、通常の高さだと上下が切れてキャラの頭が隠れるため。

### 6. 確認

ローカルで記事とブログ一覧を日本語・英語の両方で開き、スクリーンショットで絵が出ていることを見る。
ブログ一覧はスクロールが効かない作りなので、`fullPage: true` で撮って `magick -crop` で切り出す。

## これまでの記事

2026-10-17 に、blog/posts/ の62本すべて（収益公開12本・アプリ紹介44本・読み物6本）に作成済み。場面は `docs/blog-illustrations.json`。
