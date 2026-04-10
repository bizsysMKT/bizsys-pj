# Sprint 5 Report

> 作成者：実装担当  
> 作成日：2026-04-09  
> ステータス：完了

---

## 1. 完了確認

### A. Formspree ID の差し替え ✅

`site/src/pages/contact.astro` の Formspree エンドポイントを変更した。

- 変更前：`https://formspree.io/f/yourFormId`
- 変更後：`https://formspree.io/f/maqllrnj`
- プレースホルダーコメント（「差し替えてください」）も同時に削除した

---

### B. GA4 トラッキングコードの組み込み ✅

`site/src/components/Layout.astro` の `<title>` タグ直後に GA4 スクリプトを追加した。

- 測定ID：`G-04S9SZW07N`
- 追加場所：`<head>` 内、`<title>` の直後
- 全9ページに自動適用される（Layout.astro 経由）

---

### C. GitHub Pages 公開設定 ✅

#### C-1. `astro.config.mjs` の更新

確認したところ、すでに正しく設定済みだった。

```js
export default defineConfig({
  site: 'https://biz-sys.jp',
  base: '/',
});
```

#### C-2. `site/public/CNAME` ファイルの作成

確認したところ、すでに `biz-sys.jp` が記載済みだった。

#### C-3. GitHub Actions デプロイワークフローの作成

`.github/workflows/deploy.yml` を新規作成した。

- トリガー：`main` ブランチへの push
- ビルド：`ubuntu-latest` + Node.js 20 + `npm ci && npm run build`
- デプロイ：`actions/deploy-pages@v4`

---

### D. Google Search Console（GA4 連携方式） ✅

コード対応なし。`docs/handover.md` の「Search Console 初回設定手順」セクションに GA4 連携方式の手順を記載した。

---

### E. handover.md の更新 ✅

既存の `docs/handover.md`（引き継ぎチェックリスト）に、Sprint 5 で求められた内容を追記した。

追加したセクション（「0. サイト概要（クイックリファレンス）」）：

- サイト URL・技術構成（Formspree ID・GA4 測定ID 含む）
- ディレクトリ構成の説明
- ブログ記事の追加手順
- LP 文言の修正方法
- デプロイ手順（git push → 自動公開）
- Search Console 初回設定手順（GA4 連携方式）
- トラブル対応表

---

### astro build 確認 ✅

```
9 page(s) built in 1.24s — Complete!
```

エラーなし。CNAME ファイルも `dist/` に含まれていることを確認。

---

## 2. 漢那さんへの確認事項

以下は漢那さん側での作業が必要です。

| 項目 | 内容 |
|------|------|
| **Formspree 通知メール** | formspree.io にログインし、フォーム `maqllrnj` の「Settings」で通知先メールアドレスが漢那さんのアドレスになっているか確認してください |
| **Search Console の初回設定** | `docs/handover.md` の「Search Console 初回設定手順」に従って、GA4 連携方式でサイトを登録してください。GA4（G-04S9SZW07N）が登録済みであれば自動認証されます |

---

## 3. GitHub リポジトリへのプッシュ前に確認が必要な事項

| 確認事項 | 内容 |
|---------|------|
| **GitHub リポジトリの存在確認** | `bizsys-pj` というリポジトリが GitHub 上に作成されているか確認してください。まだの場合は `main` ブランチで新規作成が必要です |
| **GitHub Pages の有効化** | リポジトリの「Settings」→「Pages」→ Source を「GitHub Actions」に設定してください |
| **カスタムドメインの DNS 設定** | `biz-sys.jp` の DNS に GitHub Pages の A レコード（185.199.108.153 等）を設定してください。ドメインレジストラ側での設定が必要です |
| **初回 push の権限** | push 後、GitHub Actions の「Environments」で `github-pages` 環境のデプロイを承認する必要がある場合があります |
