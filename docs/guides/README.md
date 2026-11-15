# 検索される問いに答える記事

アプリ名ではなく、悩みの言葉（例「コンタクト 交換 アプリ」）で検索した人に届けるための記事。
1本 = JSON 1枚。`scripts/build_guides.py` が `blog/posts/<slug>.html` とサイトマップを作る。

## 1本足す手順

1. **問いを決める。** 書く前に、その語が本当に検索されているかを確かめて `evidence` に書く
   - Google の検索候補で、その語に「アプリ」「おすすめ」などが付くか
   - Google の結果の上位に、比べた記事がまだ少ないか（大手の記事が並んでいる語は避ける）
   - 自分のアプリが本当にその悩みを解決するか
2. **中身を確かめる。** 自分のアプリの機能はコードで、他社のアプリは App Store の説明文で確かめる。説明文に無いことは「記載なし」と書く
3. `docs/guides/<slug>.json` を書く（`contact-lens-reminder-apps.json` を写して直す）
   - 自分のアプリには「僕が作ったアプリ」の札が自動で付く。`disclosure` にも書く（ステマにしない）
   - 開発者名が英字でないときは `{"ja": "株式会社〇〇", "en": "〇〇 Inc."}` の形にする（英語表示で日本語を出さない）
   - 比べたアプリは、表に出したら必ずカードでも1回紹介する（スクリプトが止める）
   - 本文は skill `tsuzuki-voice` と CLAUDE.md の文章ルールで書く
4. イラストを作る（skill `blog-illustration`。キーは slug）
5. `python3 scripts/build_guides.py` で書き出す。足りないものがあれば、何が足りないかを出して止まる
6. ブログ一覧の「困りごとから選ぶアプリ」の節（新しい6本）と、全部を並べる `/blog/guides/` はスクリプトが作る。手で足さない
   - 場面だけ先に `docs/blog-illustrations.json` へ写すときは `python3 scripts/build_guides.py --sync-illustrations --draft`

HTML は直接直さない。次に書き出したときに消える。
