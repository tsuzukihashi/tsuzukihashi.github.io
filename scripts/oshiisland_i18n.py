"""推しアイランドのページ（oshiisland/）の多言語ファイルを点検する。

日本語の文言は oshiisland/*.html に直接書いてある（data-i18n="キー" の要素の中身）。
このスクリプトは:
  1. HTML から日本語を読み出して oshiisland/i18n/ja.json を作り直す
  2. 他の言語の i18n/<言語>.json に、HTML のキーが全部あるか・余分なキーが無いかを調べる

使い方:  python3 scripts/oshiisland_i18n.py
文言を足したり変えたりしたら、ja.json と en.json と全言語の json を同じキーで直してから、これを流す。
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "oshiisland"
PAGES = ["index", "faq", "privacy", "terms", "disclaimer"]
VOID = {"br", "img", "meta", "link", "input", "hr", "source", "wbr"}


class Collect(HTMLParser):
    """data-i18n を持つ要素の中身（HTML のまま）と、属性で差し替えるものを集める"""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = {}
        self.stack = []  # [tag, key, buffer]

    def _emit(self, text):
        for item in self.stack:
            item[2].append(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for attr, target in (("data-i18n-content", "content"), ("data-i18n-alt", "alt")):
            if attr in a:
                self.out[a[attr]] = a.get(target, "")
        raw = self.get_starttag_text()
        self._emit(raw)
        if tag in VOID:
            return
        self.stack.append([tag, a.get("data-i18n"), []])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, key, buf = self.stack.pop()
            if key is not None:
                self.out[key] = "".join(buf).strip()
            if t == tag:
                break
        self._emit(f"</{tag}>")

    def handle_data(self, data):
        self._emit(data)

    def handle_entityref(self, name):
        self._emit(f"&{name};")

    def handle_charref(self, name):
        self._emit(f"&#{name};")


def main():
    ja = {}
    for p in PAGES:
        c = Collect()
        c.feed((DIR / f"{p}.html").read_text())
        ja.update(c.out)
    (DIR / "i18n" / "ja.json").write_text(json.dumps(ja, ensure_ascii=False, indent=1) + "\n")
    ok = True
    for f in sorted((DIR / "i18n").glob("*.json")):
        if f.stem == "ja":
            continue
        d = json.loads(f.read_text())
        missing = sorted(set(ja) - set(d))
        extra = sorted(set(d) - set(ja))
        empty = [k for k, v in d.items() if not str(v).strip()]
        if missing or extra or empty:
            ok = False
            print(f"{f.stem}: 足りない {missing[:5]} 余分 {extra[:5]} 空 {empty[:5]}")
    langs = len(list((DIR / "i18n").glob("*.json")))
    print(f"キー {len(ja)} / 言語 {langs}: {'OK' if ok else 'NG'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
