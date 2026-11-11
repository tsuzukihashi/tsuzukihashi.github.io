"""トップページ（アプリの利用者向け）の骨組み案を、実データで描く。
python3 docs/top-redesign/build_wire.py → docs/top-redesign/wire.html"""
import json, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
apps = json.load(open(ROOT/'assets/data/apps.json'))['apps']
pop = sorted(apps, key=lambda x: -(x.get('download_count') or 0))
new = sorted(apps, key=lambda x: x['current_version_release_date'], reverse=True)
rc = sum(x['rating_count'] for x in apps)
avg = sum((x['rating'] or 0)*x['rating_count'] for x in apps)/rc
e = html.escape
def short(n): return e(n.split(' ')[0].split('　')[0].split('-')[0].split('～')[0][:9])
def icon(x, s=56, name=True):
    n = f'<div class="nm">{short(x["name"])}</div>' if name else ''
    return f'<div class="ic"><img src="{x["icon_url"].replace("512x512bb","120x120bb")}" style="width:{s}px;height:{s}px">{n}</div>'
def note(t): return f'<div class="note">{t}</div>'
def box(t, h=None, cls='box'):
    st = f' style="min-height:{h}px"' if h else ''
    return f'<div class="{cls}"{st}>{t}</div>'
HEAD = '<div class="hdr"><b>TsuzuKit</b><span>≡</span></div>'
SEARCH = '<div class="search">🔍 アプリの名前で探す</div>'
TRUST = f'<div class="trust"><div><b>{len(apps)}本</b><br>公開中</div><div><b>★{avg:.1f}</b><br>{rc:,}件の評価</div><div><b>79万</b><br>ダウンロード</div></div>'

def frame(title, sub, body, w=390):
    return f'<section><h2>{title}</h2><p class="sub">{sub}</p><div class="phone" style="width:{w}px">{body}</div></section>'

# 案1 いまを残して直す
p1 = HEAD + box('<div class="kick">iPhoneアプリを1人で作っています</div><div class="big">續橋涼（TsuzuKit）</div><div class="small">誰も作らないものを、まじめに作る。</div>', cls='hero') \
   + note('「10年間の軌跡」のバッジと WHO NEEDS THIS? は小さくして、何者かを1行で') + TRUST \
   + note('数字はいまの「数字で見る」欄を上に上げる。評価は apps.json から計算') \
   + '<h3>アプリを探す</h3>' + SEARCH + '<div class="grid g4">' + ''.join(icon(x) for x in pop[:12]) + '</div>' \
   + '<div class="btn">81本ぜんぶ見る →</div>' + note('押すと /portfolio/（検索と絞り込みは今もある）') \
   + '<h3>代表作</h3>' + box('うんちくん・流れるメモ帳・旅行思い出マップ・推しアイランド（今の絵のまま）', 90) \
   + '<h3>アプリのことで困ったら</h3>' + box('お問い合わせ（/contact/）・プライバシーポリシー・利用規約', 60) \
   + note('年表「10年間、諦めなかった理由」は About に移す') + box('ブログ・About へのリンク', 40, 'box dim')

# 案2 アプリの棚が主役
p2 = HEAD + '<div class="kick2">續橋涼が1人で作っている<br><b>81本のiPhoneアプリ</b></div>' + SEARCH \
   + '<div class="chips"><span class="on">新しい順</span><span>人気順</span><span>記録する</span><span>写真</span><span>推し活</span><span>…</span></div>' \
   + note('「記録する」などの分け方は今のデータに無い。81本に手で付ける（primary_genre は Lifestyle が19本で粗い）') \
   + '<div class="grid g4">' + ''.join(icon(x) for x in new) + '</div>' \
   + note('81本ぜんぶ。アイコンは apps.json の icon_url（120px に縮めて読む）') \
   + box('<b>作っている人</b><br>2016年から1人で。9本は会社に譲渡。→ About', 70) + box('困ったとき：お問い合わせ／プライバシーポリシー', 40)

ux = next(x for x in apps if x['bundle_id']=='com.tsuzukit.PoopCounter')
gp = '<div class="btn ghost">Google Play で開く</div>' if ux.get('google_play_url') else ''
sheet = '<div class="dim-bg">' + '<div class="grid g4">' + ''.join(icon(x) for x in new[:16]) + '</div></div>' \
   + f'<div class="sheet"><div class="row">{icon(ux,64,False)}<div><b>{e(ux["name"][:22])}</b><br><span class="small">★{ux["rating"]:.1f}（{ux["rating_count"]}件）・{e(ux["genres"][0])}</span></div></div>' \
   + '<div class="btn">App Store で開く</div>' + gp \
   + '<div class="list"><div>使い方・よくある質問</div><div>お問い合わせ</div><div>プライバシーポリシー</div><div>利用規約</div></div>' \
   + note('サポートとプライバシーの行き先は、アプリごとに違う（47本は共通の /contact/、10本ほどは専用ページ）。apps.json に項目を足す') + '</div>'

# 案3 アプリ別の窓口
p3 = HEAD + '<div class="kick2">どのアプリについて<br>知りたいですか？</div>' + '<div class="search typed">🔍 うんち<span class="caret">|</span></div>' \
   + '<div class="list res">' + ''.join(f'<div class="rrow">{icon(x,40,False)}<span>{e(x["name"][:20])}</span></div>' for x in apps if 'うんち' in x['name'] or 'PoopCounter' in x['bundle_id'])[:2000] + '</div>' \
   + note('入力するたびに81本の名前から絞る（apps.json の name）') \
   + '<h3>よく見られているアプリ</h3><div class="grid g4">' + ''.join(icon(x) for x in pop[:8]) + '</div>' \
   + box('ほかの79本もある → /portfolio/', 40, 'box dim')
p3b = HEAD + f'<div class="row big2">{icon(ux,72,False)}<div><b>{e(ux["name"][:22])}</b><br><span class="small">バージョン {ux["version"]}・{ux["current_version_release_date"][:10]} 更新</span></div></div>' \
   + '<div class="btn">App Store で開く</div>' \
   + '<h3>最新のお知らせ</h3>' + box(e(ux['release_notes'][:120]) + '…', 80) + note('apps.json の release_notes と version をそのまま出す') \
   + '<h3>困ったとき</h3><div class="list"><div>よくある質問</div><div>お問い合わせ（このアプリ名を入れて開く）</div><div>プライバシーポリシー</div></div>' \
   + '<h3>同じ人のほかのアプリ</h3><div class="grid g4">' + ''.join(icon(x) for x in pop[:4] if x is not ux) + '</div>'
p3c = HEAD + '<div class="search typed">🔍 ぴよぴよ<span class="caret">|</span></div>' \
   + box('<b>「ぴよぴよ」のアプリは見つかりませんでした</b><br><span class="small">ストアの名前の一部（ひらがな・カタカナ・英語）で試してください。<br>見つからないアプリのことは、お問い合わせから聞いてください。</span><div class="btn">お問い合わせ</div><div class="btn ghost">81本ぜんぶ見る</div>', 160, 'box empty') \
   + note('検索が0件のとき')

CSS = '''body{margin:0;padding:40px;background:#f6f2ea;font-family:"Hiragino Sans",sans-serif;color:#14110c}
.wrap{display:flex;gap:36px;align-items:flex-start}
section{width:auto}
h1{font-size:30px;margin:0 0 8px}
.lead{margin:0 0 28px;font-size:15px}
h2{font-size:20px;margin:0}
.sub{font-size:13px;margin:4px 0 12px;width:390px;line-height:1.5}
.phone{background:#fff;border:2px solid #14110c;border-radius:28px;overflow:hidden;padding:0 14px 18px;box-sizing:border-box;position:relative}
.hdr{display:flex;justify-content:space-between;background:#14110c;color:#fff;margin:0 -14px 12px;padding:12px 16px;font-size:15px}
.hero{background:#eee;border-radius:12px;padding:18px;margin-bottom:8px}
.kick{font-size:12px;color:#555}.big{font-size:22px;font-weight:800;margin:4px 0}.small{font-size:12px;color:#555}
.kick2{font-size:18px;line-height:1.5;margin:8px 0 10px}
.trust{display:flex;gap:6px;margin:6px 0}.trust div{flex:1;background:#f3f3f3;border-radius:10px;padding:8px;font-size:11px;text-align:center}.trust b{font-size:17px}
h3{font-size:15px;margin:16px 0 8px}
.search{border:1.5px solid #bbb;border-radius:12px;padding:11px 12px;font-size:14px;color:#888;margin-bottom:10px}
.search.typed{color:#14110c;border-color:#14110c}.caret{color:#8b3df5}
.grid{display:grid;gap:10px 6px}.g4{grid-template-columns:repeat(4,1fr)}
.ic{text-align:center}.ic img{border-radius:22%;display:block;margin:0 auto;border:1px solid #ddd}.nm{font-size:10px;margin-top:3px;white-space:nowrap;overflow:hidden}
.btn{background:#14110c;color:#fff;border-radius:999px;text-align:center;padding:11px;font-size:14px;margin:10px 0 4px}
.btn.ghost{background:#fff;color:#14110c;border:1.5px solid #14110c}
.box{background:#f1f1f1;border-radius:12px;padding:12px;font-size:12px;margin:8px 0;line-height:1.6}
.box.dim{color:#777}.box.empty{background:#fff;border:1.5px dashed #bbb;text-align:center}
.note{font-size:11px;color:#8b3df5;border-left:3px solid #8b3df5;padding:2px 0 2px 8px;margin:6px 0 10px;line-height:1.5}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px}.chips span{font-size:12px;border:1.5px solid #ccc;border-radius:999px;padding:4px 10px}.chips .on{background:#14110c;color:#fff;border-color:#14110c}
.dim-bg{opacity:.25}
.sheet{position:absolute;left:0;right:0;bottom:0;background:#fff;border-top:2px solid #14110c;border-radius:22px 22px 0 0;padding:16px 16px 20px;box-shadow:0 -6px 20px rgba(0,0,0,.15)}
.row{display:flex;gap:12px;align-items:center}.row b{font-size:14px}.big2{margin:10px 0}
.list>div{border-bottom:1px solid #eee;padding:11px 4px;font-size:14px}.list>div::after{content:" ›";float:right;color:#999}
.res .rrow{display:flex;gap:10px;align-items:center}
'''
out = f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>{CSS}</style></head><body>
<h1>トップページの骨組み案（アプリの利用者向け）</h1>
<p class="lead">来る人: App Store でアプリのページを見ていて「デベロッパWebサイト」を押した人（66本中47本がトップを指している）。ほとんどが iPhone。紫の札は、データの出どころと足りないもの。</p>
<div class="wrap">
{frame("案1 いまを残して直す", "変える幅は小。ヒーローを1行の自己紹介にし、その下に信頼の数字と「アプリを探す」を入れる。年表は About へ。", p1)}
{frame("案2 アプリの棚が主役", "変える幅は大。開いた瞬間に81本が並ぶ。押すとそのアプリの窓口（ストア・困ったとき・プライバシー）が下から出る。", p2)}
{frame("案2 アイコンを押したとき", "下から出るシート。ページは移らない。", sheet + '<div style="height:520px"></div>')}
{frame("案3 アプリ別の窓口", "変える幅は大。最初に「どのアプリ？」と聞く。来たアプリを探して、そのアプリの最新のお知らせと困ったときの行き先へ。", p3)}
{frame("案3 アプリを選んだあと", "1本ぶんの窓口。release_notes はいまのデータにある。", p3b)}
{frame("案3 検索が0件のとき", "空状態。", p3c)}
</div></body></html>'''
(ROOT/'docs/top-redesign/wire.html').write_text(out)
print('ok', len(out))
