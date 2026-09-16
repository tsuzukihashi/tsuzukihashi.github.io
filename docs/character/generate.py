#!/usr/bin/env python3
"""キャラのポーズをOpenAIのImages APIで描かせて、そのままサイトに置ける形にする。

    python3 docs/character/generate.py                          # 全ポーズ
    python3 docs/character/generate.py sleep wink               # 名前を指定して描き直し
    python3 docs/character/generate.py --model gpt-image-2.5-flare sleep

ポーズの一覧とプロンプトは build_prompts_page.py と同じものを読む。
文言を直したいときはあちらの POSES / SPEC / FRAME をいじれば、ページも生成も両方変わる。

やること
  1. 参照画像（reference-peek.png）とプロンプトを /v1/images/edits に投げる
  2. 返ってきた絵のクリーム背景を抜いて、黒＋アルファにする
  3. 目と目の間隔で頭の大きさを揃える
  4. assets/images/character-<名前>.png に置く
  5. 生のままの絵も docs/character/raw/ に残す。取り込みをやり直したいとき用

APIキー
  環境変数 OPENAI_API_KEY か、リポジトリ直下の .env（OPENAI_API_KEY=... の1行）。
  .env は .gitignore に入れてあるのでコミットされない。
"""
import argparse
import base64
import io
import os
import sys
import warnings

warnings.filterwarnings("ignore")

import requests
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(HERE, "raw")
REF = os.path.join(HERE, "reference-peek.png")
OUT = os.path.join(REPO, "assets", "images")

sys.path.insert(0, HERE)
from build_prompts_page import POSES, full_prompt          # noqa: E402
from import_generated import cutout, eye_span, SCALE_FIX, TARGET_EYE_SPAN  # noqa: E402

ENDPOINT = "https://api.openai.com/v1/images/edits"
# 参照画像の造形をどれだけ保てるかが命なので、編集の精度を売りにしている sunburst を既定にする。
# flare は速くて安い（料金は同じ）が、品質は gpt-image-2 相当。
MODEL = "gpt-image-2.5-sunburst"


def load_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key.strip()
    envfile = os.path.join(REPO, ".env")
    if os.path.exists(envfile):
        for line in io.open(envfile, encoding="utf-8"):
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def draw(key, prompt, size, quality, model):
    with open(REF, "rb") as f:
        files = {"image": ("reference.png", f.read(), "image/png")}
    data = {"model": model, "prompt": prompt, "size": size, "n": "1"}
    # quality の取りうる値はモデルによって変わる。指定されたときだけ送る
    if quality:
        data["quality"] = quality
    r = requests.post(ENDPOINT, headers={"Authorization": f"Bearer {key}"},
                      files=files, data=data, timeout=300)
    if r.status_code != 200:
        msg = r.json().get("error", {}).get("message", r.text[:200]) if r.headers.get(
            "content-type", "").startswith("application/json") else r.text[:200]
        raise RuntimeError(f"HTTP {r.status_code}: {msg}")
    return base64.b64decode(r.json()["data"][0]["b64_json"])


def place(name, raw_bytes):
    """生の絵を、背景抜き・縮尺そろえまでして assets/images に置く"""
    os.makedirs(RAW, exist_ok=True)
    raw_path = os.path.join(RAW, f"{name}.png")
    with open(raw_path, "wb") as f:
        f.write(raw_bytes)

    img = cutout(raw_path)
    box = img.getbbox()
    if not box:
        return None, "中身が無い"
    img = img.crop(box)

    span = eye_span(img)
    if span and span > 8:
        k = TARGET_EYE_SPAN / span * SCALE_FIX.get(f"{name}.png", 1.0)
        img = img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))),
                         Image.LANCZOS)
        img = img.crop(img.getbbox())
        note = f"目の間隔 {span:.0f}px → ×{k:.2f}"
    else:
        note = "目が見つからない。縮尺は未調整。並べて見て SCALE_FIX に足すこと"

    out = os.path.join(OUT, f"{name}.png")
    img.save(out)
    return img, note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*", help="ポーズ名（peek, sleep, wink ...）。省略で全部")
    ap.add_argument("--model", default=MODEL,
                    help=f"既定 {MODEL}。速さ優先なら gpt-image-2.5-flare")
    ap.add_argument("--quality", default=None,
                    help="指定しなければモデルの既定にまかせる。取りうる値はモデルによる")
    ap.add_argument("--size", default="1024x1024")
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("OPENAI_API_KEY が見つからない。")
        print(f"  {os.path.join(REPO, '.env')} に OPENAI_API_KEY=sk-... の1行を置くか、")
        print("  環境変数に入れてから実行する。")
        return 1

    table = {f.replace("character-", ""): (f, t, fr, pl, pose) for f, t, fr, pl, pose in POSES}
    want = args.names or list(table)
    unknown = [n for n in want if n not in table]
    if unknown:
        print("知らないポーズ:", ", ".join(unknown))
        print("使えるのは:", ", ".join(table))
        return 1

    for n in want:
        fname, title, frame, place_, pose = table[n]
        print(f"{title}（{n}）を描かせる…", flush=True)
        try:
            raw = draw(key, full_prompt(frame, pose), args.size, args.quality, args.model)
        except Exception as e:
            print(f"  失敗: {e}")
            continue
        img, note = place(fname, raw)
        if img:
            print(f"  {fname}.png  {img.width}x{img.height}  {note}")

    print("\n並べて確認する:")
    names = " ".join(f"assets/images/{table[n][0]}.png" for n in want if n in table)
    print(f"  magick montage {names} -tile 5x2 -geometry +10+10 "
          f"-background '#f6f2ea' -gravity south /tmp/chars.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
