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
    ("17_kokyo-tenant", "第5部　デベロッパーの実務"),
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
                f'<p class="au">{AUTHOR}</p><div class="note">見本紙面（序章・第1章〜第13章・第17章）<br>'
                'A5判。本文は明朝、見出し・表・柱はゴシック。ページ番号は見本用の通し番号です。'
                '</div></div>')
    last_part = None
    for i, (src, part) in enumerate(CHAPTERS):
        md_text = (SRC / f"{src}.md").read_text(encoding="utf-8")
        name = f"c{i}"
        html, chap = chapter_html(md_text, name)
        pages.append(PAGE_RULE.format(name=name, part=part, chap=chap))
        if part != last_part and part != "序章":
            body.append(f'<div class="partpage">{part.replace("　", "　")}</div>')
            last_part = part
        body.append(html)
    css = CSS.replace("%PAGES%", "\n".join(pages))
    doc = f'<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(body)}</body></html>'
    src = OUT / "mihon.html"
    src.write_text(doc, encoding="utf-8")
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{src}'); await p.evaluate(() => document.fonts.ready);
  await p.pdf({{ path: '{OUT / "mihon.pdf"}', preferCSSPageSize: true, printBackground: true }});
  await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True)
    print("built:", OUT / "mihon.pdf")


if __name__ == "__main__":
    main()
