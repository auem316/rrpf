"""原稿の点検。本は完全版の1つだけ（manuscript/）。

使い方: python3 bin/check.py   （books/fukugo で実行）

見るもの:
  1. 図の行（〔図N-M　…〕）に対応する SVG が fig/ にあるか
  2. 残っている【要確認】の数
  3. 章をまたぐ重複——同じ22字の並びが2つ以上の章に出てくる箇所
     （通読を前提に、詳しく書くのは1か所にし、ほかの章からは節番号で指す）
重複は「人の目で確かめる候補」として出す。図が欠けていれば終了コード1。
"""
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "manuscript"
FIG = ROOT / "fig"
K = 22          # 重複とみなす字数
TEMPLATE = ("規模別の現実解", "理想次善最低限", "自治体に何を確かめるか")  # 全章共通の型の文言は除く

files = sorted(SRC.glob("[0-9][0-9]_*.md"))
bad = 0

print("1. 図")
for f in files:
    for cap in re.findall(r"〔図(\d+-\d+)　[^〕]*〕", f.read_text(encoding="utf-8")):
        if not list(FIG.glob(f"fig{cap}_*.svg")):
            print(f"  {f.name}: 図{cap} の SVG がない")
            bad += 1
print("  欠けなし" if not bad else f"  欠け {bad} 件")

print("2. 【要確認】")
for f in files:
    n = f.read_text(encoding="utf-8").count("【要確認】")
    if n:
        print(f"  {f.name}: {n}")

print("3. 章をまたぐ重複（候補）")
shingles = collections.defaultdict(set)
for f in files:
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"[*#>|`\-\s]", "", t)
    for i in range(0, len(t) - K, 3):
        s = t[i:i + K]
        if not any(w in s for w in TEMPLATE):
            shingles[s].add(f.name[:2])
pairs = collections.defaultdict(list)
for s, chs in shingles.items():
    if len(chs) > 1:
        pairs[tuple(sorted(chs))].append(s)
if not pairs:
    print("  なし")
for chs, ss in sorted(pairs.items(), key=lambda x: -len(x[1])):
    if len(ss) >= 2:
        print(f"  第{'・'.join(str(int(c)) for c in chs)}章：{len(ss)}か所　例「{ss[0]}」")

total = sum(len(re.sub(r"\s", "", f.read_text(encoding="utf-8"))) for f in files)
print(f"字数（空白を除く）: {total:,}")
sys.exit(1 if bad else 0)
