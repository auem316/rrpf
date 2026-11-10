"""本の紹介ページ（Web）を組む。

本文はWebに出さない。最も詳しい内容は本に載せ、Webは本の紹介と本への入口にする
（2026年11月10日の方針。学芸出版社の指摘による）。
載せるもの：書名と著者、この本でできること、目次（節と事例名）、各章の要点、更新情報。

使い方: python3 bin/web.py   （books/fukugo で実行。出力は web/index.html）
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
UPDATED = "2026年11月10日"
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
    ("14_unei", "14-unei.html"),
    ("15_goui", "15-goui.html"),
    ("16_teigen", "16-teigen.html"),
    ("17_kokyo-tenant", "17-kokyo-tenant.html"),
    ("18_jikanjiku", "18-jikanjiku.html"),
    ("19_teian", "19-teian.html"),
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
<nav><a href="#toc">目次</a><a href="#updates">更新情報</a><a href="../index.html" class="portal">ポータルへ</a></nav>
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


def points_of(md_text):
    """「この章の要点」の箇条をそのまま取り出す。"""
    m = re.search(r"## この章の要点\n\n(.*?)\n\n---", md_text, re.S)
    return markdown.markdown(m.group(1)) if m else ""


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("printmod", ROOT / "bin" / "print.py")
    pm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pm)

    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    rows = [f'<h1>{BOOK}<br><span class="lead">{SUB}</span></h1>',
            '<p class="lead">商業・文化・福祉・交通を「広場」でつなぐ——自治体とデベロッパーの実務</p>',
            f'<p class="lead">{AUTHOR}</p>',
            '<div class="kami"><p><strong>公共施設を「何と、どこで、どう束ねるか」を、自治体と商業施設のデベロッパーの双方が判断できるようにする本です。</strong></p>'
            '<p>全国の事例を組み合わせごとに整理し、人口規模別に「理想・次善・最低限」を示します。'
            'このページでは、目次と各章の要点を紹介しています。事例の詳しい経緯、数字、点検表は本に載せています。</p></div>',
            '<h2 id="toc">目次</h2>']
    last = None
    for src, part in pm.CHAPTERS:
        md_text = (SRC / f"{src}.md").read_text(encoding="utf-8")
        if part != last and part != "序章":
            rows.append(f'<div class="part">{part}</div>')
            last = part
        for lv, t, _ in pm.toc_entries(md_text, src[:2]):
            if lv == 1:
                rows.append(f'<h3 class="toc-ch">{t}</h3>')
                pts = points_of(md_text)
                if pts:
                    rows.append(f'<div class="kami"><p><strong>この章の要点</strong></p>{pts}</div>')
            elif lv == 2:
                rows.append(f'<p class="toc-sec">{t}</p>')
            else:
                rows.append(f'<p class="toc-case">事例　{t}</p>')
    rows += ['<h2 id="updates">更新情報</h2>',
             '<p>制度の改正などで本の記述が変わったときは、ここでお知らせします。</p>',
             f'<p>{UPDATED}　紹介ページを公開しました。</p>']
    (OUT / "index.html").write_text(page("本の紹介と目次", f"{BOOK}{SUB}　本の紹介と目次", "\n".join(rows)),
                                    encoding="utf-8")
    fig = OUT / "fig"
    if fig.exists():
        for p in fig.glob("*"):
            p.unlink()
        fig.rmdir()
    print("built:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
