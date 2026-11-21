# ガチャの見た目（2026-11-21〜）

サイトそのものがカプセルトイの機械。81本のアプリがカプセルに入っていて、トップで回すと1本出る。
レア度はダウンロード数（`assets/data/apps.json` の `download_count`）。

- SSR … 10万DL以上（色 #ff3d7f）
- SR … 1万DL以上（#8a3ffc）
- R … 1000DL以上（#1f8bff）
- N … それ以外（#6b7280）

見本はいまの本番のページ（トップ・/portfolio/・/blog/・/contact/・/legal/privacy-policy.html・/404.html）。
作る前のモック（`docs/ui-patterns/v2/`）は手元だけに置いていて、リポジトリには入れていない。

## 決まりごと

| | |
|---|---|
| 地 | 赤桃 `#ff4f6d` に水玉 `#ff7a90`（30px おき） |
| 線と字 | こげ茶 `#2a1020`。板の線は 4px、影は右下に 9px ずらした塗り |
| 札 | 黄色 `#ffd23f` |
| カプセル | 上が色（6色 `--g-c1`〜`--g-c6`）、真ん中にこげ茶の帯、下が白 |
| 見出し | RocknRoll One。白い字にこげ茶の縁（-webkit-text-stroke）と影 |
| 本文 | M PLUS Rounded 1c（500 / 800） |
| キャラ | `/assets/images/character-*.png`（think・sleep・wave・cheer・peek など） |
| ロゴ | `/assets/images/logo/tsuzukit-wordmark.svg`（地が暗いところは `-white.svg`） |

ダークモードは作らない（サイトの決まり）。

## ファイル

- `assets/css/gacha.css` … 全ページ共通。土台・ヘッダー・フッター・部品（下の一覧）。部品名は全部 `g-` から始める
- `assets/css/g-*.css` … ページごとの組み方（g-top.css / g-post.css / g-apps.css / g-blog.css / g-help.css / g-legal.css / g-about.css）
- `assets/js/gacha.js` … スマホのメニュー
- `scripts/gacha_shell.py` … ヘッダー・フッター・`<head>` の行を作る。生成スクリプトはここを import する。
  手で書いたページの殻の入れ替えは `python3 scripts/gacha_shell.py <ファイル>`

## 部品（gacha.css）

| 名前 | 何 |
|---|---|
| `body.g` | ページの土台（水玉の地）。全ページの `<body>` に付ける |
| `.g-wrap` | 中身の幅（1200px・左右36px、スマホ16px） |
| `.g-head` / `.g-foot` | ヘッダー・フッター（gacha_shell.py が書く） |
| `.g-title` (`--m`) | ページの大見出し（白抜き＋縁＋影） |
| `.g-bubble` | 見出しの下の白い吹き出し |
| `.g-sh` | 節の見出し（`<div class="g-sh"><h2>…</h2><small>…</small><a class="g-btn">…</a></div>`） |
| `.g-crumb` | パンくず（白い字。今いるところは `<b>`） |
| `.g-btn` (`--k` `--y` `--big`) / `.g-btns` | ボタン |
| `.g-chip` (`.is-on`) | 絞り込みの札。数は `<i>` |
| `.g-panel` / `.g-ypanel` / `.g-paper` | 白い板・黄色い板・点線の紙 |
| `.g-cap` (`--1`〜`--6`) | カプセル。中に `<img>`（アイコン）を入れると真ん中にはまる |
| `.g-capdot` | 文の頭に置く小さなカプセル |
| `.g-mini` | カプセル＋名前（一覧の1つ分）。傾きは `style="--rot:12deg"` |
| `.g-rare` (`--SSR` `--SR` `--R` `--N`) | レア度の札 |
| `.g-burst` | 開いたカプセルからアプリが飛び出す絵（`.rays .lid .bowl .icon .st`） |
| `.g-books` / `.g-book` | 読みもののカード |
| `.g-prose` | 本文（見出し・箇条書き・表・リンク） |
| `.g-empty` | 0件・見つからないとき |

## 新しいページを作るとき

1. `<head>` は今までどおり（lang.js・Google Analytics・AdSense の meta・OGP）。CSS は `gacha_shell.head_links()` の行に替える
2. `<body class="g">` にして、ヘッダーとフッターは `gacha_shell.header()` / `footer()` の出力を貼る
3. 日本語と英語を両方書く（`.i18n-ja` / `.i18n-en`、docs/i18n.md）
4. `img { height:auto }` は gacha.css に入っている。幅と高さの属性は元の比率で書く
5. スマホ幅（390px）と PC 幅（1200px）で撮って、横はみ出しと画像の比率を見る
