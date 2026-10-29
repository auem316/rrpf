"""公共施設複合化ポータルの静的ページを生成する。
使い方: python3 build.py <paper.md> <リポジトリの出力先> <プレビュー用の出力先>
"""
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

from content import CASES, CATEGORIES, ISSUES, RECS, TERMS

PAPER_MD, REPO_OUT, PREVIEW_OUT = map(Path, sys.argv[1:4])

SITE = "公共施設複合化ポータル"
UPDATED = "2026年10月29日"
FONTS = "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Shippori+Mincho:wght@700&display=swap"

PAGES = [
    ("index.html", "ポータルトップ"),
    ("paper.html", "論点整理ペーパー"),
    ("cases.html", "事例集"),
    ("glossary.html", "用語集"),
]

BASE_URL = "https://hosp.jp/fukugo/"
GA4_ID = "G-JPKJQ6S6Y9"  # hosp.jp の全ポータル共通の測定ID

# 関連ポータルの並びは hosp.jp/fm/ と同じ。このポータルは公共施設マネジメントの次に置く
SISTERS = [
    ("https://hosp.jp/fm/", "公共施設マネジメント"),
    (BASE_URL, "公共施設の複合化"),
    ("https://hosp.jp/ppp/", "公民連携"),
    ("https://hosp.jp/energy/", "自治体エネルギー"),
    ("https://hosp.jp/gov-ai/", "自治体生成AI"),
    ("https://hosp.jp/biz-ai/", "企業の生成AI"),
    ("https://hosp.jp/edu-ai/", "学校と教育の生成AI"),
    ("https://hosp.jp/const-ai/", "建設業のAI"),
    ("https://hosp.jp/ai-security/", "AIセキュリティ"),
    ("https://hosp.jp/hr/", "自治体人材"),
    ("https://hosp.jp/gov-biz/", "自治体ビジネス参入"),
    ("https://hosp.jp/chiiki-mirai/", "地域未来交付金"),
    ("https://hosp.jp/kotsu/", "地域公共交通"),
    ("https://shokubase.jp/", "食の拠点"),
    ("https://hosp.jp/", "運営サイトへ"),
]

GA4 = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
</script>"""

e = html.escape


def sec_for_issue(n):
    return f"sec-{n + 2}" if n else "sec-2"


def head(title, desc, current, preview=False):
    url = BASE_URL + ("" if current == "index.html" else current)
    # プレビューでは外部のスクリプトを読めないので、計測タグは公開用だけに入れる
    ga = "" if preview else GA4 + "\n"
    return f"""{ga}<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'website' if current == 'index.html' else 'article'}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Horizon-Shift Partners">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/portal.css">"""


def header(current):
    links = []
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    links.append('<a class="nav-cta" href="https://hosp.jp/contact/">ご相談</a>')
    sisters = " ".join(
        f'<a href="{h}" aria-current="true">{e(l)}</a>' if h == BASE_URL else f'<a href="{h}">{e(l)}</a>'
        for h, l in SISTERS
    )
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><span class="brand-name">{SITE}</span><span class="brand-sub">減らすから、組み替えるへ</span></a>
    <nav class="nav" aria-label="ポータル内">{"".join(links)}</nav>
  </div>
</header>
<div class="sister"><div class="wrap"><span>関連ポータル</span> {sisters}</div></div>"""


FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div>
      <p>数値と制度の記述は、2026年7月に一次資料と照合したデータと、2026年10月に確認した公表資料によります。各ページの出典をご確認ください。アウガ・豊島区・エリアなかいちなどの記述の一部は報道に基づきます。</p>
      <p>本ポータルは一般的な情報提供を目的としたもので、法的・財務的な助言ではありません。個別の案件は所管の省庁・専門家にご確認ください。</p>
      <p>最終更新: {UPDATED}　© Horizon-Shift Partners</p>
    </div>
    <ul>
      <li><a href="paper.html">論点整理ペーパー</a></li>
      <li><a href="cases.html">事例集</a></li>
      <li><a href="glossary.html">用語集</a></li>
      <li><a href="https://hosp.jp/contact/">講演・研修・個別相談のお問い合わせ</a></li>
    </ul>
  </div>
</footer>"""


def page(fname, title, desc, body, preview):
    h = head(title, desc, fname, preview)
    doc_body = f"{header(fname)}\n<main id=\"main\">\n{body}\n</main>\n{FOOTER}\n"
    if preview and fname == "index.html":
        # プレビューのトップページは公開時に外枠が付くため、中身だけを書く
        return f"{h}\n{doc_body}"
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{h}
</head>
<body>
{doc_body}</body>
</html>
"""


# ---------- トップページ ----------
PLAZA_SVG = """<svg viewBox="0 0 480 340" role="img" aria-labelledby="plaza-t plaza-d">
  <title id="plaza-t">広場を囲む施設の配置</title>
  <desc id="plaza-d">中央の広場を役所、図書館・文化、商業・市場、子育て・福祉の4つの施設が囲み、駐車場と道路は外周にまとめた配置図</desc>
  <rect x="4" y="4" width="472" height="332" rx="10" fill="var(--bg)" stroke="var(--line)"/>
  <rect x="16" y="16" width="448" height="308" rx="8" fill="none" stroke="var(--ink-soft)" stroke-width="10" stroke-opacity="0.18"/>
  <g font-family="var(--font-body)" font-size="11" fill="var(--ink-soft)">
    <rect x="30" y="30" width="44" height="30" rx="4" fill="var(--surface)" stroke="var(--line)"/><text x="52" y="50" text-anchor="middle">P</text>
    <rect x="406" y="280" width="44" height="30" rx="4" fill="var(--surface)" stroke="var(--line)"/><text x="428" y="300" text-anchor="middle">P</text>
    <text x="240" y="330" text-anchor="middle">道路と駐車場は外周へ</text>
  </g>
  <g font-family="var(--font-display)" font-size="15" font-weight="700" fill="var(--ink)">
    <rect x="160" y="40" width="160" height="58" rx="5" fill="var(--surface)" stroke="var(--ink-soft)"/>
    <text x="240" y="74" text-anchor="middle">役所・窓口</text>
    <rect x="40" y="114" width="96" height="112" rx="5" fill="var(--surface)" stroke="var(--ink-soft)"/>
    <text x="88" y="166" text-anchor="middle">図書館</text><text x="88" y="186" text-anchor="middle">文化</text>
    <rect x="344" y="114" width="96" height="112" rx="5" fill="var(--surface)" stroke="var(--ink-soft)"/>
    <text x="392" y="166" text-anchor="middle">商業</text><text x="392" y="186" text-anchor="middle">市場</text>
    <rect x="160" y="242" width="160" height="58" rx="5" fill="var(--surface)" stroke="var(--ink-soft)"/>
    <text x="240" y="276" text-anchor="middle">子育て・福祉</text>
  </g>
  <rect x="152" y="110" width="176" height="120" rx="4" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.5"/>
  <g stroke="var(--accent)" stroke-opacity="0.25">
    <line x1="152" y1="140" x2="328" y2="140"/><line x1="152" y1="170" x2="328" y2="170"/><line x1="152" y1="200" x2="328" y2="200"/>
    <line x1="196" y1="110" x2="196" y2="230"/><line x1="240" y1="110" x2="240" y2="230"/><line x1="284" y1="110" x2="284" y2="230"/>
  </g>
  <g fill="var(--ochre)">
    <circle cx="178" cy="128" r="3.5"/><circle cx="214" cy="186" r="3.5"/><circle cx="262" cy="152" r="3.5"/><circle cx="300" cy="212" r="3.5"/>
    <circle cx="226" cy="124" r="3.5"/><circle cx="306" cy="132" r="3.5"/><circle cx="170" cy="210" r="3.5"/><circle cx="252" cy="214" r="3.5"/>
  </g>
  <g stroke="var(--accent)" stroke-width="2" fill="none" stroke-linecap="round">
    <path d="M240 98 V110"/><path d="M136 170 H152"/><path d="M328 170 H344"/><path d="M240 230 V242"/>
  </g>
  <text x="240" y="176" text-anchor="middle" font-family="var(--font-display)" font-size="17" font-weight="700" fill="var(--accent)">広場</text>
</svg>"""


def build_index():
    issues = []
    for n, short, q, ans, mark in ISSUES:
        tag = f'<span class="tag-main">{mark}</span>' if mark else ""
        issues.append(f"""<a class="issue" href="paper.html#{sec_for_issue(n)}">
  <span class="issue-no">論点{n}　{e(short)} {tag}</span>
  <h3>{e(q)}</h3>
  <p>{e(ans)}</p>
</a>""")
    recs = "\n".join(
        f'<li><span class="rec-no">{i}</span><span>{e(t)}</span><span class="rec-phase">{e(p)}</span></li>'
        for i, (t, p) in enumerate(RECS, 1)
    )
    body = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">公共施設の複合化を考える自治体のために</p>
      <h1>施設を「減らす」から、まちを「組み替える」へ</h1>
      <p class="lede">商業施設にも公共施設にも、まわりに人と便益を広げる力があります。自動車社会はその力を道路と駐車場で分断し、商店街の衰退を招きました。このポータルは、役所・文化・商業・福祉をもう一度ひとつの「場」に集めるための論点と事例を、自治体の担当者向けにまとめたものです。</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="paper.html">論点整理ペーパーを読む</a>
        <a class="btn btn-ghost" href="cases.html">事例集を見る</a>
      </div>
    </div>
    <figure class="plaza-figure">
      {PLAZA_SVG}
      <figcaption>ヨーロッパの広場のように、施設の入口を広場に向けて集めると、それぞれの外部経済効果が重なり合います。</figcaption>
    </figure>
  </div>
</section>

<section class="facts" aria-label="主な数字">
  <div class="wrap facts-grid">
    <div class="fact"><span class="fact-num">1,788<small>団体</small></span><span class="fact-label">総合管理計画をつくった自治体（100%）。それでも延床面積は10年で1.3%増えた</span></div>
    <div class="fact"><span class="fact-num">約39<small>%</small></span><span class="fact-label">他の公共施設と複合化・共用化している学校（11,450校）。相手の多くは倉庫と放課後児童クラブ</span></div>
    <div class="fact"><span class="fact-num">令和8<small>年度</small></span><span class="fact-label">適正管理債（借入90%・国の手当て50%）の工事着手の期限</span></div>
    <div class="fact"><span class="fact-num">203<small>か所</small></span><span class="fact-label">Park-PFIの活用（2026年3月末）。東京・福岡・神奈川・愛知・大阪に偏る</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="section-head">
      <p class="eyebrow">基本の考え方</p>
      <h2>外部経済効果を、道路で分断せず「広場」でつなぐ</h2>
    </div>
    <div class="prose">
      <p>店が集まれば客が歩いて回り、隣の店も潤います。役所や図書館、病院は毎日決まって人を呼び、その人たちが帰りに買い物をします。二つの効果が同じ場所で重なるとき、まちのにぎわいが生まれます。</p>
      <p>車で移動する社会では、役所は郊外の広い敷地へ、商業は幹線道路沿いの大型店へ移り、施設どうしが道路と駐車場で切り離されました。シエナのカンポ広場やドイツのマルクト広場のように、市庁舎・教会・市場が一つの広場を囲む配置が、その反対側にあります。</p>
      <p><a href="paper.html#sec-2">第2章「基本の考え方」を読む</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">12の論点</p>
      <h2>複合化を検討するときの問いと、その答えの要点</h2>
      <p>カードを選ぶと、論点整理ペーパーの該当する章に移ります。</p>
    </div>
    <div class="issue-grid">
{chr(10).join(issues)}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="section-head">
      <p class="eyebrow">中心論点</p>
      <h2>地方の再開発が失敗した6つの型</h2>
      <p>駅前の再開発ビルでテナントが集まらず、空いた床を公共施設で埋める。この結末が各地で繰り返されてきました。根っこにあるのは「商業が主役、公共は穴埋め」という順序です。</p>
      <p><a href="paper.html#sec-11">融合戦略の7つの原則を読む</a></p>
    </div>
    <ol class="pitfalls">
      <li><div><strong>売上の見込みが楽観的すぎる</strong><span>青森市アウガは初年度の売上が計画の半分以下だった</span></div></li>
      <li><div><strong>商業床が売れる前提でお金を組む</strong><span>地方では保留床の買い手がおらず、第三セクターや自治体が抱える</span></div></li>
      <li><div><strong>核となる大型店に頼る</strong><span>百貨店やスーパーが抜けるとビル全体が一気に空く</span></div></li>
      <li><div><strong>郊外化と車社会を見ない</strong><span>郊外のバイパス沿いに店が集まり、中心部の地価は下がり続ける</span></div></li>
      <li><div><strong>補助金で規模が膨らむ</strong><span>公費でまかなえるため、身の丈を超えた床を建ててしまう</span></div></li>
      <li><div><strong>公共施設が後から穴埋めで入る</strong><span>置く必然性が薄いまま、管理費と修繕費を払い続ける</span></div></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">18の提言</p>
      <h2>今年度から着手できること</h2>
      <p>時期は、見える化（Phase 1）、構想と試行（Phase 2）、事業化と運営（Phase 3）の3段階で示しています。</p>
    </div>
    <ol class="recs">
{recs}
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="doors">
      <a class="door" href="paper.html"><h3>論点整理ペーパー</h3><p>背景から12の論点、18の提言、ロードマップまでを一つにまとめた本文です。</p><span class="go">本文を読む</span></a>
      <a class="door" href="cases.html"><h3>事例集（{len(CASES)}件）</h3><p>国内外の成功例と、構造から学ぶべき注意事例を、分野別に絞り込めます。</p><span class="go">事例を探す</span></a>
      <a class="door" href="glossary.html"><h3>用語集（{len(TERMS)}語）</h3><p>保留床、定期借地、Park-PFIなど、複合化の議論に出てくる言葉を短く説明します。</p><span class="go">用語を調べる</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <div>
        <h2>講演・研修・個別のご相談</h2>
        <p>施設再編計画への落とし込み、庁内研修、議会や住民への説明資料づくりをお手伝いします。</p>
      </div>
      <a class="btn btn-primary" href="https://hosp.jp/contact/">お問い合わせ</a>
    </div>
  </div>
</section>"""
    return body


# ---------- 論点整理ペーパー ----------
ROADMAP_SVG = """<figure class="roadmap" aria-label="複合化のロードマップ">
<svg viewBox="0 0 760 300" role="img" aria-label="まず見える化から始め、2つの関門で立ち止まりながら事業化へ" font-family="var(--font-body)" font-size="13">
  <text x="24" y="34" font-size="15" font-weight="700" fill="var(--ink)">まず見える化から始め、2つの関門で立ち止まりながら事業化へ</text>
  {boxes}
  {gates}
</svg>
</figure>"""


def roadmap():
    phases = [
        (24, True, "Phase 1　見える化", "0〜1年目", ["施設カルテの公開", "中学校区ごとの機能の地図", "起債の期限で案件を仕分け", "庁内の横断チームを設置"]),
        (274, False, "Phase 2　構想と試行", "1〜3年目", ["地区別ワークショップ", "複数案と削減の全体像を提示", "民間へのサウンディング", "社会実験で需要を確認"]),
        (524, False, "Phase 3　事業化と運営", "3年目〜", ["運営者とテナントを先に決定", "事業者選定・設計・整備", "利益還元・見直しの条項", "運営の評価を毎年公表"]),
    ]
    boxes = []
    for x, main, name, period, items in phases:
        fill = 'fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"' if main else 'fill="var(--surface)" stroke="var(--ink-soft)" stroke-width="1.25"'
        lines = "".join(f'<text x="{x + 16}" y="{144 + i * 20}" font-size="11.5" fill="var(--ink)">{e(t)}</text>' for i, t in enumerate(items))
        boxes.append(f'<g><rect x="{x}" y="64" width="210" height="160" rx="8" {fill}/><line x1="{x + 16}" y1="120" x2="{x + 194}" y2="120" stroke="var(--line)"/><text x="{x + 16}" y="90" font-weight="700" fill="var(--ink)">{e(name)}</text><text x="{x + 16}" y="110" font-size="11.5" fill="var(--ink-soft)">{e(period)}</text>{lines}</g>')
    gates = []
    for cx, name, desc in [(254, "関門1", "候補エリアと必要な機能に合意"), (504, "関門2", "試行の結果を踏まえ1案に決定")]:
        gates.append(f'<g><polygon points="{cx - 12},144 {cx},132 {cx + 12},144 {cx},156" fill="var(--accent)"/><line x1="{cx}" y1="156" x2="{cx}" y2="238" stroke="var(--ink-soft)" stroke-dasharray="3 3"/><text x="{cx}" y="256" text-anchor="middle" font-weight="700" fill="var(--ink)">{name}</text><text x="{cx}" y="274" text-anchor="middle" font-size="11.5" fill="var(--ink-soft)">{e(desc)}</text></g>')
    return ROADMAP_SVG.format(boxes="".join(boxes), gates="".join(gates))


def clean_paper(md):
    lines = md.splitlines()
    out = []
    for ln in lines:
        if ln.startswith("# ") or ln.startswith("Oct 22, 2026"):
            continue
        # 公開資料で裏付けを取れていない3事例と、その注記は公開版から外す
        if ln.startswith(("| 大船渡市", "| 下諏訪町", "| 白馬村")) or ln.startswith("大船渡市・下諏訪町・白馬村の内容は"):
            continue
        if "embedded content" in ln:
            out.append("ROADMAP_PLACEHOLDER")
            continue
        out.append(ln)
    md = "\n".join(out)
    md = md.replace("(<https://en.wikipedia.org/wiki/Market_Hall_(Rotterdam)>)", "(https://en.wikipedia.org/wiki/Market_Hall_%28Rotterdam%29)")
    md = md.replace("農業", "農業").replace("マイナビ农業", "マイナビ農業")
    # 「* 」で始まる出典の箇条書きを「- 」にそろえる
    md = re.sub(r"^\* ", "- ", md, flags=re.M)
    md = md.replace("- [ ] ", "- ")
    return md


def build_paper():
    md = clean_paper(PAPER_MD.read_text(encoding="utf-8"))
    body = markdown.markdown(md, extensions=["tables", "sane_lists"])
    body = body.replace("<p>ROADMAP_PLACEHOLDER</p>", roadmap())
    body = re.sub(r"<table>", '<div class="table-scroll"><table>', body)
    body = body.replace("</table>", "</table></div>")
    body = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', body)

    toc = []
    count = {"n": 0}

    def h2(m):
        text = m.group(1)
        plain = re.sub(r"<[^>]+>", "", text)
        if plain.startswith("参考資料"):
            sid = "sec-sources"
        elif plain.startswith("要旨"):
            sid = "sec-0"
        else:
            num = re.match(r"(\d+)\.", plain)
            sid = f"sec-{num.group(1)}" if num else f"sec-x{count['n']}"
        count["n"] += 1
        toc.append((sid, plain))
        return f'<h2 id="{sid}">{text}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    # まとめのチェックリスト
    body = re.sub(r'(<h2 id="sec-16">.*?</h2>.*?)<ul>', r'\1<ul class="checklist">', body, count=1, flags=re.S)
    # 出典以降を小さな文字に
    body = body.replace('<h2 id="sec-sources">', '<div class="sources"><h2 id="sec-sources">') + "</div>"

    toc_html = "\n".join(f'<li><a href="#{sid}">{e(t)}</a></li>' for sid, t in toc)
    return f"""<div class="page-head wrap">
  <p class="eyebrow">論点整理ペーパー</p>
  <h1>公共施設の複合化戦略</h1>
  <p class="lede">自治体が公共施設を、他の公共施設や商業施設、文化施設、福祉施設、公園、地域公共交通などと複合化するときに検討すべき論点を、12の問いと18の提言に整理しました。特定の自治体を前提にしない一般論です。</p>
</div>
<div class="wrap paper-layout">
  <nav class="toc" aria-label="目次"><p>目次</p><ol>
{toc_html}
  </ol></nav>
  <article class="paper">
{body}
  </article>
</div>"""


# ---------- 事例集 ----------
def build_cases():
    cat_label = dict(CATEGORIES)
    chips = "".join(
        f'<button type="button" class="chip" id="chip-{k}" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(l)}</button>'
        for k, l in CATEGORIES
    )
    cards = []
    for c in CASES:
        caution = "caution" in c["cats"]
        tags = "".join(
            f'<span class="case-tag{" caution" if k == "caution" else ""}">{e(cat_label[k])}</span>' for k in c["cats"]
        )
        meta = " ".join(f"<span>{e(x)}</span>" for x in (c["place"], c["year"]) if x)
        issue_label = f"論点{c['issue']}" if c["issue"] else "基本の考え方"
        cards.append(f"""<article class="case{" is-caution" if caution else ""}" data-cats="{" ".join(c["cats"])}">
  <div class="case-meta">{meta}</div>
  <h3>{e(c["name"])}</h3>
  <p>{e(c["what"])}</p>
  <p class="lesson"><b>学び：</b>{e(c["lesson"])}</p>
  <div class="case-links"><a href="{e(c["url"])}" target="_blank" rel="noopener">出典：{e(c["src"])}</a><a href="paper.html#{sec_for_issue(c["issue"])}">{issue_label}で読む</a></div>
  <div class="case-tags">{tags}</div>
</article>""")
    script = """<script>
(function () {
  var chips = document.querySelectorAll('.chip');
  var cards = document.querySelectorAll('.case');
  var count = document.getElementById('case-count');
  function apply(cat) {
    var shown = 0;
    cards.forEach(function (card) {
      var hit = cat === 'all' || card.getAttribute('data-cats').split(' ').indexOf(cat) >= 0;
      card.hidden = !hit;
      if (hit) shown++;
    });
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-cat') === cat ? 'true' : 'false'); });
    count.textContent = shown + '件を表示しています';
    try { if (cat === 'all') { history.replaceState(null, '', location.pathname); } else { history.replaceState(null, '', '#' + cat); } } catch (e) {}
  }
  chips.forEach(function (c) { c.addEventListener('click', function () { apply(c.getAttribute('data-cat')); }); });
  var start = (location.hash || '').replace('#', '');
  if (document.getElementById('chip-' + start)) apply(start);
})();
</script>"""
    return f"""<div class="page-head wrap">
  <p class="eyebrow">事例集</p>
  <h1>国内外の複合化の事例</h1>
  <p class="lede">成功例だけでなく、構造的な理由でつまずいた事例も載せています。注意すべき事例は、個別の努力不足ではなく、仕組みから起きたこととして読んでください。分野を選ぶと絞り込めます。</p>
</div>
<section class="wrap" style="padding-block: 0 4rem;">
  <div class="filters" role="group" aria-label="分野で絞り込む">{chips}</div>
  <p class="case-count" id="case-count" aria-live="polite">{len(CASES)}件を表示しています</p>
  <div class="case-grid">
{chr(10).join(cards)}
  </div>
</section>
{script}"""


# ---------- 用語集 ----------
def build_glossary():
    items = []
    for i, (term, yomi, desc, link) in enumerate(TERMS):
        items.append(f"""<div class="term" id="term-{i + 1}">
  <dt>{e(term)}<small>{e(yomi)}</small></dt>
  <dd>{e(desc)}<a class="see" href="{link}">ペーパーの関連する章へ</a></dd>
</div>""")
    return f"""<div class="page-head wrap">
  <p class="eyebrow">用語集</p>
  <h1>複合化の議論に出てくる言葉</h1>
  <p class="lede">行政や不動産の専門用語を、はじめて読む人にも伝わるように短く説明しています。制度の詳細は、所管の省庁の資料でご確認ください。</p>
</div>
<section class="wrap" style="padding-block: 0 4rem;">
  <dl class="glossary">
{chr(10).join(items)}
  </dl>
</section>"""


def main():
    builds = {
        "index.html": ("公共施設複合化ポータル", "公共施設を他の公共施設や商業・文化・福祉施設、公園、地域公共交通と複合化するための論点・事例・用語をまとめた自治体向けポータル。", build_index()),
        "paper.html": ("公共施設の複合化戦略 論点整理ペーパー｜公共施設複合化ポータル", "公共施設の複合化を検討するときの12の論点と18の提言。", build_paper()),
        "cases.html": ("事例集｜公共施設複合化ポータル", "国内外の公共施設の複合化の事例と、注意すべき事例。", build_cases()),
        "glossary.html": ("用語集｜公共施設複合化ポータル", "公共施設の複合化の議論に出てくる用語の解説。", build_glossary()),
    }
    css = Path(__file__).parent / "portal.css"
    for out, preview in ((REPO_OUT, False), (PREVIEW_OUT, True)):
        (out / "assets").mkdir(parents=True, exist_ok=True)
        for fname, (title, desc, body) in builds.items():
            (out / fname).write_text(page(fname, title, desc, body, preview), encoding="utf-8")
    if PREVIEW_OUT != REPO_OUT:
        shutil.copy(REPO_OUT / "assets" / "portal.css", PREVIEW_OUT / "assets" / "portal.css")


if __name__ == "__main__":
    main()
