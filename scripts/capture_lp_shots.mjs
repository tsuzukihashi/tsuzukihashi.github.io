// トップのアプリのシートに見切れて出す、各アプリの LP の最初の画面を iPhone の幅で撮る。
//   node scripts/capture_lp_shots.mjs            … LP のあるアプリを全部撮る
//   node scripts/capture_lp_shots.mjs 6758856276 … 1本だけ撮り直す（App Store の ID）
//
// - LP の行き先は assets/data/app_urls.json（scripts/fetch_app_urls.rb が ASC から取る）
// - トップ自身・空欄・bento.me（プロフィールのページで LP ではない）は撮らない。シートはストアのスクショを出す
// - GA・広告は読み込ませない（撮るだけで LP の閲覧数や広告の表示が増えないように）
// - 書き出し先: assets/images/lp/<id>-ja.jpg と <id>-en.jpg、一覧は assets/data/lp_shots.json
//
// playwright は npm の playwright を使う。入っていない環境では PLAYWRIGHT_MODULE に index.mjs のパスを渡す。
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const mod = process.env.PLAYWRIGHT_MODULE ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href : 'playwright';
const { chromium, devices } = await import(mod);

const urls = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/data/app_urls.json'), 'utf8'));
const outDir = path.join(ROOT, 'assets/images/lp');
const listPath = path.join(ROOT, 'assets/data/lp_shots.json');
fs.mkdirSync(outDir, { recursive: true });
const list = fs.existsSync(listPath) ? JSON.parse(fs.readFileSync(listPath, 'utf8')) : {};

const isOwnLp = (u) => {
  if (!u) return false;
  const s = u.trim().replace(/^https?:\/\/(www\.)?/, '').replace(/\/+$/, '').replace(/\/index\.html$/, '');
  // tsuzukihashi.github.io はこのサイトの古い住所（トップへ転送される）
  if (s === '' || s === 'tsuzukit.com' || s === 'tsuzukihashi.github.io') return false;
  if (s.startsWith('bento.me')) return false;
  return true;
};

// トップに出すのはポートフォリオにあるアプリだけ（ASC には配信を止めたアプリも残っている）
const shown = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/data/apps.json'), 'utf8')).apps.map((a) => String(a.id)));
const only = process.argv[2] || null;
const targets = Object.entries(urls).filter(([id, v]) => shown.has(id) && (only === null || id === only) && isOwnLp(v.marketing_url?.ja));

const BLOCK = /googletagmanager|google-analytics|googlesyndication|doubleclick|adservice\.google|analytics\.google/;
const browser = await chromium.launch({ channel: 'chrome', headless: true });

for (const [id, v] of targets) {
  const entry = { url: { ja: v.marketing_url.ja, en: v.marketing_url.en || v.marketing_url.ja }, shots: {} };
  for (const lang of ['ja', 'en']) {
    const url = entry.url[lang];
    const ctx = await browser.newContext({
      ...devices['iPhone 13'],
      deviceScaleFactor: 2, // 780px 幅。シートの中では 390px 以下で出すので2倍で足りる
      locale: lang === 'ja' ? 'ja-JP' : 'en-US',
      extraHTTPHeaders: { 'Accept-Language': lang === 'ja' ? 'ja-JP,ja;q=0.9' : 'en-US,en;q=0.9' },
    });
    // lang.js はブラウザの第一言語で出し分けるので、navigator.languages もそろえる
    await ctx.addInitScript((l) => {
      Object.defineProperty(navigator, 'languages', { get: () => [l] });
      Object.defineProperty(navigator, 'language', { get: () => l });
    }, lang === 'ja' ? 'ja-JP' : 'en-US');
    await ctx.route('**/*', (r) => (BLOCK.test(r.request().url()) ? r.abort() : r.continue()));
    const page = await ctx.newPage();
    let status = 0;
    try {
      const res = await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      status = res ? res.status() : 0;
    } catch (e) {
      console.log(`${id} ${lang} networkidle を待てなかった（${e.message.split('\n')[0]}）。そのまま撮る`);
      status = 200;
    }
    if (status >= 400) {
      // 登録された LP が開けない。シートはストアのスクショを出す
      console.log(`${id} ${lang} ${url} は ${status}。撮らない`);
      await ctx.close();
      entry.broken = true;
      break;
    }
    await page.waitForTimeout(2500);
    // 200 を返しても「ページが見つかりません」を出すところがある（Notion の消したページなど）
    const text = await page.evaluate(() => (document.body ? document.body.innerText : '').slice(0, 2000)).catch(() => '');
    if (text.length < 600 && /見つかりませんでした|page not found|this page (could not|couldn't) be found|404/i.test(text)) {
      console.log(`${id} ${lang} ${url} は「見つかりません」のページ。撮らない`);
      await ctx.close();
      entry.broken = true;
      break;
    }
    const file = `${id}-${lang}.jpg`;
    await page.screenshot({ path: path.join(outDir, file), type: 'jpeg', quality: 78, clip: { x: 0, y: 0, width: 390, height: 760 } });
    entry.shots[lang] = `/assets/images/lp/${file}`;
    console.log(`${id} ${lang} ${url} -> ${file}`);
    await ctx.close();
  }
  if (entry.broken) {
    for (const f of Object.values(list[id]?.shots || {})) fs.rmSync(path.join(ROOT, f), { force: true });
    delete list[id];
  } else {
    list[id] = entry;
  }
}
await browser.close();

// LP が無くなったアプリは一覧から外す（画像は残さない）
for (const id of Object.keys(list)) {
  if (!shown.has(id) || !urls[id] || !isOwnLp(urls[id].marketing_url?.ja)) {
    for (const f of Object.values(list[id].shots || {})) fs.rmSync(path.join(ROOT, f), { force: true });
    delete list[id];
  }
}
fs.writeFileSync(listPath, JSON.stringify(list, null, 2) + '\n');
console.log(`lp_shots.json: ${Object.keys(list).length} 本`);
