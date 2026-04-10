# デザイン方針ガイドライン：案1（`docs/design-template-1.html`）

> **このファイルの役割**：「どう見せるか」を定義するデザイン仕様書。色・フォント・余白・CTAの見た目・レイアウトルールを管理する。テキスト内容・ターゲット定義は `docs/lp-content.md` を参照。

---

## 改訂履歴

| バージョン | 日付 | 変更概要 |
|-----------|------|---------|
| v1.0 | Sprint 0〜2 | 初版（シンプル・クリーン） |
| v2.0 | Sprint 3 | 依頼者フィードバック「リッチにしてほしい」を受け、全面改訂 |
| v2.1 | Sprint 3 | PMレビュー対応：stats ダーク化廃止・グラスモーフィズム廃止 |
| v3.0 | Sprint 3 | 実装レビュー差し戻し対応：①ヒーローレイアウト再設計・②border-radius 廃止・③サービスカードアイコン仕様追加 |

---

## 目的

このドキュメントは、実装担当が案1のLPデザインをそのまま理解・再現できるよう、方針・構成・表現ルールを明確にまとめたものです。

- 実装担当が `site/src/pages/index.astro` を修正する際、何をどう変えるかが明確にわかる状態にする
- `docs/lp-content.md` と整合させ、コンテンツ仕様との齟齬を生じさせない
- Sprint 2 で確立済みの仕様と、Sprint 3 で変更する仕様を明確に区別して記載する

---

## ターゲット像と訴求軸

→ `docs/lp-content.md` セクション1（LPコンテンツの基本方針）参照。ターゲット定義・メイン訴求軸はコンテンツ仕様書で管理する。

---

## Sprint 2 で確立済みの仕様（変更しない）

以下は Sprint 2 実装で動作確認済みのため、Sprint 3 では変更しない。

| 項目 | 確定仕様 |
|------|---------|
| ページ構成・セクション順序 | hero → stats → team → services → cases → tools → faq → contact-cta |
| 全CTAリンク先 | メインCTA `href="/contact"`、事例は `href="/cases"` に統一済み |
| レスポンシブ対応のブレークポイント | 900px（カラム崩し）、480px（縦並び） |
| ナビゲーション文字列 | 日本語（サービス・事例・FAQ・お問い合わせ）で確定 |
| コンテンツテキスト | `docs/lp-content.md` の確定テキストを使用。Sprint 3 では変更しない |

---

## Sprint 3 デザイン改善方針

### 改善の背景と方針

依頼者より「もっとリッチにしてほしい」とのフィードバックがあった。参考サイト（https://www.co-assign.com/campaign-1/）の分析結果と、ビズシスのブランド制約（信頼感・誠実さ・専門性）を踏まえ、以下の方針で改善する。

**リッチ感の差がどこから来ているかの分析：**

1. **ヒーロー背景が白のみ** → 視覚的なインパクトが最も弱い部分
2. **全セクションが単調な白/淡いグレー** → 奥行き・立体感がない
3. **フォントに変化がない** → 見出しの格・重厚感が出ていない
4. **カード・ボタンが静的** → インタラクションのフィードバックがない
5. **実績数字セクションが弱い** → 信頼性の訴求が視覚的に弱い

**ビズシスブランドに合わせた取り込み範囲：**

- 取り入れる：ヒーロー背景のダーク化・グラデーション、フォント強化、セクション背景の交互切り替え、カード/ボタンのホバー効果、実績数字のサイズ・ウェイト強化（※実績セクション背景はダーク化せず白を維持。PMレビューにより変更）
- 取り入れない：Serif系フォント（中小企業の社長に馴染まない）、大きな画像ビジュアル（実装制約）、過度なアニメーション（信頼感を損なうリスク）、SaaSらしいUI（業種が違う）

---

## 色・トーン（v2.0）

### カラーパレット

| 用途 | 色値 | 説明 |
|------|------|------|
| ブランドネイビー | `#0a4f9f` | キーカラー。Sprint 2 から継続 |
| ダークネイビー | `#061e3f` | ヒーロー背景・ダークセクション用 |
| ブライトブルー | `#1a6fd4` | グラデーション終端・アクセント |
| ベース白 | `#ffffff` | カード背景・本文エリア |
| ライトセクション | `#f5f8ff` | 淡いブルーグレー。偶数セクション背景 |
| テキスト黒 | `#111111` | 見出しテキスト |
| テキストグレー | `#444444` | 本文テキスト |
| サブテキスト | `#666666` | ラベル・補足テキスト |

### トーン

- 清潔感・信頼感・専門性を軸とする。Sprint 2 から継続
- ヒーローのみダーク背景を使い、LPの冒頭にインパクトを集中させる（実績セクションは白。PMレビューで変更済み）
- 全体をダークにはせず、白基調を維持する（ターゲット：中小企業の社長に合わせる）

---

## フォント（v2.0）

### 変更内容

Sprint 2 はシステムフォントのみだったが、見出しの格と重厚感を高めるために Google Fonts を導入する。

### 指定方法

`Layout.astro` の `<head>` に以下を追加する：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
```

### フォントスタック

```css
font-family: 'Noto Sans JP', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### タイポグラフィルール

| 要素 | font-size | font-weight | 備考 |
|------|-----------|-------------|------|
| `hero h1` | `3.5rem`（SP: `2.2rem`） | `900` | v3.0 で変更。フル幅レイアウト時の視覚的重量感を確保 |
| `.section-title` | `1.8rem`（SP: `1.4rem`） | `700` | Sprint 2 は `1.6rem` だった |
| ヒーロー本文 | `1.1rem` | `400` | line-height: `1.9` |
| カード見出し | `1.1rem` | `700` | Sprint 2 から継続 |

---

## ヒーロー（v3.0）

### 変更概要

- v2.0：白背景 → ダークグラデーション背景に変更（PMレビュー承認済み）
- **v3.0（今回）**：`1fr 1fr` の2カラム構成でパンチラインが折れる問題を解消するため、レイアウト構造を3ゾーン構成に変更。`border-radius` の非対称・過大問題を解消するため `border-radius: 0`（フラット）に変更。

---

### ① レイアウト構造（v3.0 変更）

**問題**：`grid-template-columns: 1fr 1fr` の左カラム幅（約560px）に `font-size: 3.5rem / font-weight: 900` の見出し（22文字）を置くと折れ曲がり、最重要メッセージの可読性が損なわれる。

**採用する構造：3ゾーン構成**

```
┌─────────────────────────────────────────┐
│  [eyebrow]                               │
│  [h1 — フル幅 1行]                       │  ← .hero-top
├──────────────────────┬──────────────────┤
│  [lead文・CTAボタン]  │  [課題共感カード] │  ← .hero-bottom（2カラム）
└──────────────────────┴──────────────────┘
```

h1 をフル幅の上段（`.hero-top`）に置くことで、パンチラインがデスクトップ幅で1行に収まる。リード文とカードは下段（`.hero-bottom`）に2カラムで配置する。

**HTML構造（index.astro の変更箇所）**

```html
<section class="hero" id="hero">
  <!-- 上段：パンチライン（フル幅） -->
  <div class="hero-top">
    <p class="hero-eyebrow">現場のExcel管理に、終止符を。</p>
    <h1>そのExcel管理、そろそろ限界じゃないですか？</h1>
  </div>
  <!-- 下段：リード文＋カード（2カラム） -->
  <div class="hero-bottom">
    <div class="hero-body">
      <p class="hero-lead">
        ビズシスは、業務システム開発・保守に特化した少数精鋭チームです。<br />
        Excelの限界を解消し、現場業務を自動化して、運用負担を軽減します。
      </p>
      <div class="cta-group">
        <a class="btn-primary" href="/contact">まずは相談する</a>
        <a class="btn-secondary" href="/cases">導入事例を見る</a>
      </div>
    </div>
    <div class="hero-card">
      <h2>Excel管理は見えないコストを生む</h2>
      <ul>
        <li>入力ミスによるデータ不整合</li>
        <li>バージョン管理の混乱</li>
        <li>集計作業の二度手間</li>
        <li>担当者依存による属人化</li>
      </ul>
    </div>
  </div>
</section>
```

**CSS（追加・変更箇所）**

```css
/* 上段：パンチライン（フル幅） */
.hero-top {
  margin-bottom: 40px;
}

/* 下段：2カラム */
.hero-bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: center;
}

/* v2.0 の .hero の grid 指定を削除し、以下に変更 */
.hero {
  background: linear-gradient(135deg, #061e3f 0%, #0a4f9f 60%, #1a6fd4 100%);
  padding: 72px 0 64px;
  /* border-radius: 削除（下記②参照） */
}

/* レスポンシブ */
@media (max-width: 900px) {
  .hero { padding: 48px 0 40px; }
  .hero-bottom { grid-template-columns: 1fr; }
}
```

**削除するCSS**：v2.0 の `.hero { display: grid; grid-template-columns: 1fr 1fr; ... }` は削除し、上記に置き換える。

---

### ② border-radius（v3.0 変更）

**問題**：`border-radius: 0 0 32px 32px`（上辺直角・下辺32px）は視覚的に非対称で不安定な印象を生む。また32pxのアールはブランド方針「信頼感・専門性」に対して柔らかすぎる。

**採用する方針：border-radius: 0（フラット）**

```css
.hero {
  border-radius: 0;
}
```

**判断根拠**：中小企業の社長（40〜60代）は、角丸の大きいデザインを「カジュアル・信頼感が薄い」と感じやすい。フラットな矩形は金融・専門サービス・B2B領域で標準的な「誠実・安定」の視覚言語。非対称アール（上0・下32）を廃止し上下を統一することで、安定感も同時に確保する。

---

### テキスト色（v2.0 から継続）

ヒーロー内のすべてのテキストを白系に変更する：

```css
.hero h1 { color: #ffffff; }
.hero-lead { color: rgba(255, 255, 255, 0.85); }
.hero-eyebrow {
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 4px 12px;
  border-radius: 999px;
  display: inline-block;
  font-size: 0.85rem;
}
```

---

### ヒーローカード（v2.1 から継続）

グラスモーフィズムは廃止済み（PMレビュー対応済み）。白不透明カード＋強めのシャドウを使用する。

```css
.hero-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.25);
}
.hero-card h2 { color: #111; margin: 0 0 16px; font-size: 1.15rem; }
.hero-card ul { color: #444; padding-left: 20px; line-height: 2.1; margin: 0; }
```

---

### CTAボタン（ヒーロー内）（v2.0 から継続）

```css
/* ヒーロー内メインCTA */
.hero .btn-primary {
  background: #ffffff;
  color: #0a4f9f;
}
.hero .btn-primary:hover { background: #e8f0fb; }

/* ヒーロー内セカンダリCTA */
.hero .btn-secondary {
  background: transparent;
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.6);
}
.hero .btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }
```

---

## 実績セクション（stats）（v2.1）

### 変更概要

Sprint 2 は白カード。**v2.0 ではダーク背景を検討したが、hero に続いてダークが連続すると圧迫感が生じるため、PMレビューにより白背景に変更**。ヒーローのダーク → stats の白という「開放感の切り替え」でリズムを作る。数字の力強さはサイズ・太さ・色で表現する。

### 背景

stats セクションは `#ffffff`（白）。背景CSS の追加変更は不要。

### 実績カードCSS

```css
.stat {
  background: #fff;
  padding: 28px 20px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(10, 79, 159, 0.08);
  text-align: center;
}
.stat strong {
  display: block;
  font-size: 2.2rem;
  color: #0a4f9f;
  font-weight: 900;
  margin-bottom: 6px;
}
.stat span { font-size: 0.85rem; color: #666; }
```

**Sprint 2 との差分**：`font-size` を `1.8rem → 2.2rem`、`font-weight` を既存値 → `900` に強化。数字の視覚的な力強さをサイズとウェイトで確保する。

---

## セクション背景の交互切り替え（v2.0）

### 変更概要

Sprint 2 は全セクションが白/淡いグレーで単調。Sprint 3 では背景を交互に変えて奥行きを出す。

### 各セクションの背景

| セクション | 背景色 | 理由 |
|-----------|--------|------|
| hero | `linear-gradient(135deg, #061e3f, #1a6fd4)` | インパクト重視。ダーク |
| stats | `#ffffff` | 白。heroダークからの「開放感」を演出。PMレビューにより変更 |
| team | `#ffffff` | 白。読みやすさ重視 |
| services | `#f5f8ff` | 淡いブルーグレー |
| cases | `#ffffff` | 白 |
| tools | `#f5f8ff` | 淡いブルーグレー |
| faq | `#ffffff` | 白 |
| contact-cta | `#0a4f9f`（Sprint 2 から継続） | 最終CTAで締める |

### 実装方法

各 `<section>` に `style="background: ..."` を直接指定するか、セクション固有のクラスを追加して CSS で管理する。

---

## カードのホバー効果（v2.0）

### 変更概要

Sprint 2 はホバー効果なし。Sprint 3 では浮き上がりアニメーションを追加する。

### CSS

```css
.card, .case-card, .faq-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: default;
}
.card:hover, .case-card:hover, .faq-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 48px rgba(10, 79, 159, 0.15);
}
```

---

## サービスカード：アイコン仕様（v3.0）

### 変更概要

Sprint 2〜v2.1 はサービスカードにアイコンなし（見出し＋本文テキストのみ）。v3.0 で各カードにインラインSVGアイコンを追加し、「何をしてくれる会社か」を視覚的に補強する。

**制約**：`.png` / `.jpg` は使用不可。インラインSVGで実装する（絵文字はフォント環境によって見た目が変わるため不採用）。

---

### アイコン配置仕様

- **位置**：カード内の `<h3>` の上（カードコンテンツ最上部）
- **サイズ**：`width="40" height="40"`（2.5rem 相当）
- **色**：ブランドネイビー `#0a4f9f`（stroke色で統一）
- **マージン**：`margin-bottom: 16px; display: block;`
- **背景**：なし（透明。カード背景白に直接置く）

---

### 3サービスのアイコン仕様

#### 1. 業務システム開発

**表現すべき価値**：効率化・時間短縮・「Excel管理からの脱却」  
**アイコン**：モニター画面＋チェックマーク（「システムで課題が解決された」状態を示す）

```html
<!-- index.astro の「業務システム開発」カード内 h3 の直前に挿入 -->
<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin-bottom:16px;" aria-hidden="true">
  <rect x="4" y="6" width="32" height="22" rx="3" stroke="#0a4f9f" stroke-width="2.5"/>
  <path d="M14 34h12M20 28v6" stroke="#0a4f9f" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M13 18l4.5 4.5 9-9" stroke="#0a4f9f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

#### 2. ツール・Webシステム開発

**表現すべき価値**：手作業削減・自動化・データ連携  
**アイコン**：歯車（自動化・仕組み化を直感的に示す）

```html
<!-- index.astro の「ツール・Webシステム開発」カード内 h3 の直前に挿入 -->
<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin-bottom:16px;" aria-hidden="true">
  <circle cx="20" cy="20" r="5.5" stroke="#0a4f9f" stroke-width="2.5"/>
  <path d="M20 6v4M20 30v4M6 20h4M30 20h4M10.1 10.1l2.8 2.8M27.1 27.1l2.8 2.8M10.1 29.9l2.8-2.8M27.1 12.9l2.8-2.8" stroke="#0a4f9f" stroke-width="2.5" stroke-linecap="round"/>
</svg>
```

---

#### 3. 保守・運用サポート

**表現すべき価値**：安心・継続性・長期的なパートナーシップ  
**アイコン**：シールド＋チェックマーク（「守られている・任せられる」安心感を示す）

```html
<!-- index.astro の「保守・運用サポート」カード内 h3 の直前に挿入 -->
<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin-bottom:16px;" aria-hidden="true">
  <path d="M20 4L6 10v11c0 8.3 14 15 14 15s14-6.7 14-15V10L20 4z" stroke="#0a4f9f" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M14 20.5l4 4 8-8" stroke="#0a4f9f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

### 実装上の注意点

- `aria-hidden="true"` を必ず付与する（スクリーンリーダーへの重複読み上げを防ぐ。意味はテキストで十分に伝わる）
- SVG の `style` 属性で `display:block; margin-bottom:16px;` を直接指定する（CSSクラスの追加が不要なため）
- カードの `padding` は Sprint 2 の `28px` を維持する（アイコン分の余白は上記 margin-bottom で確保）

---

## CTAボタン（グローバル）（v2.0）

### 変更概要

Sprint 2 は単色フラットボタン。Sprint 3 ではグラデーション＋シャドウを追加してリッチ感を出す。

### CSS

```css
.btn-primary {
  background: linear-gradient(135deg, #0a4f9f, #1a6fd4);
  box-shadow: 0 8px 20px rgba(10, 79, 159, 0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.btn-primary:hover {
  background: linear-gradient(135deg, #083d7a, #0a4f9f);
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(10, 79, 159, 0.45);
}
.btn-secondary {
  transition: background 0.15s ease, transform 0.15s ease;
}
.btn-secondary:hover {
  transform: translateY(-2px);
}
```

**注意**：ヒーロー内・CTA ブロック内のボタンは「ヒーロー」セクション仕様を優先する（上記参照）。

---

## セクションタイトルの装飾（v2.0）

### 変更概要

Sprint 2 はテキストのみ。Sprint 3 では左側にアクセントバーを追加して見出しに格を持たせる。

### CSS

```css
.section-title {
  position: relative;
  padding-left: 20px;
}
.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.1em;
  bottom: 0.1em;
  width: 5px;
  border-radius: 3px;
  background: linear-gradient(180deg, #1a6fd4, #0a4f9f);
}
```

---

## ページ構成と各セクションの役割（変更なし）

以下は Sprint 2 から変更なし。構成・役割はそのまま維持する。

### ヘッダー
- 日本語ナビゲーションで構成
- ナビ項目は `サービス`, `事例`, `FAQ`, `お問い合わせ`
- クリックしやすいシンプルなテキストリンク

### ヒーロー
- 見出し：→ `docs/lp-content.md` 3.1参照（確定テキストはコンテンツ仕様書で管理）
- サブコピー：現場のExcel管理課題を共感し、解決へ誘導する
- CTA：「まずは相談する」を最優先に、`/contact` へ誘導
- サブCTA：「導入事例を見る」など関連ページ遷移
- サイドカードは「課題の共感＋次の一手」型にする

### 実績セクション
- 主要実績：14年 / ★5.0 / 550件 / 25社以上 / 89社以上 / 10社以上（6項目、Sprint 2 実装済み）

### サービス紹介
- 主要3サービスをカード形式で提示（Sprint 2 から継続）

### 事例セクション
- 業種ベースの現場事例8件をカード形式で掲載（Sprint 2 から継続）

### FAQセクション
- 5問のQ&Aをカード形式で掲載（Sprint 2 から継続）

### Contactセクション
- ネイビー背景の最終CTAブロック（Sprint 2 から継続）

---

## Astroテンプレート選定方針

- デザイン方向性：シンプル・クリーン・信頼感をベースに、ヒーローと実績セクションで「リッチ感」を演出
- 選定基準：余白がある・タイポグラフィが明瞭・CTAが目立つ・実績バッジが配置しやすい

---

## 実装注意点と優先度（v3.0）

### 優先度高（必ず実装）

1. **Noto Sans JP の導入**：`Layout.astro` の `<head>` に Google Fonts リンクを追加し、全体に適用
2. **ヒーロー HTML 構造の変更**：v3.0 の3ゾーン構成（`.hero-top` + `.hero-bottom`）に書き換える。v2.0 の `1fr 1fr` グリッドは `.hero-bottom` に移動する
3. **ヒーロー `border-radius` 廃止**：`border-radius: 0 0 32px 32px` を `border-radius: 0` に変更
4. **サービスカードへのSVGアイコン挿入**：3サービスそれぞれの `<h3>` 直前に各SVGを挿入する
5. **実績数字の強化**：`.stat strong` を `font-size: 2.2rem; font-weight: 900;` に変更（背景は白を維持）
6. **CTAボタンのグラデーション化**：グローバル `.btn-primary` に gradient + shadow を適用
7. **セクションタイトルへのアクセントバー追加**：`.section-title::before` で左ライン装飾

### 優先度中（できれば実装）

8. **セクション背景の交互切り替え**：services・tools セクションに `#f5f8ff` を適用
9. **カードのホバー効果追加**：`.card`, `.case-card`, `.faq-card` に transition + transform

### 優先度低（余裕があれば）

10. **モバイル時の hero 余白最適化**：SP時のパディングを確認・調整（`.hero-top` / `.hero-bottom` の新構造に合わせること）

---

## 実装担当への引き渡し

- このガイドを起点として、`docs/lp-content.md` と合わせて参照してください
- 現在の実装は `site/src/pages/index.astro`（Sprint 2 完了版）です
- Sprint 3 で変更する箇所は「優先度高」から順に実装してください
- LP実装後に以下を確認すること：
  - ヒーロー背景がダーク（ネイビー系グラデーション）になっているか
  - **パンチライン（h1）がデスクトップ幅で1行に収まっているか**（v3.0 最重要確認）
  - **ヒーローの下辺がフラット（`border-radius: 0`）になっているか**
  - **3つのサービスカードにSVGアイコンが表示されているか**
  - 実績数字（`.stat strong`）が `font-size: 2.2rem; font-weight: 900;` で大きく表示されているか
  - Noto Sans JP が全体に適用されているか
  - `.btn-primary` にグラデーションとシャドウが効いているか
  - モバイル（480px以下）でレイアウトが崩れていないか（`.hero-top` / `.hero-bottom` が縦積みになっているか）

---

## 参考リンク

- `docs/lp-content.md`
- `input/戦略メモ/HP素材集.md`
- `input/戦略メモ/LP・ブログ・SNS方針.md`
- 参考サイト：https://www.co-assign.com/campaign-1/
