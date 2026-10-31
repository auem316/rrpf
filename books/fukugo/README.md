# 『公共施設の複合化』出版企画

- 企画書（案）：https://claude.ai/artifact/41RdDdx4rPW473n5DTA9cj
- 元になった論点整理ペーパー：https://claude.ai/artifact/Jqw2LxfseBy4XVGgLV7nd3
- 公開ポータル：https://hosp.jp/fukugo/

## 見本原稿（Web版）

| ファイル | 中身 |
| --- | --- |
| manuscript/00_josho.md | 序章 なぜ「減らす」から「組み替える」へなのか |
| manuscript/01_hiroba.md | 第1章 外部経済効果を「広場」でつなぐ |
| manuscript/02_ruikei.md | 第2章 何と何を組み合わせるか（4つの類型） |
| manuscript/03_saikaihatsu.md | 第3章 地方の再開発はなぜ失敗したか |
| manuscript/17_kokyo-tenant.md | 第17章 公共テナントは商業施設に何をもたらすか |
| manuscript/konkyo.md | 根拠資料——章別 |
| manuscript/checklist.md | 章別チェックリスト |

文体と紙面は『自治体の公民連携ハンドブック』（hosp.jp/ppp/book/）にそろえている（である調、要点は番号付き、根拠資料とチェックリストは別ページ）。

Web版は `python3 bin/web.py` で `web/` に組む。デザインは姉妹編と同じ。公開先は hosp.jp/fukugo/book/ を想定（いまは noindex）。

紙版はWeb版の約4割に絞る予定。〔図〇-〇〕は図の差し込み位置、【要確認】は公開資料で裏付けが取れていない点。

紙面（A5の見本PDF）は `python3 bin/print.py` で `print/mihon.pdf` に組む。公民連携ハンドブックの紙面（ポイント欄、節見出し、囲み、柱とノンブル）にそろえている。

図は `python3 bin/figs.py` で `fig/` に作る（紙版の図の決まり：最小の文字15以上、文字22個以内、総字数260字以内、幅820以内、色は濃淡だけ、図題は図の外）。
