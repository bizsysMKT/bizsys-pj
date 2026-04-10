# Sprint 4 Report

> 作成者：実装担当  
> 作成日：2026-04-06  
> ステータス：完了

---

## 1. 実装した変更の概要

### A. 共通CSS集約（Layout.astro）

`Layout.astro` に `<style is:global>` を導入し、全ページ共通のクラスを集約した。

**移動・追加したクラス：**
- ベーススタイル（`body`, `*`, `.page`）
- ヘッダー・フッター（`site-header`, `site-nav`, `site-footer`）
- セクション共通（`.section`, `.section-inner`, `.section-title`）
- ページヘッダー（`.page-header`, `.page-lead`）
- 背景ユーティリティ（`.bg-white`, `.bg-light`, `.bg-tint`）
- CTAボタン（`.btn-primary`, `.btn-secondary`, `.cta-group`）
- カード（`.card`, `.card-grid`, `.card-icon`）
- フォームフィールド（`.form-group`, `.form-group input/textarea`, `.form-submit`）
- ブログ（`.blog-list`, `.blog-item`, `.blog-article`, `.prose`）
- レスポンシブ（900px / 480px）

**index.astro に残したクラス（ページ固有）：**  
`.hero` 系, `.stats`/`.stat`, `.cases-grid`/`.case-card`, `.faq-grid`/`.faq-card`, `.pricing-box`, `.cta-block`

---

### B. 5ページへのデザイン適用

| ページ | 実装内容 |
|-------|---------|
| `services.astro` | ページヘッダー → SVGアイコン付き3カード → 料金3カード → CTA |
| `cases.astro` | ページヘッダー → 8事例カード（4列グリッド）→ 共通ポイント3カード → CTA |
| `faq.astro` | ページヘッダー → FAQ 5問（3列グリッド、5問目全幅）→ CTA |
| `about.astro` | ページヘッダー → チーム紹介 → 実績数字6項目 → 強み3カード → CTA |
| `tools.astro` | ページヘッダー → ツール実績リスト → ツール3カード → CTA |

全ページで `page-header` → `bg-white` / `bg-light` の交互背景を適用。

---

### C. contact.astro 完成

**追加フィールド：**

| フィールド | 種類 | 必須 |
|-----------|------|------|
| お名前 | text | 必須（バッジ表示） |
| 会社名 / 団体名 | text | 任意（バッジ表示） |
| メールアドレス | email | 必須 |
| お問い合わせ内容 | textarea | 必須 |
| 相談希望日 / 備考 | textarea | 任意 |

- フォーム action: `https://formspree.io/f/yourFormId`（プレースホルダー維持）
- HTMLコメントで「漢那さんの Formspree ID に差し替えてください」を明記
- 必須/任意バッジを視覚的に区別（ネイビー/グレー）
- 説明ボックスに「文字ベース・電話不要・1日以内回答」を記載

---

### D. ブログ関連ページ（最低限対応）

- `blog/index.astro`：ページヘッダー + `.blog-list` / `.blog-item` でカード形式の記事一覧
- `blog/[slug].astro`：ページヘッダー + `.blog-article` / `.prose` で読みやすい記事ページ。パンくず・CTAボタン追加

---

### ビルド確認

`astro build` 完了、エラーなし（9ページ全て生成）。

---

## 2. 判断内容・PM確認事項

| 判断 | 内容 |
|------|------|
| `cases.astro`・`faq.astro` のグリッドCSS | briefing では「index.astro のクラスを流用」とあるが、`is:global` で Layout に移動したクラスとは別に、各ページの `<style>` タグで定義した。Layout に移動すると全ページで同名クラスが干渉するリスクがあるため、ページ固有として管理する方針とした |
| `services.astro` の料金セクション | briefing の「料金ボックス」指定に対し、index.astro の `pricing-box`（左ボーダーアクセント）ではなくカードグリッドで実装した。サービスページでは料金が主要コンテンツであり「補足情報」として扱う必要がないと判断 |
| `blog/[slug].astro` パンくず追加 | briefing に明示なしだが、ブログから記事への回遊性向上のため追加した |

---

## 3. 公開前チェックリスト（未設定項目）

以下は漢那さん側での設定が必要です。Sprint 4 での実装対象外です。

| 項目 | 場所 | 対応方法 |
|------|------|---------|
| **Formspree ID** | `site/src/pages/contact.astro` 6行目 `action="https://formspree.io/f/yourFormId"` の `yourFormId` | Formspree（formspree.io）にアカウント登録後、フォームIDを取得して差し替える |
| **GA4 トラッキングコード** | `site/src/components/Layout.astro` の `<head>` | GA4 でプロパティ作成後、測定IDを取得して `<script>` タグを追加する |
| **Google Search Console 認証ファイル** | `site/public/` に配置 | Search Console でサイト登録後、HTMLファイルをダウンロードして `public/` に配置し、ビルド・デプロイする |
