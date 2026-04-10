# Sprint 3 ｜ PM 最終レビュー

> 作成者：PM  
> 作成日：2026-04-06  
> 対象：Sprint 3 v3 レビュー対応実装（report.md 更新版）  
> 判定：**✅ 条件付き承認（軽微な修正1点のみ）**

---

## 評価サマリー

①〜⑤ 全項目が実装されており、各仕様に沿った実装品質を確認した。設計意図が正確にコードに落とし込まれている。1点の軽微な見落とし（アクセシビリティ属性）を修正すれば Sprint 3 をクローズできる。

---

## 各項目の評価

### ① ヒーローレイアウト：3ゾーン構成

**判定：承認**

`.hero-top`（h1 フル幅・`font-size: 3.5rem`）と `.hero-bottom`（2カラム）の構造が正しく実装されている。`max-width: 1080px; margin: 0 auto;` が `.hero-top` / `.hero-bottom` 双方に付与されており、コンテンツ幅が正しく制御されている。SP対応（900px: `1fr`崩し / 480px: `1.9rem`）も適切。

---

### ② border-radius：フラット

**判定：承認**

`.hero { border-radius: 0; }` が実装されている。`.hero` の `margin: 0 -32px` による full-width 表現は継続されており、フラット下辺がページ全幅に渡って表示される。

実装担当からの確認依頼（stats 直下の境界が直線になること）については、本番公開時にブラウザで視認確認を行う。現時点でのコードに問題はない。

---

### ③ サービスカードSVGアイコン

**判定：条件付き承認（→ 要修正1点）**

3アイコン（モニター+チェック / 歯車 / シールド+チェック）が各カード `<h3>` の直前に挿入され、stroke 色 `#0a4f9f` で統一されている。`.card .card-icon { display: block; margin-bottom: 16px; }` も設定済み。

**【要修正】`aria-hidden="true"` が全3SVGに未付与。**

設計仕様書（v3.0 「実装上の注意点」）に「`aria-hidden="true"` を必ず付与する」と明記されていた箇所。スクリーンリーダーがSVGを不要に読み上げるリスクがある。追加してください。

```html
<!-- 修正前 -->
<svg class="card-icon" width="40" height="40" ...>

<!-- 修正後 -->
<svg class="card-icon" width="40" height="40" ... aria-hidden="true">
```

3箇所（業務システム開発・ツール・Webシステム・保守・運用サポートの各カード）に追加すること。

---

### ④ 要素間マージン強化

**判定：承認**

`.team-body { margin: 0 0 28px }` / `.team-list { line-height: 2.2 }` / `.pricing-box { margin-top: 36px }` がそれぞれ反映されている。

---

### ⑤ pricing-box 視覚的差別化

**判定：承認**

`background: #eef3fb` + `border-left: 4px solid #0a4f9f` + `border-radius: 0 12px 12px 0` の組み合わせにより、サービスカード（`background: #fff` + `border-radius: 20px` + shadow）と明確に差別化されている。h3 の `text-transform: uppercase; letter-spacing: 0.08em` によるラベル表現も意図通り。

---

## 実装担当からのPM確認事項への回答

**確認事項1（`.section-inner` への padding 移動）：承認**  
`.page` 依存から `.section-inner` への移行は、将来的なフル幅セクション実装のための適切な構造改善。副作用なし。

**確認事項2（border-radius: 0 でhero-stats境界が直線になること）：確認済み**  
コード上の問題なし。本番公開時にブラウザで外観を目視確認する。

---

## 要修正タスク

| # | ファイル | 修正内容 |
|---|---------|---------|
| 1 | `site/src/pages/index.astro` | 3つのサービスカードSVGに `aria-hidden="true"` を追加 |

---

## Sprint 3 クローズ条件

上記の `aria-hidden="true"` 追加が完了した時点で、**Sprint 3 クローズ**とする。  
修正は軽微なため、別途レビューは不要。実装担当が対応後、progress.md を「完了」に更新すること。

---

## Sprint 4 GO

Sprint 3 クローズをもって Sprint 4 を開始する。  
Sprint 4 ブリーフィングは `docs/sprint/sprint-04/briefing.md` を参照。
