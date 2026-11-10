# 『公共施設の複合化』出版企画

- 企画書（案）：https://claude.ai/artifact/41RdDdx4rPW473n5DTA9cj
- 元になった論点整理ペーパー：https://claude.ai/artifact/Jqw2LxfseBy4XVGgLV7nd3
- 公開ポータル：https://hosp.jp/fukugo/

## 原稿（本の完全版）

| ファイル | 中身 |
| --- | --- |
| manuscript/00_josho.md | 序章 なぜ「減らす」から「組み替える」へなのか |
| manuscript/01_hiroba.md | 第1章 外部経済効果を「広場」でつなぐ |
| manuscript/02_ruikei.md | 第2章 何と何を組み合わせるか（4つの類型） |
| manuscript/03_saikaihatsu.md | 第3章 地方の再開発はなぜ失敗したか |
| manuscript/04_gakko.md | 第4章 公共×公共——学校を核にする |
| manuscript/05_shogyo.md | 第5章 公共×商業——床を借りるか、持つか |
| manuscript/06_bunka.md | 第6章 文化×商業——入口に商業、奥に文化 |
| manuscript/07_kominkan.md | 第7章 公民館×カフェ・居酒屋 |
| manuscript/08_fukushi.md | 第8章 福祉×商業・文化——幼老複合をまちの居場所に |
| manuscript/09_koen.md | 第9章 公園×収益施設——Park-PFIの先へ |
| manuscript/10_shoku.md | 第10章 食を核にする |
| manuscript/11_kotsu.md | 第11章 地域公共交通×複合施設 |
| manuscript/12_kangen.md | 第12章 商業の稼ぎで公共を支える（収益還元） |
| manuscript/13_okane.md | 第13章 お金をどう用意するか |
| manuscript/14_unei.md | 第14章 誰がどう運営するか |
| manuscript/15_goui.md | 第15章 試してから決める（合意形成） |
| manuscript/16_teigen.md | 第16章 18の提言とロードマップ |
| manuscript/17_kokyo-tenant.md | 第17章 公共テナントは商業施設に何をもたらすか |
| manuscript/18_jikanjiku.md | 第18章 自治体の決め方と時間軸を読む |
| manuscript/19_teian.md | 第19章 通る提案の組み立て |
| manuscript/konkyo.md | 根拠資料——章別 |
| manuscript/checklist.md | 章別チェックリスト |

文体と紙面は『自治体の公民連携ハンドブック』（hosp.jp/ppp/book/）にそろえている（である調、要点は番号付き）。

## 本とWebの役割（2026年11月10日に変更）

**最も詳しい内容は本に載せる。Webは本の紹介と、本への入口にする。** 学芸出版社の指摘（通読を前提に重複を減らす、事例を本に詳しく載せて目次に事例名を出す、Webに本と同じものを置かない）による。

- 本の原稿は `manuscript/` の1つだけ。紙版を別に削った原稿はやめた。
- 同じ事例を詳しく書くのは1か所にし、ほかの章からは「第3章3-5」のように節番号で指す。
- `python3 bin/print.py`：A5の見本紙面 `print/mihon.pdf` を組む。冒頭に目次（節と事例名、ページ番号つき）を置く。ページ番号は一度組んでから拾い直す。
- `python3 bin/web.py`：本の紹介ページ `web/index.html` だけを組む（書名、この本でできること、目次、各章の要点、更新情報）。本文は出さない。
- `python3 bin/check.py`：図の欠け、残った【要確認】、章をまたぐ重複の候補を出す。
- `python3 bin/figs.py`：図を `fig/` に作る（最小の文字15以上、文字22個以内、総字数260字以内、幅820以内、色は濃淡だけ、図題は図の外）。

公開中のポータル hosp.jp/fukugo/ は要約の段階のもので、今のまま残す。本への入口を加える。

〔図〇-〇〕は図の差し込み位置、【要確認】は公開資料で裏付けが取れていない点。
