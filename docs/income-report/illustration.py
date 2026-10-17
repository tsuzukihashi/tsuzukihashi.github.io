#!/usr/bin/env python3
"""収益公開の各号のイラストを作るための補助スクリプト。

  python3 docs/income-report/illustration.py script 2026-10
      → .playwright-mcp/gen/gen-2026-10.js を書き出す。
        Playwright MCP の browser_run_code_unsafe に filename で渡すと、
        ChatGPT の新しい会話で参照画像を添付し、絵を1枚作って .playwright-mcp/gen/2026-10.png に保存する
  python3 docs/income-report/illustration.py webp 2026-10
      → 1200x800 の WebP にして assets/images/income-report/2026-10.webp に置く

場面と代替テキストは docs/income-report/illustrations.json に号ごとに書く。
手順の全体は .claude/skills/income-report-illustration/SKILL.md。
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(REPO, "docs/income-report/illustrations.json")
REF = os.path.join(REPO, "docs/income-report/mascot-ref.png")
GEN_DIR = os.path.join(REPO, ".playwright-mcp/gen")
OUT_DIR = os.path.join(REPO, "assets/images/income-report")

TEMPLATE = r'''async (page) => {
  const KEY = __KEY__;
  const PROMPT = __PROMPT__;
  const REF = __REF__;
  const OUT = __OUT__;
  await page.goto('https://chatgpt.com/');
  await page.waitForSelector('div.ProseMirror[contenteditable="true"]', { timeout: 30000 });
  await page.waitForTimeout(1500);
  await page.locator('input[type=file][accept="image/*"][multiple]').first().setInputFiles(REF);
  await page.waitForTimeout(5000);
  await page.locator('div.ProseMirror[contenteditable="true"]').click();
  await page.evaluate((t) => { document.execCommand('insertText', false, t); }, PROMPT);
  await page.waitForTimeout(800);
  await page.keyboard.press('Enter');
  const start = Date.now();
  let last = null;
  while (Date.now() - start < 300000) {
    await page.waitForTimeout(8000);
    const info = await page.evaluate(() => {
      const g = [...document.querySelectorAll('img')].filter(i => /^生成画像/.test(i.alt) && i.complete && i.naturalWidth >= 800);
      const busy = /細部を仕上げ中|画像を作成中|生成中|Creating image/.test(document.body.innerText);
      return { src: g.length ? g[g.length - 1].src : null, busy };
    });
    // 生成中の表示が消え、同じ絵が2回続けて見えたら完成とみなす
    if (info.src && !info.busy && info.src === last) break;
    last = info.src;
  }
  if (!last) return 'TIMEOUT ' + KEY;
  const [dl] = await Promise.all([
    page.waitForEvent('download', { timeout: 30000 }),
    page.evaluate(async (src) => {
      const blob = await (await fetch(src)).blob();
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'x.png';
      document.body.appendChild(a); a.click(); a.remove();
    }, last),
  ]);
  await dl.saveAs(OUT);
  return 'saved ' + OUT + ' ' + Math.round((Date.now() - start) / 1000) + 's';
}'''


def write_script(key):
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    if key not in d["scenes"]:
        sys.exit(f"illustrations.json の scenes に {key} がありません")
    os.makedirs(GEN_DIR, exist_ok=True)
    code = (TEMPLATE.replace("__KEY__", json.dumps(key))
            .replace("__PROMPT__", json.dumps(d["common"] + d["scenes"][key], ensure_ascii=False))
            .replace("__REF__", json.dumps(REF))
            .replace("__OUT__", json.dumps(os.path.join(GEN_DIR, key + ".png"))))
    path = os.path.join(GEN_DIR, f"gen-{key}.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(os.path.relpath(path, REPO))


def to_webp(key):
    src = os.path.join(GEN_DIR, key + ".png")
    dst = os.path.join(OUT_DIR, key + ".webp")
    os.makedirs(OUT_DIR, exist_ok=True)
    subprocess.run(["magick", src, "-resize", "1200x800", "-strip", "-quality", "72",
                    "-define", "webp:method=6", dst], check=True)
    print(os.path.relpath(dst, REPO), os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("script", "webp"):
        sys.exit(__doc__)
    {"script": write_script, "webp": to_webp}[sys.argv[1]](sys.argv[2])
