"""iPhone の画面を端末の枠にまるごとはめる（中身は skill tiktok-slideshow の phone_mockup.py）。

  python3 src/make_mockups.py

- いまの画面: 6.3.0 のストア用の撮影（iPhone Air 1260x2736。枠と同じ比率）
- 前の画面: 5.0.0 のストア用スクショの中に描かれた端末から、画面の内側だけを取り出す（OLD_SCREEN_BOX はふちの黒から測った）
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
IMG = HERE / "assets/img"
TOOL = Path.home() / ".claude/skills/tiktok-slideshow/scripts/phone_mockup.py"
OLD = IMG / "old-store"   # ASC の 5.0.0 の APP_IPHONE_67（ja）。一時フォルダに置くと消える
OLD_SCREEN_BOX = "156,507,1162,2701"

args = [f"new-{n}={IMG}/new-{n}.png" for n in (1, 3, 6)]
args += [f"old-{n}={OLD}/5.0.0-APP_IPHONE_67-{n:02d}.png[{OLD_SCREEN_BOX}]" for n in (1, 3, 4)]
subprocess.run([sys.executable, str(TOOL), str(IMG), *args], check=True)
