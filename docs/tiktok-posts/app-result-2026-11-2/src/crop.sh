#!/bin/bash
# 生の画面（assets/raw）から、スライドに使う部分を切り出す（長い辺1400px以下）。
# 書式: 出力名 元ファイル 幅x高さ+x+y
cd "$(dirname "$0")/assets"
while read -r out src geo; do
  [ -z "$out" ] && continue
  magick "raw/$src" -crop "$geo" +repage -resize '1400x1400>' "img/$out"
done <<'LIST'
mk-tear.png mk-01_tear.png 1320x1960+0+800
mk-page.png mk-02_page.png 1260x1540+30+790
mk-stack.png mk-05_stack.png 1020x1070+150+1030
mk-detail.png mk-06_detail.png 1320x1070+0+1020
fb-card.png fb-01_preview.png 860x1160+230+380
fb-postal.png fb-03_postal.png 1245x1260+20+1260
fb-book.png fb-02_book.png 1320x1250+0+540
fb-paper.png fb-04_paper.png 920x1210+200+1270
km-home.png km-01_home.png 1229x880+48+365
km-record.png km-02_record.png 1240x795+40+370
km-tags.png km-02_record.png 1240x730+40+1190
km-today.png km-01_home.png 1260x670+30+1560
mb-flash.png mb-01_flash.png 1320x1030+0+1000
mb-summary.png mb-02_summary.png 1320x960+0+410
mb-listen.png mb-05_listen.png 1240x915+50+600
mb-records.png mb-06_records.png 1250x1250+40+410
fl-result.png fl-02_result.png 1260x1215+30+380
fl-birth.png fl-04_birth.png 1200x1435+60+510
fl-calendar.png fl-05_calendar.png 1320x1620+0+640
fl-collection.png fl-06_collection.png 1260x1690+40+510
bl-result.png bl-02_result.png 1260x990+30+370
bl-camera.png bl-01_camera.png 1320x1750+0+800
bl-info.png bl-02_result.png 1260x540+30+1355
bl-collection.png bl-05_collection.png 1260x1690+40+510
ds-home.png ds-01_home.png 1260x1440+30+380
ds-week.png ds-01_home.png 702x690+575+650
ds-overlay.png ds-02_overlay.png 1170x1700+75+565
ds-add.png ds-01_home.png 1260x860+30+1880
LIST
