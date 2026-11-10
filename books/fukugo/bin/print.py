"""見本章の紙面（A5）を、『自治体の公民連携ハンドブック』の紙面にそろえて PDF に組む。

使い方: python3 bin/print.py   （books/fukugo で実行。出力は print/mihon.pdf）
Chromium（playwright）で組む。明朝は Noto Serif CJK JP、表と柱はゴシック。
"""
import re
import subprocess
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "manuscript"
OUT = ROOT / "print"
FIG = ROOT / "fig"

BOOK = "公共施設の複合化"
SUB = "——「減らす」から「組み替える」へ"
SUB2 = "商業・文化・福祉・交通を「広場」でつなぐ——自治体とデベロッパーの実務"
AUTHOR = "上村　章文"

# 見本として組む章：(原稿, 部)
CHAPTERS = [
    ("00_josho", "序章"),
    ("01_hiroba", "第1部　考え方"),
    ("02_ruikei", "第1部　考え方"),
    ("03_saikaihatsu", "第1部　考え方"),
    ("04_gakko", "第2部　組み合わせ別"),
    ("05_shogyo", "第2部　組み合わせ別"),
    ("06_bunka", "第2部　組み合わせ別"),
    ("07_kominkan", "第2部　組み合わせ別"),
    ("08_fukushi", "第2部　組み合わせ別"),
    ("09_koen", "第2部　組み合わせ別"),
    ("10_shoku", "第2部　組み合わせ別"),
    ("11_kotsu", "第2部　組み合わせ別"),
    ("12_kangen", "第3部　仕組み"),
    ("13_okane", "第3部　仕組み"),
    ("14_unei", "第3部　仕組み"),
    ("15_goui", "第3部　仕組み"),
    ("16_teigen", "第4部　行動"),
    ("17_kokyo-tenant", "第5部　デベロッパーの実務"),
    ("18_jikanjiku", "第5部　デベロッパーの実務"),
    ("19_teian", "第5部　デベロッパーの実務"),
]

CSS = r"""
@page { size: 148mm 210mm; margin: 17mm 16mm 18mm 16mm; }
@page :left  { margin-left: 17mm; margin-right: 15mm; }
@page :right { margin-left: 15mm; margin-right: 17mm; }
@page plain { @bottom-left { content: none } @bottom-right { content: none } }
%PAGES%
@counter-style circled { system: fixed; symbols: "❶" "❷" "❸" "❹" "❺" "❻" "❼"; suffix: " "; }
html { font-family: "Noto Serif CJK JP", "IPAMincho", serif; font-size: 8.7pt; line-height: 1.78;
  color: #000; text-align: justify; font-kerning: none; }
body { margin: 0; }
.sans, table, .point .label, h2, h3, .fig, .partpage, .title, .kakomi-label {
  font-family: "Noto Sans CJK JP", "IPAGothic", sans-serif; }
p { margin: 0; text-indent: 1em; }
p + p { margin-top: 0; }
strong { font-weight: 700; font-family: "Noto Sans CJK JP", sans-serif; font-size: .97em; }
.title { page: plain; height: 170mm; display: flex; flex-direction: column; justify-content: center; }
.title h1 { font-size: 20pt; line-height: 1.5; margin: 0 0 4mm; font-weight: 700; }
.title .sub { font-size: 11pt; margin: 0 0 2mm; }
.title .sub2 { font-size: 8.5pt; margin: 0 0 16mm; }
.title .au { font-size: 11pt; }
.title .note { margin-top: 26mm; font-size: 7.5pt; line-height: 1.7; border-top: .3mm solid #000; padding-top: 3mm; }
.partpage { page: plain; break-before: page; height: 170mm; display: flex; align-items: center; justify-content: center;
  font-size: 15pt; font-weight: 700; letter-spacing: .05em; }
.ch { break-before: page; }
.toc { page: plain; break-before: page; font-family: "Noto Sans CJK JP", sans-serif; }
.toc h1 { font-size: 13pt; margin: 4mm 0 5mm; padding-bottom: 2mm; border-bottom: .6mm solid #000; }
.toc .part { font-size: 8.5pt; font-weight: 700; margin: 3.2mm 0 .8mm; letter-spacing: .05em; }
.toc .row { display: flex; align-items: baseline; font-size: 7.4pt; line-height: 1.55; break-inside: avoid; }
.toc .row .t { flex: 0 1 auto; }
.toc .row .dots { flex: 1 1 auto; border-bottom: .2mm dotted #000; margin: 0 1.2mm; transform: translateY(-.8mm); min-width: 4mm; }
.toc .row .p { flex: 0 0 auto; min-width: 6mm; text-align: right; }
.toc .l1 { font-size: 8.3pt; font-weight: 700; margin-top: 1.6mm; }
.toc .l2 { padding-left: 4mm; }
.toc .l3 { padding-left: 8mm; font-size: 7pt; color: #222; }
.toc .l3 .t { padding-left: 7.5mm; text-indent: -7.5mm; }
.toc .l3 .t::before { content: "事例　"; font-size: 6.2pt; border: .2mm solid #000; padding: 0 .6mm; margin-right: 1mm; }
.ch h1 { font-family: "Noto Sans CJK JP", sans-serif; font-size: 15pt; line-height: 1.45; font-weight: 700;
  margin: 6mm 0 6mm; padding-bottom: 2.5mm; border-bottom: .6mm solid #000; }
.ch h1 .no { display: block; font-size: 9pt; font-weight: 700; letter-spacing: .1em; margin-bottom: 1mm; }
.point { border: .35mm solid #000; padding: 2.5mm 3.5mm 2.8mm; margin: 0 0 6mm; break-inside: avoid; }
.point .label { display: inline-block; background: #000; color: #fff; font-weight: 700; font-size: 8pt;
  padding: .3mm 2.5mm; margin: 0 0 1.8mm; letter-spacing: .1em; }
.point ol { list-style: none; counter-reset: pt; margin: 0; padding-left: 1.45em; }
.point li { margin: 0; line-height: 1.7; }
.point li { counter-increment: pt; position: relative; }
.point li::before { content: counter(pt, circled); position: absolute; left: -1.45em; font-family: "Noto Serif CJK JP", serif; font-weight: 400; }
.point li strong { font-family: inherit; font-size: 1em; }
h2 { font-size: 10pt; font-weight: 700; line-height: 1.5; margin: 6mm 0 2.5mm; padding: .6mm 0 .6mm 2.4mm;
  border-left: 1.3mm solid #000; break-after: avoid; }
h3 { font-size: 9pt; font-weight: 700; margin: 4mm 0 1.2mm; break-after: avoid; }
ul, ol { margin: 1.5mm 0; padding-left: 1.3em; }
li { margin: .6mm 0; }
li p { text-indent: 0; }
blockquote { margin: 3mm 0; padding: 2.2mm 3.2mm; border: .3mm solid #000; background: #ececec; break-inside: avoid; }
blockquote p { text-indent: 0; }
table { width: 100%; border-collapse: collapse; font-size: 7.2pt; line-height: 1.5; margin: 3mm 0 3.5mm;
  break-inside: avoid; text-align: left; }
th, td { border: .2mm solid #000; padding: .9mm 1.3mm; vertical-align: top; }
th { background: #dcdcdc; font-weight: 700; }
td strong { font-size: 1em; }
.fig { margin: 4mm 0; break-inside: avoid; }
.fig .cap { display: inline-block; background: #000; color: #fff; font-size: 7.5pt; font-weight: 700; padding: .4mm 2.4mm; }
.fig .art { margin-top: 1.5mm; }
.fig .art svg { display: block; width: 100%; height: auto; }
.fig .ph { border: .3mm dashed #000; height: 46mm; display: flex; align-items: center; justify-content: center;
  font-size: 7.5pt; color: #444; margin-top: 1.2mm; }
"""

PAGE_RULE = """@page {name}:left  {{ @bottom-left  {{ content: counter(page) "　{part}"; font: 7pt "Noto Sans CJK JP", sans-serif; }} }}
@page {name}:right {{ @bottom-right {{ content: "{chap}　" counter(page); font: 7pt "Noto Sans CJK JP", sans-serif; }} }}
@page {name}:first {{ @bottom-left {{ content: none }} @bottom-right {{ content: none }} }}"""


CASE = re.compile(r"（.*(\d{4}|県|都|府|イギリス|フィンランド|ポルトガル)|「|^\S+[市町村区]\s|^反面の例|^[①②③④]\s|^人材育成")
SKIP2 = ("この章の要点", "この章で覚えておくこと", "規模別の現実解", "から見ると")


# 目次で同じ事例が重ならないようにする。詳しく書いた章だけを目次に出す
TOC_SKIP = {("02", "いーよの"), ("02", "秦野"), ("02", "オガール"), ("17", "アウガ")}
TOC_LABEL = {("17", "オガール"): "紫波町 オガールプラザ（民間の側から見た組み方）"}


def case_name(t):
    """目次では事例の名前だけを出す（副題を落とす）。"""
    if "——" not in t:
        return t
    a, b = t.split("——", 1)
    if re.match(r"^([A-D＋]+\s|[①②③④]\s|反面の例$|人材育成)", a.strip() + (" " if len(a.strip()) <= 3 else "")) or "×" in a:
        return b
    return a


def toc_entries(md_text, ch=""):
    """目次に載せる見出し：(段, 文字列, 照合用の文字列)。章・節・事例。"""
    out = []
    for line in md_text.splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            out.append((1, t, t.split("　", 1)[1]))
        elif line.startswith("## "):
            t = line[3:].strip()
            if not any(k in t for k in SKIP2):
                out.append((2, t, t))
        elif line.startswith("### "):
            t = line[4:].strip()
            if CASE.search(t) and not any(c == ch and k in t for c, k in TOC_SKIP):
                label = next((v for (c, k), v in TOC_LABEL.items() if c == ch and k in t), case_name(t))
                out.append((3, label, t))
    return out


def norm(x):
    return re.sub(r"[\s*_`]", "", x)


def toc_html(groups, pages=None):
    rows = ['<div class="toc"><h1>目次</h1>']
    k = 0
    for part, entries in groups:
        if part:
            rows.append(f'<div class="part">{part}</div>')
        for lv, t, _ in entries:
            p = pages[k] if pages else "000"
            k += 1
            rows.append(f'<div class="row l{lv}"><span class="t">{t}</span><span class="dots"></span><span class="p">{p}</span></div>')
    rows.append("</div>")
    return "".join(rows)


def find_pages(pdf, groups, start):
    """組んだPDFから各見出しのページを探す（前から順に）。"""
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
    txt = [norm(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True).stdout)
           for i in range(1, n + 1)]
    pages, cur = [], start
    for _, entries in groups:
        for lv, _, key in entries:
            key = norm(key)[:14]
            i = cur
            while i < n and key not in txt[i]:
                i += 1
            if i >= n:
                pages.append("?")
            else:
                pages.append(str(i + 1))
                cur = i
    return pages


def chapter_html(md_text, name):
    html = markdown.markdown(md_text, extensions=["tables"])
    html = re.sub(r"<hr\s*/?>", "", html)
    m = re.match(r"<h1>(序章|第\d+章)　(.*?)</h1>", html)
    no, title = m.group(1), m.group(2)
    html = html[m.end():]
    html = re.sub(r"<h2>この章の要点</h2>\s*(<ol>.*?</ol>)",
                  r'<div class="point"><div class="label">ポイント</div>\1</div>', html, count=1, flags=re.S)
    def fig(m):
        svg = next(FIG.glob(f"fig{m.group(1)[1:]}_*.svg"), None)
        inner = svg.read_text(encoding="utf-8") if svg else '<div class="ph">作図中</div>'
        return f'<div class="fig"><span class="cap">{m.group(1)}　{m.group(2)}</span><div class="art">{inner}</div></div>'
    html = re.sub(r"<p>〔(図[^　〕]*)　([^〕]*)〕</p>", fig, html)
    # 表のセル・見出し・要点の段落は字下げしない
    return (f'<section class="ch" style="page:{name}"><h1><span class="no">{no}</span>{title}</h1>{html}</section>',
            f"{no}　{title}")


def main():
    OUT.mkdir(exist_ok=True)
    pages, body = [], []
    body.append(f'<div class="title"><h1>{BOOK}</h1><p class="sub">{SUB}</p><p class="sub2">{SUB2}</p>'
                f'<p class="au">{AUTHOR}</p><div class="note">見本紙面（目次・序章・第1章〜第19章）<br>'
                'A5判。本文は明朝、見出し・表・柱はゴシック。ページ番号は見本用の通し番号です。'
                '</div></div>')
    toc_at = len(body)
    body.append("")  # 目次はあとで差し込む
    groups = []
    last_part = None
    for i, (src, part) in enumerate(CHAPTERS):
        md_text = (SRC / f"{src}.md").read_text(encoding="utf-8")
        groups.append((part if part != last_part and part != "序章" else "", toc_entries(md_text, src[:2])))
        name = f"c{i}"
        html, chap = chapter_html(md_text, name)
        pages.append(PAGE_RULE.format(name=name, part=part, chap=chap))
        if part != last_part and part != "序章":
            body.append(f'<div class="partpage">{part.replace("　", "　")}</div>')
            last_part = part
        body.append(html)
    css = CSS.replace("%PAGES%", "\n".join(pages))
    src = OUT / "mihon.html"
    pdf = OUT / "mihon.pdf"

    def render():
        doc = f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(body)}</body></html>'
        src.write_text(doc, encoding="utf-8")
        js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{src}'); await p.evaluate(() => document.fonts.ready);
  await p.pdf({{ path: '{pdf}', preferCSSPageSize: true, printBackground: true }});
  await b.close(); }})();"""
        subprocess.run(["node", "-e", js], check=True)

    body[toc_at] = toc_html(groups)
    render()
    # 本文の始まり（序章の扉）を探してから、見出しのページを拾う
    n_toc_end = 1
    out = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout.split("\f")
    for i, t in enumerate(out):
        if "序章" in t and "なぜ" in t and "目次" not in t:
            n_toc_end = i
            break
    found = find_pages(pdf, groups, n_toc_end)
    body[toc_at] = toc_html(groups, found)
    render()
    miss = sum(1 for p in found if p == "?")
    print("toc entries:", len(found), "not found:", miss)
    print("built:", pdf)


if __name__ == "__main__":
    main()
