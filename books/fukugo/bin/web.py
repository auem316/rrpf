"""見本章の Web 版を『自治体の公民連携ハンドブック』と同じ紙面で組む。

使い方: python3 bin/web.py   （books/fukugo で実行。出力は web/）
"""
import re
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "manuscript"
OUT = ROOT / "web"
BOOK = "公共施設の複合化"
SUB = "——「減らす」から「組み替える」へ"
AUTHOR = "上村　章文"
UPDATED = "2026年10月30日"
BASEDATE = "2026年10月30日"

# (ファイル, 部) 見本として組む章
CHAPTERS = [
    ("00_josho", "00-josho.html"),
    ("01_hiroba", "01-hiroba.html"),
    ("02_ruikei", "02-ruikei.html"),
    ("03_saikaihatsu", "03-saikaihatsu.html"),
    ("04_gakko", "04-gakko.html"),
    ("05_shogyo", "05-shogyo.html"),
    ("06_bunka", "06-bunka.html"),
    ("07_kominkan", "07-kominkan.html"),
    ("08_fukushi", "08-fukushi.html"),
    ("09_koen", "09-koen.html"),
    ("10_shoku", "10-shoku.html"),
    ("11_kotsu", "11-kotsu.html"),
    ("12_kangen", "12-kangen.html"),
    ("13_okane", "13-okane.html"),
    ("17_kokyo-tenant", "17-kokyo-tenant.html"),
]
PAGE_OF = {int(src[:2]): html for src, html in CHAPTERS}

TOC = [
    (None, ["序章　なぜ「減らす」から「組み替える」へなのか"]),
    ("第1部　考え方", [
        "第1章　外部経済効果を「広場」でつなぐ",
        "第2章　何と何を組み合わせるか（4つの類型）",
        "第3章　地方の再開発はなぜ失敗したか"]),
    ("第2部　組み合わせ別", [
        "第4章　公共×公共——学校を核にする",
        "第5章　公共×商業——床を借りるか、持つか",
        "第6章　文化×商業——入口に商業、奥に文化",
        "第7章　公民館×カフェ・居酒屋",
        "第8章　福祉×商業・文化——幼老複合をまちの居場所に",
        "第9章　公園×収益施設——Park-PFIの先へ",
        "第10章　食を核にする",
        "第11章　地域公共交通×複合施設"]),
    ("第3部　仕組み", [
        "第12章　商業の稼ぎで公共を支える（収益還元）",
        "第13章　お金をどう用意するか",
        "第14章　誰がどう運営するか",
        "第15章　試してから決める（合意形成）"]),
    ("第4部　行動", ["第16章　18の提言とロードマップ"]),
    ("第5部　デベロッパーの実務", [
        "第17章　公共テナントは商業施設に何をもたらすか",
        "第18章　自治体の決め方と時間軸を読む",
        "第19章　通る提案の組み立て"]),
]

CSS = (ROOT / "bin" / "style.css").read_text(encoding="utf-8")


def slug(value, sep):
    return re.sub(r"\s+", "", value)


def page(title, desc, body):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}｜{BOOK}</title>
<meta name="description" content="{desc}">
<style>
{CSS}
</style>
</head>
<body>
<header class="site"><div class="wrap">
<a class="home" href="index.html">{BOOK}</a>
<nav><a href="index.html">目次</a><a href="konkyo.html">根拠資料</a><a href="checklist-web.html">チェックリスト</a><a href="../index.html" class="portal">ポータルへ</a></nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer class="site"><div class="wrap">
{AUTHOR}　｜　最終更新 {UPDATED}　｜　本書の情報の基準日は{BASEDATE}です
</div></footer>

</body>
</html>
"""


def render(md_text):
    html = markdown.markdown(md_text, extensions=["tables", "toc"],
                             extension_configs={"toc": {"slugify": slug}})
    html = re.sub(r"<table>(.*?)</table>", r'<div class="tw"><table>\1</table></div>', html, flags=re.S)
    def fig(m):
        cap = m.group(1)
        svg = next((ROOT / "fig").glob(f"fig{cap.split('　')[0][1:]}_*.svg"), None)
        if not svg:
            return f'<div class="fig-ph">{cap}（作図中）</div>'
        return f'<figure><img src="fig/{svg.name}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
    html = re.sub(r"<p>〔(図[^〕]*)〕</p>", fig, html)

    def link(m):
        n = int(m.group(1))
        return f'<a href="{PAGE_OF[n]}">第{n}章</a>' if n in PAGE_OF else m.group(0)
    # 本文中の「（第N章）」「（第N章、第M章）」だけをリンクにする（h1 は除く）
    head, rest = html.split("</h1>", 1)
    rest = re.sub(r"（[^（）]*第\d+章[^（）]*）",
                  lambda m: re.sub(r"第(\d+)章", link, m.group(0)), rest)
    return head + "</h1>" + rest


def desc_of(md_text):
    t = re.sub(r"[#*>|\-]", "", md_text)
    return re.sub(r"\s+", " ", t).strip()[:120]


def main():
    OUT.mkdir(exist_ok=True)
    titles = []
    for src, _ in CHAPTERS:
        titles.append((SRC / f"{src}.md").read_text(encoding="utf-8").splitlines()[0][2:])
    for i, (src, dst) in enumerate(CHAPTERS):
        md_text = (SRC / f"{src}.md").read_text(encoding="utf-8")
        n = int(src[:2])
        body = render(md_text)
        anc = "序章" if n == 0 else f"第{n}章"
        body += ('\n<hr>\n<blockquote><p><strong>この章は見本原稿です。</strong>'
                 f'Web版には、この章の<a href="konkyo.html#{anc}">根拠資料</a>と'
                 f'<a href="checklist-web.html#{anc}">チェックリスト</a>を置いている。</p></blockquote>\n')
        prev = f'<a href="{CHAPTERS[i-1][1]}">← {titles[i-1]}</a>' if i else "<span></span>"
        nxt = f'<a href="{CHAPTERS[i+1][1]}">{titles[i+1]} →</a>' if i + 1 < len(CHAPTERS) else "<span></span>"
        body += f'<div class="pager">{prev}{nxt}</div>'
        (OUT / dst).write_text(page(titles[i], desc_of(md_text), body), encoding="utf-8")

    for src, dst in [("konkyo", "konkyo.html"), ("checklist", "checklist-web.html")]:
        md_text = (SRC / f"{src}.md").read_text(encoding="utf-8")
        body = render(md_text)
        # 章見出しに「第N章」のアンカーを付ける
        body = re.sub(r'<h2 id="(第(\d+)章[^"]*)">第\d+章',
                      lambda m: f'<span id="第{m.group(2)}章"></span><h2 id="{m.group(1)}">'
                                + (f'<a href="{PAGE_OF[int(m.group(2))]}">第{m.group(2)}章</a>'
                                   if int(m.group(2)) in PAGE_OF else f"第{m.group(2)}章"), body)
        body = re.sub(r'<h2 id="(序章[^"]*)">序章', r'<span id="序章"></span><h2 id="\1"><a href="00-josho.html">序章</a>', body)
        (OUT / dst).write_text(page(md_text.splitlines()[0][2:], desc_of(md_text), body), encoding="utf-8")

    rows = [f'<h1>{BOOK}<br><span class="lead">{SUB}</span></h1>',
            '<p class="lead">商業・文化・福祉・交通を「広場」でつなぐ——自治体とデベロッパーの実務</p>',
            f'<p class="lead">{AUTHOR}</p>',
            '<div class="kami"><p><strong>この本には、紙の版とWebの版があります。</strong></p>'
            '<p>紙は、読んで決め、点検表として書き込むためのもの。Webは、必要なところをその場で引くためのものです。'
            '<strong>本文は同じですが、Web版には章ごとの根拠資料とチェックリストを足しています。</strong></p>'
            '<p class="lead">いま読めるのは、序章・第1章〜第3章・第17章です。ほかの章は準備中です。</p></div>']
    for part, chs in TOC:
        if part:
            rows.append(f'<div class="part">{part}</div>')
        for ch in chs:
            m = re.match(r"第(\d+)章", ch)
            n = 0 if ch.startswith("序章") else (int(m.group(1)) if m else None)
            if n in PAGE_OF:
                rows.append(f'<p><a href="{PAGE_OF[n]}">{ch}</a></p>')
            else:
                rows.append(f'<p class="soon">{ch}（準備中）</p>')
    rows += ['<h2>巻末資料</h2>',
             '<p><a href="konkyo.html">根拠資料——章別</a></p>',
             '<p><a href="checklist-web.html">章別チェックリスト</a></p>']
    (OUT / "index.html").write_text(page("目次", f"{BOOK}{SUB}　目次と見本章", "\n".join(rows)),
                                    encoding="utf-8")
    (OUT / "fig").mkdir(exist_ok=True)
    for svg in (ROOT / "fig").glob("*.svg"):
        (OUT / "fig" / svg.name).write_text(svg.read_text(encoding="utf-8"), encoding="utf-8")
    print("built:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
