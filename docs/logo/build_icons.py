#!/usr/bin/env python3
"""Ki のシンボル（assets/images/logo/tsuzukit-symbol*.svg）からファビコン一式を作る。

    python3 docs/logo/build_icons.py

  favicon.ico                         16 / 32 / 48 を内包。墨のシンボル、背景は透明
  assets/icons/favicon-16x16.png      墨・透明
  assets/icons/favicon-32x32.png      墨・透明
  assets/icons/favicon-dark-16x16.png 白・透明（ブラウザが暗い表示のとき）
  assets/icons/favicon-dark-32x32.png 白・透明
  assets/icons/apple-touch-icon.png   180px。クリームの地に墨（iOS は透明を黒く塗るので地を敷く）
  assets/images/logo/tsuzukit-symbol-512.png / tsuzukit-wordmark-1200.png  SVG が使えない所（OGP の生成など）用
"""
import io
import os
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LOGO = os.path.join(REPO, "assets", "images", "logo")
ICONS = os.path.join(REPO, "assets", "icons")
CREAM = (246, 242, 234, 255)


def render(svg, height):
    """SVG を指定の高さの透明 PNG に描く（大きく描いてから縮める）。"""
    png = subprocess.run(["magick", "-background", "none", "-density", "400", svg, "png:-"],
                         check=True, capture_output=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


def fit_square(svg, size, pad):
    inner = size - 2 * pad
    big = render(svg, 1200)
    r = min(inner / big.width, inner / big.height)
    s = big.resize((max(1, round(big.width * r)), max(1, round(big.height * r))), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(s, ((size - s.width) // 2, (size - s.height) // 2), s)
    return canvas


def main():
    ink = os.path.join(LOGO, "tsuzukit-symbol.svg")
    white = os.path.join(LOGO, "tsuzukit-symbol-white.svg")
    for size in (16, 32):
        fit_square(ink, size, 0).save(os.path.join(ICONS, f"favicon-{size}x{size}.png"))
        fit_square(white, size, 0).save(os.path.join(ICONS, f"favicon-dark-{size}x{size}.png"))
    sizes = [fit_square(ink, s, 0) for s in (16, 32, 48)]
    sizes[2].save(os.path.join(REPO, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=sizes[:2])
    touch = Image.new("RGBA", (180, 180), CREAM)
    sym = fit_square(ink, 180, 30)
    touch.paste(sym, (0, 0), sym)
    touch.convert("RGB").save(os.path.join(ICONS, "apple-touch-icon.png"))
    fit_square(ink, 512, 0).save(os.path.join(LOGO, "tsuzukit-symbol-512.png"))
    render(os.path.join(LOGO, "tsuzukit-wordmark.svg"), 372).save(os.path.join(LOGO, "tsuzukit-wordmark-1200.png"))
    print("ok")


if __name__ == "__main__":
    main()
