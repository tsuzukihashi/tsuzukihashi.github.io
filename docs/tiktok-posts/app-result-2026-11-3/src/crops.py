"""assets/raw の生の画面から、スライドに使う部分を切り出して assets/img に置く（長い辺は1400px以下）。

  /usr/bin/python3 src/crops.py

座標は生の画面の画素 (x0, y0, x1, y1)。どの画面もストア撮影の見本のデータ。
"""
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).parent
RAW = HERE / "assets/raw"
IMG = HERE / "assets/img"

CROPS = {
    # ふくわらい（1206x2622）。duo/ は絵が上下さかさまなので使わない
    "fk-reveal.png": ("fuku-01_reveal.png", (150, 180, 1056, 1110)),     # じゃーん！とおかめの顔（点の札より上）
    "fk-placing.png": ("fuku-02_placing.png", (40, 400, 1166, 1270)),    # つぎは これ「くち」・見えないよ
    "fk-finish.png": ("fuku-04_finish.png", (40, 270, 1095, 1180)),      # みんなの かお・いちばん へんてこ
    "fk-album.png": ("fuku-05_album.png", (50, 380, 1154, 1195)),        # これまでの かお（上の2つ・点と AI の感想）
    # みのうえ（1320x2868）。01_resume・04_photo は AI の顔が写るので使わない
    "mi-years.png": ("minoue-02_years.png", (60, 470, 1260, 1935)),      # 生年月日・いま25歳・入学と卒業の8行
    "mi-career.png": ("minoue-05_career.png", (99, 469, 1220, 1890)),    # 職務経歴書の1枚（見本の氏名はぼかす。BLUR）
    "mi-private.png": ("minoue-07_private.png", (55, 1060, 1267, 1790)), # このアプリは何も送りません（文の所だけ）
    "mi-style.png": ("minoue-07_private.png", (55, 2290, 1267, 2868)),   # 様式・紙の大きさ・年の書き方
    # うんぐりっしゅ（1320x2868）。_framed は使わない
    "un-hero.png": ("ung-0_hero.png", (65, 235, 1251, 1356)),            # よくできました・星3つ
    "un-signs.png": ("ung-4_signs.png", (73, 925, 1246, 1838)),          # かんばん 4行
    "un-pair.png": ("ung-7_pair.png", (65, 417, 1251, 1303)),            # light / right
    "un-titles.png": ("ung-8_titles.png", (104, 391, 1317, 1199)),       # 称号と場面のバッジ
    # パタパタ推し時計（1320x2868）。写真と背景は ChatGPT で作った絵
    "pt-clock.png": ("pata-01_clock.png", (0, 1060, 1320, 1930)),        # 22:05 のカード
    "pt-digits.png": ("pata-02_digits.png", (40, 530, 1270, 1460)),      # 設定済み 60/60・00〜09
    "pt-board.png": ("pata-03_board.png", (125, 1981, 1194, 2738)),      # メッセージとカウントダウン
    "pt-widget.png": ("pata-04_widget.png", (104, 208, 1199, 1408)),     # ウィジェット
    # 空想旅行カメラ（1320x2868）。02_map は Apple マップの画像なので使わない
    "dr-result.png": ("dream-01_result.png", (70, 873, 1246, 1517)),     # 雪のエッフェル塔
    "dr-situation.png": ("dream-03_situation.png", (57, 1108, 1262, 2203)),  # 天候7つ・シチュエーション（地図より下）
    "dr-detail.png": ("dream-05_detail.png", (52, 456, 1316, 1799)),     # 千本鳥居・住所と日付
    "dr-album.png": ("dream-04_album.png", (26, 1108, 1290, 1600)),      # 思い出の2段目（ギリシャ・アイスランド）
    # 赤シート六法（1320x2868）
    "ak-sheet.png": ("aka-01_sheet.png", (39, 430, 1277, 1668)),         # 憲法96条の赤い帯
    "ak-choice.png": ("aka-02_choice.png", (65, 443, 1264, 1290)),       # 4択（民法94条）
    "ak-input.png": ("aka-03_input.png", (65, 1225, 1264, 1799)),        # 書いて答える・三分の二・正解
    "ak-markers.png": ("aka-07_markers.png", (39, 391, 1316, 1382)),     # 自分のマーカー
    # 旅行思い出マップ（1320x2868・一覧は 1398x2034）。日本地図は使わない
    "om-europe.png": ("omo-01_europe.png", (0, 400, 1320, 2380)),        # ヨーロッパ 18/29カ国
    "om-west.png": ("omo-01_europe.png", (150, 1470, 800, 2290)),        # フランス・スペインのあたり
    "om-us.png": ("omo-01_usmap.png", (0, 1130, 1320, 2130)),            # アメリカ
    "om-list.png": ("omo-02_list29.png", (20, 90, 1120, 1610)),          # 写真一覧の国の形
}


# 切り出す前にぼかす所（生の画面の座標）。みのうえの職務経歴書の日付と見本の氏名の行
BLUR = {"minoue-05_career.png": (860, 600, 1120, 680)}


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    for out, (src, box) in CROPS.items():
        im = Image.open(RAW / src).convert("RGB")
        if src in BLUR:
            b = BLUR[src]
            im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
        im = im.crop(box)
        if max(im.size) > 1400:
            r = 1400 / max(im.size)
            im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        im.save(IMG / out)
        print(out, im.size)


if __name__ == "__main__":
    main()
