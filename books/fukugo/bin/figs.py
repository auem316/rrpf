"""見本章の図（SVG）を作る。『自治体の公民連携ハンドブック』の図と同じ描き方。

決まり：幅820以内／最小の文字15以上／<text> 22個以内／色は currentColor の濃淡だけ／図題は図の中に書かない。
使い方: python3 bin/figs.py   （出力は fig/）
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "fig"
FONT = "font-family:'Yu Gothic','Hiragino Kaku Gothic ProN','Noto Sans JP','Noto Sans CJK JP',sans-serif;color:inherit"


class Fig:
    def __init__(self, label, h):
        self.label, self.h, self.parts, self.n = label, h, [], 0

    def box(self, x, y, w, h, fill=0.0, sw=1.8, dash=False, rx=5):
        f = f'fill="currentColor" fill-opacity="{fill}"' if fill else 'fill="none"'
        d = ' stroke-dasharray="7 5"' if dash else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {f} stroke="currentColor" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=17, bold=False, anchor="middle"):
        b = ' font-weight="bold"' if bold else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}"{b} text-anchor="{anchor}">{s}</text>')

    def arrow(self, x1, y1, x2, y2, sw=2, dash=False):
        self.n += 1
        mid = f"a{self.n}"
        d = ' stroke-dasharray="6 5"' if dash else ""
        self.parts.append(
            f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9" fill="none" stroke="currentColor" stroke-width="2"/></marker></defs>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="{sw}"{d} marker-end="url(#{mid})"/>')

    def line(self, x1, y1, x2, y2, sw=2, op=1.0):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="{sw}" stroke-opacity="{op}"/>')

    def head(self, x, y, w, s):
        self.box(x, y, w, 44, fill=0.13, sw=2.2)
        self.text(x + w / 2, y + 29, s, 19, True)

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 832 {self.h + 12}" width="100%" role="img"\n'
                f' aria-label="{self.label}"\n style="{FONT}">\n' + "\n".join(self.parts) + "\n</svg>\n")


def fig1_1():
    f = Fig("図1-1　自動車社会の配置と、広場を中心にした配置", 330)
    # 左：自動車社会
    f.head(0, 0, 395, "自動車社会の配置")
    f.line(0, 165, 395, 165, sw=10, op=0.25)
    f.line(200, 60, 200, 268, sw=10, op=0.25)
    for x, y, s in [(22, 78, "役所"), (240, 190, "大型店"), (250, 76, "病院")]:
        f.box(x, y, 110, 52, sw=2)
        f.text(x + 55, y + 33, s, 17, True)
    for x, y in [(22, 190), (130, 76), (140, 205)]:
        f.box(x, y, 46, 40, fill=0.13, sw=1.4)
        f.text(x + 23, y + 27, "P", 17, True)
    # 右：広場中心
    f.head(425, 0, 395, "広場を中心にした配置")
    f.box(575, 130, 120, 80, fill=0.13, sw=2.2, dash=True)
    f.text(635, 177, "広場", 19, True)
    for x, y, s in [(580, 56, "役所"), (440, 144, "図書館"), (712, 144, "商業")]:
        f.box(x, y, 110 if s != "役所" else 110, 52, sw=2)
        f.text(x + 55, y + 33, s, 17, True)
    f.arrow(635, 110, 635, 128)
    f.arrow(552, 170, 573, 170)
    f.arrow(710, 170, 697, 170)
    f.box(440, 224, 70, 40, fill=0.13, sw=1.4)
    f.text(475, 251, "P", 17, True)
    f.box(750, 224, 70, 40, fill=0.13, sw=1.4)
    f.text(785, 251, "P", 17, True)
    # 下の結論
    f.box(0, 280, 395, 50, fill=0.13, sw=2.2)
    f.text(197, 311, "効果は施設ごとに閉じる", 19, True)
    f.box(425, 280, 395, 50, fill=0.13, sw=2.2)
    f.text(622, 311, "広場で効果が重なる", 19, True)
    return f


def fig1_2():
    f = Fig("図1-2　広場を囲む施設の配置（入口の向きと駐車場の位置）", 360)
    f.box(0, 0, 820, 300, sw=1.2, dash=True)
    f.box(270, 100, 280, 110, fill=0.13, sw=2.4)
    f.text(410, 145, "広場", 20, True)
    f.text(410, 178, "運営者と予算を先に決める", 16)
    for x, y, w, s in [(300, 22, 220, "公共施設（役所・図書館）"), (60, 120, 160, "文化施設"), (600, 120, 160, "商業")]:
        f.box(x, y, w, 52, sw=2.2)
        f.text(x + w / 2, y + 33, s, 17, True)
    f.arrow(410, 76, 410, 98)
    f.arrow(222, 155, 268, 155)
    f.arrow(598, 155, 552, 155)
    f.text(410, 248, "入口は広場に向ける", 17, True)
    f.box(20, 228, 150, 56, fill=0.13, sw=1.4)
    f.text(95, 262, "駐車場", 17, True)
    f.box(650, 228, 150, 56, fill=0.13, sw=1.4)
    f.text(725, 262, "駐車場", 17, True)
    f.arrow(410, 262, 410, 296, dash=True)
    f.text(410, 330, "商店街・停留所へ歩いて回る", 17)
    f.text(95, 222, "外周にまとめる", 15)
    return f


def fig3_1():
    f = Fig("図3-1　失敗の連鎖", 236)
    steps = [("保留床が", "売れない"), ("第三セクターが", "床を抱える"), ("商業が", "撤退する"), ("公共施設で", "埋める")]
    w, gap = 176, 39
    for i, (a, b) in enumerate(steps):
        x = i * (w + gap)
        f.box(x, 0, w, 96, fill=0.13 if i == 3 else 0, sw=2.2)
        f.text(x + w / 2, 40, a, 17)
        f.text(x + w / 2, 70, b, 19, True)
        if i < 3:
            f.arrow(x + w + 4, 48, x + w + gap - 4, 48)
    subs = ["床の買い手がいない", "債務超過・公費で支援", "キーテナントが抜ける", "置く必然性が薄い"]
    for i, s in enumerate(subs):
        f.text(i * (w + gap) + w / 2, 126, s, 15)
    f.arrow(410, 140, 410, 170)
    f.box(0, 180, 820, 54, fill=0.13, sw=2.2)
    f.text(410, 214, "施設の総量が増え、床の管理費と修繕費を払い続ける", 19, True)
    return f


def fig3_2():
    f = Fig("図3-2　二つの順序の比較", 300)
    rows = [("失敗の順序", ["再開発ビルを建てる", "商業で埋める", "空いた床を公共で埋める"], 0),
            ("融合の順序", ["施設再編計画で決める", "公共機能を核に置く", "テナント分だけ足す"], 128)]
    for label, items, y in rows:
        f.box(0, y, 140, 100, fill=0.13, sw=2.2)
        f.text(70, y + 57, label, 18, True)
        for i, s in enumerate(items):
            x = 170 + i * 220
            f.box(x, y + 14, 196, 72, sw=2 if y else 1.6, dash=(y == 0))
            f.text(x + 98, y + 57, s, 16, bool(y))
            if i < 2:
                f.arrow(x + 198, y + 50, x + 218, y + 50)
    f.box(0, 248, 820, 52, fill=0.13, sw=2.2)
    f.text(410, 281, "集客の核を、商業から公共に置き換える", 19, True)
    return f


def fig2_1():
    f = Fig("図2-1　4つの類型——相手が民間に近づくほど、価値もリスクも大きくなる", 340)
    items = [("A 公共×公共", "学校＋公民館"), ("B 公共×商業", "図書館＋飲食"),
             ("C 公共×働く場", "廃校＋オフィス"), ("D 公共×住まい", "庁舎＋住宅")]
    w, gap = 190, 20
    for i, (a, b) in enumerate(items):
        x = i * (w + gap)
        f.box(x, 0, w, 84, fill=0.06 + i * 0.07, sw=2.2)
        f.text(x + w / 2, 36, a, 18, True)
        f.text(x + w / 2, 66, b, 16)
    f.arrow(0, 112, 816, 112, sw=2.4)
    f.text(410, 140, "相手が民間に近づく", 17, True)
    f.parts.append('<path d="M0,226 L820,188 L820,226 Z" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.4"/>')
    f.text(0, 180, "価値：にぎわい・民間の資金", 16, True, "start")
    f.parts.append('<path d="M0,298 L820,260 L820,298 Z" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="1.4"/>')
    f.text(0, 252, "リスク：撤退・公費での穴埋め", 16, True, "start")
    f.text(410, 332, "B・C・D は、民間が稼げるかを確かめてから選ぶ", 16)
    return f


def fig2_2():
    f = Fig("図2-2　4つの問いで類型を選ぶ", 400)
    f.box(250, 0, 320, 56, fill=0.13, sw=2.2)
    f.text(410, 35, "④ その場所で束ねる施設か", 18, True)
    f.arrow(250, 28, 160, 28)
    f.box(0, 4, 156, 48, sw=1.4, dash=True)
    f.text(78, 34, "残す・転じる・畳む", 15)
    f.text(205, 20, "いいえ", 15)
    f.arrow(410, 58, 410, 92)
    f.text(440, 80, "はい", 15, False, "start")
    f.box(180, 96, 460, 84, sw=2)
    f.text(410, 130, "① 利用時間帯は補い合うか", 17)
    f.text(410, 162, "② 利用者は重なるか", 17)
    f.arrow(410, 182, 410, 214)
    f.box(250, 218, 320, 56, fill=0.13, sw=2.2)
    f.text(410, 253, "③ 民間が稼げる立地か", 18, True)
    f.arrow(330, 276, 210, 320)
    f.arrow(490, 276, 610, 320)
    f.text(250, 300, "いいえ", 15, False, "end")
    f.text(570, 300, "はい", 15, False, "start")
    f.box(0, 324, 400, 66, sw=2.2)
    f.text(200, 352, "A を軸にする", 18, True)
    f.text(200, 378, "民間は小さな床で試す", 16)
    f.box(420, 324, 400, 66, sw=2.2)
    f.text(620, 352, "A を核に B・C・D を足す", 18, True)
    f.text(620, 378, "テナントが決まった分だけ", 16)
    return f


def fig17_1():
    f = Fig("図17-1　4つの入り方と、お金・床の流れ", 392)
    # 列：入り方｜自治体｜流れ｜民間｜持ち主
    f.head(150, 0, 80, "自治体")
    f.head(490, 0, 80, "民間")
    f.head(590, 0, 230, "床・土地を持つのは")
    f.box(150, 52, 80, 300, fill=0.13, sw=0)
    f.box(490, 52, 80, 300, fill=0.13, sw=0)
    rows = [("① 賃貸借", "床を貸す", "賃料を毎年払う", "民間", True),
            ("② 今の床を買う", "できている床を売る", "代金を一度払う", "自治体（建物の一部）", True),
            ("③ 新築で買う", "注文どおり建てて渡す", "完成時に代金を払う", "公共部分は自治体", True),
            ("④ 定期借地", "土地を貸す", "地代を払う", "土地は自治体、建物は民間", False)]
    for i, (name, thing, money, owner, to_public) in enumerate(rows):
        y = 60 + i * 74
        f.box(0, y, 140, 62, sw=2)
        f.text(70, y + 38, name, 17, True)
        # 実線＝床・土地、点線＝お金
        if to_public:
            f.arrow(484, y + 22, 236, y + 22)
            f.arrow(236, y + 52, 484, y + 52, dash=True)
        else:
            f.arrow(236, y + 22, 484, y + 22)
            f.arrow(484, y + 52, 236, y + 52, dash=True)
        f.text(360, y + 15, thing, 15, True)
        f.text(360, y + 45, money, 15)
        f.box(590, y, 230, 62, sw=1.6)
        f.text(705, y + 38, owner, 16, True)
    f.text(410, 384, "実線は床・土地の動き、点線はお金の動き", 15)
    return f


def fig4_1():
    f = Fig("図4-1　学校の複合化の相手——多いのは「置くだけ」の施設", 420)
    rows = [("地域防災用備蓄倉庫", 7475), ("放課後児童クラブ", 6870), ("体育館等", 843), ("公民館等", 608),
            ("給食共同調理場", 409), ("児童館等", 170), ("保育所", 88), ("図書館", 75)]
    x0, maxw, rh = 250, 470, 40
    for i, (name, n) in enumerate(rows):
        y = 10 + i * rh
        f.text(x0 - 12, y + 24, name, 17, i < 2, anchor="end")
        w = max(4, round(maxw * n / 7475))
        f.box(x0, y + 4, w, 28, fill=0.38 if i < 2 else 0.13, sw=1.4, rx=2)
        f.text(x0 + w + 10, y + 25, f"{n:,}", 17, i < 2, anchor="start")
    f.line(x0, 6, x0, 10 + len(rows) * rh, sw=2)
    f.box(0, 350, 400, 66, fill=0.38, sw=2)
    f.text(200, 391, "空き教室や敷地に置くだけ", 18, True)
    f.box(420, 350, 400, 66, sw=2.2, dash=True)
    f.text(620, 391, "人が出入りする複合は少ない", 18, True)
    return f


def fig5_1():
    f = Fig("図5-1　借りるか、持つか——お金の出方の違い", 400)
    ox, oy, W, H = 90, 300, 690, 270
    f.line(ox, oy, ox + W, oy, sw=2)
    f.line(ox, oy, ox, oy - H, sw=2)
    f.text(ox - 14, oy - H + 16, "累計の", 16, anchor="end")
    f.text(ox - 14, oy - H + 38, "支出", 16, anchor="end")
    f.text(ox + W, oy + 30, "年数", 16, anchor="end")
    # 借りる：毎年の賃料が積み上がる
    f.parts.append(f'<polyline points="{ox},{oy} {ox + W},{oy - H + 10}" fill="none" stroke="currentColor" stroke-width="3.2"/>')
    # 持つ：最初に取得・改修、途中で大規模修繕
    pts = [(ox, oy), (ox, oy - 110), (ox + 460, oy - 135), (ox + 460, oy - 165), (ox + W, oy - 180)]
    f.parts.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) +
                   '" fill="none" stroke="currentColor" stroke-width="3.2" stroke-dasharray="10 6"/>')
    f.text(ox + W - 10, oy - H - 2, "借りる（賃料が毎年）", 17, True, anchor="end")
    f.text(ox + W - 10, oy - 192, "持つ", 17, True, anchor="end")
    f.text(ox + 14, oy - 120, "取得・改修", 16, anchor="start")
    f.text(ox + 472, oy - 140, "大規模修繕", 16, anchor="start")
    # 分かれ目（線が交わるあたり）
    cx = ox + 341
    f.line(cx, oy, cx, oy - 128, sw=1.6, op=0.6)
    f.text(cx, oy + 30, "分かれ目", 16, True)
    f.text(ox + 175, oy - 12, "短いなら借りる", 16)
    f.text(ox + 560, oy - 60, "長いなら持つ", 16)
    f.box(0, 340, 820, 56, fill=0.13, sw=2.2)
    f.text(410, 376, "先に「何年いるか」を決めれば、総額で比べられる", 18, True)
    return f


def fig6_1():
    f = Fig("図6-1　入口に商業、奥に文化——にぎやかさの順に並べる", 380)
    rows = [("奥・上の階", "閲覧席・学習席・郷土資料", 0.0),
            ("中ほど", "交流の場・工房・講座・子どもの本", 0.13),
            ("入口・1階", "カフェ・書店・新刊の棚・展示", 0.38)]
    for i, (pos, what, fill) in enumerate(rows):
        y = i * 92
        f.box(0, y, 170, 78, fill=0.13, sw=2.2)
        f.text(85, y + 47, pos, 18, True)
        f.box(190, y, 470, 78, fill=fill, sw=2)
        f.text(425, y + 47, what, 18, True)
    f.text(740, 40, "静か", 19, True)
    f.text(740, 248, "にぎやか", 19, True)
    f.arrow(740, 225, 740, 64, sw=2.6)
    f.box(0, 296, 820, 80, sw=2.2, dash=True)
    f.text(410, 330, "通りから入った人が、ついでに奥へ進む", 18, True)
    f.text(410, 360, "音と人の流れは、静かな場所に届きにくい", 16)
    return f


def fig7_1():
    f = Fig("図7-1　公民館に商業を入れる三つの道筋", 330)
    cols = [("① 公民館のまま", "区画を公募で貸す", "所管は変えない"),
            ("② コミセンに", "首長部局の施設へ", "稼ぐ自由が増える"),
            ("③ 住民の組織が", "指定管理で運営", "稼ぎが地域に残る")]
    w, gap = 260, 20
    for i, (a, b, c) in enumerate(cols):
        x = i * (w + gap)
        f.head(x, 0, w, a)
        f.box(x, 58, w, 116, sw=2, fill=0.13 if i == 2 else 0)
        f.text(x + w / 2, 104, b, 18, True)
        f.text(x + w / 2, 144, c, 16)
    f.arrow(410, 186, 410, 222)
    f.box(0, 234, 820, 90, fill=0.13, sw=2.2)
    f.text(410, 270, "どの道でも、事業者は公正に選び、賃料は相場に", 18, True)
    f.text(410, 304, "禁じられているのは、特定の事業者への優遇", 16)
    return f


def fig8_1():
    f = Fig("図8-1　閉じた施設から、まちの居場所へ", 340)
    cols = [("① 福祉×福祉", "高齢者＋子ども", "まだ閉じている", 0.0),
            ("② 福祉×商業", "温泉・食堂・売店", "住民が来る理由", 0.13),
            ("③ 福祉×文化", "図書館・公民館に", "日常の動線に乗る", 0.13)]
    w, gap = 240, 50
    for i, (a, b, c, fill) in enumerate(cols):
        x = i * (w + gap)
        f.head(x, 0, w, a)
        f.box(x, 58, w, 120, fill=fill, sw=2, dash=(i == 0))
        f.text(x + w / 2, 106, b, 18, True)
        f.text(x + w / 2, 146, c, 16)
        if i < 2:
            f.arrow(x + w + 6, 118, x + w + gap - 6, 118)
    f.arrow(410, 190, 410, 226)
    f.box(0, 238, 820, 96, fill=0.38, sw=2.2)
    f.text(410, 276, "自治体は、土地・床・条件を出す", 19, True)
    f.text(410, 310, "公募の条件に「地域に開く機能」の一行", 17)
    return f


def fig9_1():
    f = Fig("図9-1　Park-PFI のお金の流れ——収益施設の稼ぎを公園に戻す", 360)
    f.box(0, 40, 250, 110, fill=0.38, sw=2.2)
    f.text(125, 88, "収益施設", 19, True)
    f.text(125, 120, "カフェ・レストラン", 16)
    f.box(570, 40, 250, 110, sw=2.2)
    f.text(695, 88, "公園の広場・園路", 19, True)
    f.text(695, 120, "誰でも無料で使う", 16)
    f.arrow(256, 80, 562, 80, sw=2.6)
    f.text(410, 66, "稼ぎの一部で整備・運営", 17, True)
    f.arrow(562, 124, 256, 124, sw=2, dash=True)
    f.text(410, 150, "人が来て、長くいる", 16)
    f.box(150, 196, 520, 76, fill=0.13, sw=2)
    f.text(410, 228, "代わりに受ける特例", 17, True)
    f.text(410, 258, "期間 最長20年／建物 12%まで", 16)
    f.box(0, 296, 820, 60, sw=2.2, dash=True)
    f.text(410, 334, "人が集まる場所でしか回りにくい", 18, True)
    return f


def fig10_1():
    f = Fig("図10-1　食の拠点の五つの要素——市場と飲食から始める", 330)
    f.box(0, 0, 400, 130, fill=0.38, sw=2.4)
    f.text(200, 56, "市場", 21, True)
    f.text(200, 96, "毎日の需要・新鮮な食材", 16)
    f.box(420, 0, 400, 130, fill=0.38, sw=2.4)
    f.text(620, 56, "飲食・フードホール", 21, True)
    f.text(620, 96, "訪れるきっかけ・滞在", 16)
    items = [("人材育成", "県・大学・学校"), ("研究開発", "大学・試験研究機関"), ("交流", "広場・調理室・催し")]
    w, gap = 260, 20
    for i, (a, b) in enumerate(items):
        x = i * (w + gap)
        f.box(x, 160, w, 100, sw=2, dash=True)
        f.text(x + w / 2, 202, a, 19, True)
        f.text(x + w / 2, 236, b, 16)
    f.text(410, 300, "まず二つで始め、あとから既存の施設と組む", 18, True)
    return f


def fig11_1():
    f = Fig("図11-1　交通と複合施設の四つの組み合わせ方", 330)
    cells = [("① 結節型", "駅・ターミナルの隣に置く", "大都市"),
             ("② 拠点型", "束ねた施設を交通の起点に", "町村"),
             ("③ 回遊型", "散らばった施設を循環で結ぶ", "中規模の市"),
             ("④ 共有型", "病院・学校・企業の送迎を開く", "町村")]
    for i, (a, b, c) in enumerate(cells):
        x, y = (i % 2) * 420, (i // 2) * 165
        f.box(x, y, 400, 150, fill=0.13 if i in (1, 3) else 0, sw=2.2)
        f.text(x + 200, y + 46, a, 20, True)
        f.text(x + 200, y + 88, b, 17)
        f.text(x + 200, y + 124, "向く規模：" + c, 16)
    return f


def fig12_1():
    f = Fig("図12-1　収益還元の取引——見返りと還元は釣り合う", 340)
    f.box(0, 0, 330, 200, sw=2.2)
    f.head(0, 0, 330, "公共が渡す見返り")
    f.text(165, 92, "営業できる期間", 17)
    f.text(165, 128, "建てられる量", 17)
    f.text(165, 164, "使い方の自由", 17)
    f.box(490, 0, 330, 200, fill=0.13, sw=2.2)
    f.head(490, 0, 330, "民間が返す還元")
    f.text(655, 92, "整備・地代・使用料", 17)
    f.text(655, 128, "運営の肩代わり", 17)
    f.text(655, 164, "売上の一部", 17)
    f.arrow(338, 80, 482, 80, sw=2.6)
    f.arrow(482, 150, 338, 150, sw=2.6)
    f.text(410, 120, "取引", 18, True)
    f.box(0, 240, 820, 96, fill=0.38, sw=2.2)
    f.text(410, 280, "見返りが小さければ、還元も小さい", 19, True)
    f.text(410, 314, "足りない分は市の負担と組み合わせる（混合型）", 16)
    return f


def fig13_1():
    f = Fig("図13-1　寄附企業が商業施設の事業者でもある場合の三つの形", 340)
    cols = [("① 自治体が整備", "自治体が持ち、運営", "最も安全", 0.0),
            ("② 民間が整備し譲渡", "完成後に自治体へ", "代金と寄附を分ける", 0.13),
            ("③ 民間に補助", "民間が持ち、運営", "最も慎重に", 0.38)]
    w, gap = 260, 20
    for i, (a, b, c, fill) in enumerate(cols):
        x = i * (w + gap)
        f.head(x, 0, w, a)
        f.box(x, 58, w, 130, fill=fill, sw=2)
        f.text(x + w / 2, 108, b, 17, True)
        f.text(x + w / 2, 150, c, 17)
    f.box(0, 214, 820, 120, sw=2.2, dash=True)
    f.text(410, 254, "寄附は公益の部分に充て、額を約束しない", 18, True)
    f.text(410, 290, "お金の流れ・所有・契約を、営利の部分と分ける", 16)
    f.text(410, 320, "集まらなくても成り立つ財源を用意する", 16)
    return f


def check(f):
    import re
    s = f.svg()
    texts = re.findall(r"<text[^>]*>(.*?)</text>", s)
    sizes = [int(x) for x in re.findall(r'font-size="(\d+)"', s)]
    chars = sum(len(t) for t in texts)
    assert len(texts) <= 22, (f.label, "text", len(texts))
    assert min(sizes) >= 15, (f.label, "size", min(sizes))
    assert chars <= 260, (f.label, "chars", chars)
    return len(texts), chars


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in [("fig2-1_ruikei", fig2_1), ("fig2-2_toi", fig2_2), ("fig1-1_haichi", fig1_1), ("fig1-2_hiroba", fig1_2), ("fig3-1_rensa", fig3_1),
                     ("fig3-2_junjo", fig3_2), ("fig17-1_4hairikata", fig17_1),
                     ("fig4-1_aite", fig4_1), ("fig5-1_kariru-motsu", fig5_1),
                     ("fig6-1_dousen", fig6_1), ("fig7-1_3michi", fig7_1),
                     ("fig8-1_hiraku", fig8_1), ("fig9-1_parkpfi", fig9_1),
                     ("fig10-1_shoku", fig10_1), ("fig11-1_kotsu", fig11_1),
                     ("fig12-1_torihiki", fig12_1), ("fig13-1_kifu", fig13_1)]:
        f = fn()
        n, c = check(f)
        (OUT / f"{name}.svg").write_text(f.svg(), encoding="utf-8")
        print(f"{name}: text {n}, chars {c}")


if __name__ == "__main__":
    main()
