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


def fig17_1():
    f = Fig("図17-1　4つの入り方と、お金・床の流れ", 392)
    # 列：入り方｜自治体｜流れ｜民間｜持ち主
    f.head(150, 0, 80, "自治体")
    f.head(490, 0, 80, "民間")
    f.head(590, 0, 230, "床・土地を持つのは")
    f.box(150, 52, 80, 300, fill=0.13, sw=0)
    f.box(490, 52, 80, 300, fill=0.13, sw=0)
    rows = [("① 賃貸借", "床を貸す", "賃料を毎年払う", "民間", True),
            ("② 区分所有", "床を売る", "代金を一度払う", "自治体（床）", True),
            ("③ 買い取り", "建てて公共部分を渡す", "買取代金を払う", "公共部分は自治体", True),
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
    for name, fn in [("fig1-1_haichi", fig1_1), ("fig1-2_hiroba", fig1_2), ("fig3-1_rensa", fig3_1),
                     ("fig3-2_junjo", fig3_2), ("fig17-1_4hairikata", fig17_1)]:
        f = fn()
        n, c = check(f)
        (OUT / f"{name}.svg").write_text(f.svg(), encoding="utf-8")
        print(f"{name}: text {n}, chars {c}")


if __name__ == "__main__":
    main()
