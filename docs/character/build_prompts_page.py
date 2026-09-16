#!/usr/bin/env python3
"""キャラのポーズ生成プロンプトを、ボタンひとつでコピーできるページにする。

    python3 docs/character/build_prompts_page.py && open docs/character/prompts.html

ポーズを足したいときは POSES に1行足すだけ。参照画像はページに埋め込むので、
このHTML1枚をどこに置いても動く。
"""
import base64
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "reference-peek.png")
OUT = os.path.join(HERE, "prompts.html")

SPEC = """添付した画像のキャラクターを、まったく同じ造形のまま別のポーズで描いてください。
似た雰囲気の新しいキャラクターを作るのではなく、同一人物として描いてください。

■ 造形（変えてはいけないところ）
・黒一色のベタ塗りシルエット。輪郭線なし、グラデーションなし、影なし、質感なし
・頭と胴はつながったひと続きの丸い塊。首はない。おもちのようにやわらかく、角や尖った部分がどこにもない
・顔にあるのは目だけ。口も鼻も眉も頬も描かない
・目は縦長の小さな楕円が2つ。黒を塗り残した穴で、背景の色がそのまま見えている。2つとも頭の傾きと同じ角度に傾き、顔の上のほうにある
・目の大きさは頭の幅の8分の1くらい。奥側の目をわずかに小さくして向きを出す
・腕は根元が太く先に向かって細くなり、先端は丸い。指はない。ミトンかヒレの形
・足は丸い塊を2つ。体との境目は線ではなく、細い背景色の隙間で区切る
・頭が全体の3分の2を占める。重心が低く、ずんぐりしている

■ 画面
・背景は #f6f2ea のクリーム一色。柄も影もグラデーションも敷かない
・正方形、1024×1024以上
・キャラクターは1体だけ。周りに余白をとり、画面いっぱいに描かない

■ 入れてはいけないもの
文字、ロゴ、枠線、地面や床の線、効果線、キラキラ、ハート、汗マーク、吹き出し、背景の小物、他のキャラクター、色（黒とクリーム以外）"""

# 既定は全身。切れた絵はこちらで元に戻せないが、全身ならどこでも切れる。
# ふちを使うポーズ（ぶら下がる・頭だけ出す）だけ A を使う。
FRAME = {
    "B": """■ フレーム
全身を入れる。腕も足も切らず、体のどこも画面の外に出さない。地面や影は描かず、何もない空間に置く。上下左右に均等な余白をとる。""",
    "A": """■ フレーム
画面の下辺で、体が水平にすっぱり切れている。見えない棚のふちの向こう側からこちらを覗いている状態で、ふちより下の体は描かない。切れ目は必ずまっすぐな水平線。""",
}

# (ファイル名, 見出し, フレーム, 置き場所, ポーズの本文)
POSES = [
    ("character-peek", "素の顔", "B", "全ページのフッター、法務ページ",
     "立ったままこちらをまっすぐ見ている。片手を軽く前に出している。目は開いていて、落ち着いた顔。"),
    ("character-sleep", "眠っている", "B", "収益公開の達成率バーの右端",
     "座りこんで眠っている。目は閉じていて、上にゆるくふくらんだ弧が2本。頭が少し前に傾き、腕は体の横に力なく垂れている。"),
    ("character-wink", "ウインク", "B", "トップのCTA",
     "片目をつぶってウインクしている。つぶった目は上にふくらんだ弧、もう片方は開いた縦長の楕円。片手を軽く上げている。"),
    ("character-wave", "手を振る", "B", "ブログ一覧",
     "片手を高く上げて手を振っている。上げた手は根元から先へ向かってのびやかに曲がる。目は開いている。"),
    ("character-think", "考えこむ", "B", "Aboutの署名の横",
     "片手を頭の横に添えて考えこんでいる。目は細めた弧で、視線をやや外している。"),
    ("character-surprised", "驚いている", "B", "404、検索0件",
     "両目を大きく見開いて驚いている。目はいつもより縦に長い楕円。両手を顔の横まで上げ、体をわずかに後ろへ引いている。"),
    ("character-cheer", "万歳", "B", "ランキングの1位",
     "両手をまっすぐ上に伸ばして喜んでいる。体は少し浮き、目は弧を描いて笑っている。"),
    ("character-run", "走る", "B", "Contact、ファビコン",
     "横を向いて走っている。体を進行方向へ傾け、腕と足を前後に振っている。目は進む方向を見ている。"),
    ("character-hang", "ぶら下がる", "A", "記事の読み終わり",
     "ふちに両手だけをかけて、顔を下からのぞかせている。体はふちの下にぶら下がっている。目は開いている。"),
    ("character-tiny", "頭だけちょこん", "A", "ポートフォリオの絞り込みバー",
     "ふちのすぐ上に頭のてっぺんと目だけを出している。体はふちに隠れて見えない。目は上目づかいでこちらを見ている。"),
]



def full_prompt(frame, pose):
    return f"{SPEC}\n\n{FRAME[frame]}\n\n■ ポーズ\n{pose}"


def main():
    ref = base64.b64encode(io.open(REF, "rb").read()).decode()
    items = [{
        "file": f, "title": t, "frame": fr, "place": pl,
        "pose": pose, "text": full_prompt(fr, pose),
    } for f, t, fr, pl, pose in POSES]

    html = TEMPLATE.replace("__DATA__", json.dumps(items, ensure_ascii=False)) \
                   .replace("__REF__", ref)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"{OUT} を書いた（{len(items)}ポーズ）")


TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>キャラのポーズ生成プロンプト - TsuzuKit</title>
<style>
  :root { --bg:#f6f2ea; --ink:#14110c; --sub:#57514a; --line:rgba(20,17,12,.16); }
  * { box-sizing: border-box; }
  body {
    margin:0; padding:40px 24px 80px; background:var(--bg); color:var(--ink);
    font-family:-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif; line-height:1.8;
  }
  .wrap { max-width:940px; margin:0 auto; }
  h1 { font-size:1.5rem; margin:0 0 6px; }
  .lead { color:var(--sub); font-size:.92rem; margin:0 0 28px; }

  .ref {
    display:flex; gap:20px; align-items:center; background:#fff;
    border:2px solid var(--ink); border-radius:16px; box-shadow:6px 6px 0 var(--ink);
    padding:18px 20px; margin-bottom:34px;
  }
  .ref img { width:120px; height:120px; border:2px solid var(--ink); border-radius:12px; cursor:grab; }
  .ref div { flex:1; min-width:0; }
  .ref b { display:block; margin-bottom:4px; }
  .ref p { margin:0; font-size:.88rem; color:var(--sub); }
  .ref code { background:var(--bg); padding:2px 6px; border-radius:5px; font-size:.82rem; word-break:break-all; }

  .card {
    background:#fff; border:2px solid var(--ink); border-radius:16px;
    box-shadow:6px 6px 0 var(--ink); padding:18px 20px 20px; margin-bottom:22px;
  }
  .head { display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:12px; }
  .no { font-weight:800; font-size:1.05rem; }
  .tag { font-size:.72rem; font-weight:700; border:2px solid var(--ink); border-radius:999px; padding:2px 10px; }
  .place { font-size:.82rem; color:var(--sub); margin-left:auto; }
  .fname { font-size:.76rem; color:var(--sub); font-family:ui-monospace,monospace; }

  button {
    font:inherit; font-weight:700; font-size:.85rem; cursor:pointer;
    background:var(--ink); color:#fff; border:2px solid var(--ink);
    border-radius:999px; padding:7px 18px; transition:transform .15s ease;
  }
  button:hover { transform:translate(-1px,-1px); }
  button.done { background:#fff; color:var(--ink); }

  .pose {
    margin:0 0 12px; padding:13px 16px; background:var(--bg);
    border:1px solid var(--line); border-radius:10px; font-size:.92rem;
  }
  pre {
    margin:0; padding:14px 16px; background:var(--bg); border:1px solid var(--line);
    border-radius:10px; white-space:pre-wrap; word-break:break-word;
    font-family:ui-monospace,SFMono-Regular,monospace; font-size:.78rem; line-height:1.75;
  }
  pre[hidden] { display:none; }
  .more { background:none; color:var(--sub); border-color:var(--line); margin-bottom:10px; }

  .note { margin-top:34px; font-size:.86rem; color:var(--sub); }
  .note li { margin-bottom:6px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>キャラのポーズ生成プロンプト</h1>
  <p class="lead">ボタンを押すと、その1ポーズぶんの全文がクリップボードに入ります。ChatGPTに貼るだけ。<br>ほとんどのポーズは<b>全身</b>で描いてもらいます。切れた絵は元に戻せませんが、全身ならこちらで好きな位置で切れるからです。</p>

  <div class="ref">
    <img id="ref" alt="参照画像">
    <div>
      <b>先にこの画像を添付してください</b>
      <p>この絵をそのままドラッグしてChatGPTに落とせます。ファイルから入れる場合は
      <code>~/Downloads/tsuzukit-character-reference.png</code></p>
    </div>
  </div>

  <div id="list"></div>

  <ul class="note">
    <li>同じチャットの中で10個続けて出してください。チャットを分けると頭の丸みや目の位置がぶれます。</li>
    <li>左端に置くぶんはこちらで左右反転するので、反転版は頼まなくて大丈夫です。</li>
    <li>出てきたらDownloadsに保存して、ファイル名を伝えてください。背景を抜いて大きさを揃えて配ります。</li>
    <li>いま入っている8枚は下で切れた版です。全身で描き直すと置ける場所が増えます。</li>
  </ul>
</div>

<script>
const REF = "data:image/png;base64,__REF__";
const ITEMS = __DATA__;
document.getElementById('ref').src = REF;

function copyText(t) {
  const ta = document.createElement('textarea');
  ta.value = t;
  ta.style.cssText = 'position:fixed;left:-9999px;top:0';
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  ta.remove();
  if (!ok && navigator.clipboard) { navigator.clipboard.writeText(t); ok = true; }
  return ok;
}

const list = document.getElementById('list');
ITEMS.forEach((it, i) => {
  const card = document.createElement('div');
  card.className = 'card';

  const head = document.createElement('div');
  head.className = 'head';
  head.innerHTML = '<span class="no">' + (i + 1) + '. ' + it.title + '</span>'
    + '<span class="tag">' + (it.frame === 'A' ? 'ふちから覗く' : '全身') + '</span>'
    + '<span class="fname">' + it.file + '.png</span>'
    + '<span class="place">' + it.place + '</span>';

  const btn = document.createElement('button');
  btn.textContent = 'プロンプトをコピー';
  btn.onclick = () => {
    if (copyText(it.text)) {
      btn.textContent = 'コピーしました';
      btn.classList.add('done');
      setTimeout(() => { btn.textContent = 'プロンプトをコピー'; btn.classList.remove('done'); }, 1600);
      return;
    }
    // ブラウザに止められたときは全文を開いて選択しておく。あとは Cmd+C でよい
    pre.hidden = false;
    more.textContent = '閉じる';
    const r = document.createRange();
    r.selectNodeContents(pre);
    const sel = getSelection();
    sel.removeAllRanges();
    sel.addRange(r);
    btn.textContent = '全文を選択しました。⌘Cを押してください';
    btn.classList.add('done');
  };
  head.appendChild(btn);

  const pose = document.createElement('p');
  pose.className = 'pose';
  pose.textContent = it.pose;

  const pre = document.createElement('pre');
  pre.textContent = it.text;
  pre.hidden = true;

  const more = document.createElement('button');
  more.className = 'more';
  more.textContent = 'コピーされる全文を見る';
  more.onclick = () => {
    pre.hidden = !pre.hidden;
    more.textContent = pre.hidden ? 'コピーされる全文を見る' : '閉じる';
  };

  card.append(head, pose, more, pre);
  list.appendChild(card);
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
