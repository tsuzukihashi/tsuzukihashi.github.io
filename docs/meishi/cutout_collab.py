#!/usr/bin/env python3
"""ChatGPT で作った10場面の白い背景を抜いて docs/meishi/parts/collab/ に置く。

    python3 docs/meishi/cutout_collab.py

背景にするのは、白（RGB の最小値が 244 以上）のうち
- 画像の外枠につながっている塊
- 囲まれていても広い塊（6000px 超。脚立の段のあいだなど）
キャラの白い目（囲まれた小さな白）は残す。
"""
import glob
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = sys.argv[1] if len(sys.argv) > 1 else ".playwright-mcp/meishi/collab/"
DST = "docs/meishi/parts/collab/"
os.makedirs(DST, exist_ok=True)
for f in sorted(glob.glob(os.path.join(SRC, "[0-9][0-9]-*.png"))):
    name = os.path.basename(f)
    im = Image.open(f).convert("RGB")
    a = np.array(im).astype(int)
    white = a.min(axis=2) >= 244
    lab, n = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(n + 1))
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    big = {i for i in range(1, n + 1) if sizes[i] > 6000}
    bg = np.isin(lab, list(edge | big))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    soft = ndimage.binary_dilation(bg, iterations=1) & ~bg
    alpha[soft] = 150
    out = Image.fromarray(np.dstack([np.array(im), alpha]))
    out = out.crop(out.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox())
    out.save(os.path.join(DST, name))
    print(name, out.size, "囲まれた広い白:", len(big - edge))
