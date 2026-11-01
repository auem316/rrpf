"""紙版の原稿（print/NN_名前.md）を Web版（manuscript/NN_名前.md）と突き合わせて点検する。

使い方: python3 bin/check.py   （books/fukugo で実行）
見るもの：章題・節題（## 行）と順番が同じか／図の行が同じか／
紙版に Web版にない数値が出ていないか／残った【要確認】／分量（Web版に対する割合）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB, PAPER = ROOT / "manuscript", ROOT / "print"
NUM = re.compile(r"\d[\d,，.．]*")


def chars(s):
    return len(re.sub(r"\s|[#>|*\-]", "", s))


def heads(s):
    return [l.strip() for l in s.splitlines() if re.match(r"#{1,2} ", l)]


def figs(s):
    return re.findall(r"〔図[^〕]*〕", s)


def main():
    bad, tw, tp = 0, 0, 0
    for p in sorted(PAPER.glob("[0-9][0-9]_*.md")):
        w = WEB / p.name
        ps, ws = p.read_text(encoding="utf-8"), w.read_text(encoding="utf-8")
        msgs = []
        if heads(ps) != heads(ws):
            msgs.append(f"節題が違う: {sorted(set(heads(ws)) ^ set(heads(ps)))}")
        if figs(ps) != figs(ws):
            msgs.append(f"図の行が違う: {sorted(set(figs(ws)) ^ set(figs(ps)))}")
        wnums = set(NUM.findall(ws))
        extra = sorted(set(n for n in NUM.findall(ps) if n not in wnums))
        if extra:
            msgs.append(f"Web版にない数値: {extra}")
        k = ps.count("【要確認】")
        if k:
            msgs.append(f"【要確認】が{k}か所")
        a, b = chars(ws), chars(ps)
        tw, tp = tw + a, tp + b
        print(f"{p.name:24} {b:6} / {a:6}  {b / a:5.0%}  " + ("OK" if not msgs else "; ".join(msgs)))
        bad += any(not m.startswith("【要確認】") for m in msgs)
    print(f"{'合計':22} {tp:6} / {tw:6}  {tp / tw:5.0%}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
