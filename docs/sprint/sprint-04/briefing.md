# Sprint 4 Briefing

> 作成者：PM  
> 作成日：2026-04-05  
> 担当：実装担当  
> 前提条件：Sprint 3 完了済み（index.astro のリッチデザイン確立後）  
> ステータス：**GO（2026-04-06 Sprint 3 クローズ確認済み）**

---

## このスプリントの目的

Sprint 3 で確立した `index.astro` のデザインシステムを全ページに横展開し、  
公開可能な状態（GitHub Pages デプロイ準備完了）にする。

---

## 作業スコープ

### A. 共通 CSS の集約（最初に対応）

Sprint 3 の `index.astro` から共通クラスを `Layout.astro` のグローバル `<style>` に移動する。

**Layout.astro へ移動するクラス（共通利用）：**
- `.btn-primary`, `.btn-secondary`, `.cta-group`
- `.card`, `.card-grid`, `.card-icon`, `.card--accent-left`
- `.section-title`, `.section-header`, `.section-eyebrow`
- `.bg-white`, `.bg-light`, `.bg-tint`
- `.full-bleed` ユーティリティ

**index.astro に残すクラス（ページ固有）：**
- `.hero`, `.hero-eyebrow`, `.hero-lead`, `.hero-card`, `.hero-keyword`
- `.stats`, `.stat`, `.stat-icon`
- `.cases-grid`, `.case-card`
- `.faq-grid`, `.faq-card`
- `.pricing-box`, `.cta-block`

---

### B. 残り5ページへのデザイン適用

Sprint 3 で確立したデザインを以下の5ページに適用する。  
コンテンツは `docs/lp-content.md` セクション3.2〜3.5, 3.8 を参照して実装すること。

#### B-1：`services.astro`（サービス内容）
- セクション：ページヘッダー → サービス3カード（アイコン＋左ボーダー） → 料金ボックス → CTA
- 背景：`bg-white` / `bg-light` の交互

#### B-2：`cases.astro`（開発事例）
- セクション：ページヘッダー → 事例8カード（4列グリッド） → CTA
- `index.astro` の `.cases-grid` / `.case-card` を流用

#### B-3：`faq.astro`（よくある質問）
- セクション：ページヘッダー → FAQ 5問カード（3列、最終カード全幅） → CTA
- `index.astro` の `.faq-grid` / `.faq-card` を流用

#### B-4：`about.astro`（ビズシスとは）
- セクション：ページヘッダー → チーム紹介 → 実績数字（6項目）→ 強み3点 → CTA
- `index.astro` の `.stats` / `.stat` を流用

#### B-5：`tools.astro`（ツール実績）
- セクション：ページヘッダー → ツール3種（カード）→ 説明文 → CTA

---

### C. `contact.astro` の完成

**C-1：フォーム項目の追加**

`lp-content.md` セクション3.7 に基づき、以下を追加：

| フィールド | 種類 | 必須 |
|-----------|------|------|
| お名前 | text | 必須（既存） |
| 会社名 / 団体名 | text | 任意 |
| メールアドレス | email | 必須（既存） |
| お問い合わせ内容 | textarea | 必須（既存） |
| 相談希望日 / 備考 | textarea | 任意 |

**C-2：ページ文言**（`lp-content.md` セクション3.7 の確定テキストを使用）

- ページタイトル：「まずは、現状と課題をお聞かせください」
- 説明文：文字ベース・電話不要・1日以内回答

**C-3：Formspree ID**

`action="https://formspree.io/f/yourFormId"` のプレースホルダーは維持。  
コメントで「漢那さんの Formspree ID に差し替えてください」と記載すること。

**C-4：スタイリング**

index.astro と統一感のあるデザインを適用。

---

### D. ブログ関連ページの最低限対応

`blog/index.astro` と `blog/[slug].astro` は Sprint 4 に含めるが、  
スタイリングは「読める・使えるレベル」に留める（Sprint 3 水準への完全準拠は Sprint 5 以降）。

---

## 完了基準

- [ ] 共通 CSS が Layout.astro に集約されており、各ページで重複定義がない
- [ ] `services`, `cases`, `faq`, `about`, `tools` の5ページにコンテンツとスタイルが適用されている
- [ ] 全ページでナビ・フッター・フォントが統一されている
- [ ] `contact.astro` に全フォーム項目が揃っている
- [ ] `contact.astro` のデザインが他ページと統一されている
- [ ] `blog/index.astro` が最低限読める状態になっている
- [ ] `astro build` でエラーが出ない（9ページすべて生成）
- [ ] 全7ページを `localhost:4321` で確認し、デザインの統一感がある

---

## 完了後の作業

完了したら `docs/sprint/sprint-04/report.md` を作成し、以下を記載する：

1. 実装した変更の概要（ページごと）
2. 判断内容・PM 確認事項（あれば）
3. **公開前チェックリスト**（以下が未設定であることを明記）
   - Formspree ID（漢那さんのアカウントから取得が必要）
   - GA4 トラッキングコード
   - Google Search Console 認証ファイル

---

## 注意事項

- `input/` 以下は読み取り専用
- Formspree ID・GA4 トラッキングコードはこのスプリントでは設定しない（プレースホルダー維持）
- Sprint 3 で確立したデザインを「コピー & 調整」する形で横展開すること（ゼロから設計しない）

---

## 実装担当への補足指示（設計仕様書に未定義の2パターン）

以下2点は `design-template-1-guidelines.md` に明示仕様がない。指定する構造に従って実装すること。

### 補足①：サブページ用ページヘッダー

B-1〜B-5 の各ページ冒頭に共通で使用するヘッダーセクション。

**構造：**
```
背景：#f5f8ff（ライトセクションと同色）
パディング：padding: 48px 0 40px
内容：ページタイトル（h1）+ 1行のリード文（p）
```

**CSS：**
```css
.page-header { background: #f5f8ff; }
.page-header h1 {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  margin: 0 0 12px;
}
.page-header .page-lead {
  font-size: 1rem;
  color: #555;
  margin: 0;
  line-height: 1.75;
}
```

**HTML構造（各ページ共通）：**
```html
<section class="section page-header">
  <div class="section-inner">
    <h1>ページタイトル</h1>
    <p class="page-lead">リード文1行</p>
  </div>
</section>
```

各ページのタイトル・リード文は `docs/lp-content.md` の該当セクションを参照すること。

---

### 補足②：contact.astro フォームフィールドのスタイル

**CSS：**
```css
.form-group { margin-bottom: 24px; }
.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1.5px solid #cdd6e8;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  color: #111;
  background: #fff;
  transition: border-color 0.15s ease;
  box-sizing: border-box;
}
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0a4f9f;
}
.form-group textarea { resize: vertical; min-height: 120px; }
.form-submit { margin-top: 8px; }
```

送信ボタンは既存の `.btn-primary` を使用すること。
