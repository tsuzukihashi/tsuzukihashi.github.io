# Playwright MCP でChatGPTに描かせる手順

APIに課金せず、ChatGPTの契約のまま10ポーズを回すときの手順。
2026-09-16に実際に通したときの、効いたやり方と踏んだ罠を残す。

規約の話。OpenAIはAPIの外でChatGPTを自動操作することを認めていない。
アカウントを止められる可能性がある前提で使うこと。

## 前提

- ブラウザ操作は Playwright MCP のみ。Claude in Chrome は使わない
- **ログインは人がやる。** Playwrightのブラウザに `https://auth.openai.com/log-in` を出して、
  本人に入力してもらう。パスワードは受け取らない
- このログインは保たない。次に回すときはまたログインから

## 通った手順

### 1. プロンプトを localStorage に置く

1ポーズごとに700文字のプロンプトを丸ごと送ると、呼び出しが毎回巨大になる。
最初に一度だけ全部を `localStorage.__tk_prompts` に入れておくと、
以降は `JSON.parse(localStorage.getItem('__tk_prompts'))[key]` で引ける。
chatgpt.com のオリジン内なら画面を移動しても残る。

### 2. 参照画像を貼る

```js
await page.locator('#upload-photos').setInputFiles(REF);
await page.waitForTimeout(3500);   // アップロード完了を待つ
```

`#composer-plus-btn` を押してメニューから選ぶ道は、メニューのDOMが掴めず失敗した。
隠れている `input[type=file]` に直接入れるほうが速くて確実。

⚠️ **ポーズごとに毎回貼る。** 同じチャットで続けると、前に出た絵のほうを参照して
だんだんずれていく。1ポーズにつき新しいチャット（`page.goto('https://chatgpt.com/')`）を開く。

### 3. プロンプトを入れる

```js
await page.locator('#prompt-textarea').click();
await page.evaluate((t) => {
  const el = document.querySelector('#prompt-textarea');
  el.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('insertText', false, t);
}, text);
```

`fill()` や `type()` は改行でそのまま送信されてしまう。`insertText` なら
改行を保ったまま入り、Reactにも入力として伝わる。

### 4. 送信して待つ

```js
await page.locator('#composer-submit-button, button[aria-label*="プロンプトを送信"]').first().click();
```

⚠️ **生成中の判定に `[data-message-author-role="assistant"]` を使わない。**
画像の返信にはこの属性が付かず、いつまでも0件のままになる。
**`main img` のうち naturalWidth が1000以上のものが2枚（参照＋生成）になったら完了**、
で見るのが確実。1枚あたり40〜90秒かかるので、上限は160秒くらい取る。

### 5. 画像を落とす

⚠️ **画像URLを curl で叩くと 403。** cookie が要る。
⚠️ **ChatGPTの「保存」ボタンは、全画面表示にしても出たり出なかったりする。**

UIを当てにせず、ページの中で自分でダウンロードを起こすのが確実。
同一オリジンの fetch なので cookie が乗る。

```js
const [dl] = await Promise.all([
  page.waitForEvent('download', { timeout: 30000 }),
  page.evaluate(async () => {
    const imgs = [...document.querySelectorAll('main img')].filter(i => i.naturalWidth >= 1000);
    const res = await fetch(imgs[imgs.length - 1].src);
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'pose.png';
    document.body.appendChild(a); a.click(); a.remove();
  }),
]);
await dl.saveAs(DIR + 'character-' + KEY + '.png');
```

`download.saveAs()` は Playwright 側で書けるので、fs を使わずに好きな名前で保存できる
（`browser_run_code_unsafe` の中では `require` が使えない）。

### 6. 取り込む

```
python3 docs/character/import_generated.py <落としたフォルダ>
```

背景を抜いて、目と目の間隔で頭の大きさを揃えて `assets/images/` に置く。
**横向きのポーズは目が近づくので倍率が大きく出る。** 並べて見て `SCALE_FIX` で直す。

### 7. 寸法を合わせる

絵を差し替えると縦横比が変わるので、HTMLの `width` / `height` を実ファイルに合わせ直す。
そのあと `generate_articles.py` と `build_ranking.py` を回して、生成側も揃える。

## 1回あたりの所要

3ポーズで2〜4分。MCPの呼び出しは120秒でバックグラウンドに移るので、
2〜3ポーズずつに分けて投げると扱いやすい。
