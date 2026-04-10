# Sprint 5 Briefing

> 作成者：PM  
> 作成日：2026-04-09  
> 担当：実装担当  
> 前提条件：Sprint 4 完了済み（全ページ実装・astro build OK）  
> ステータス：**GO**

---

## このスプリントの目的

サイトを GitHub Pages で公開できる状態にする。
計測（GA4）・問い合わせ受信（Formspree）・検索インデックス（Search Console）の3つを有効化し、漢那さんが実際に運用を開始できる状態にする。

---

## 作業スコープ

### A. Formspree ID の差し替え

`site/src/pages/contact.astro` の Formspree エンドポイントを確定値に変更する。

| 項目 | 値 |
|------|-----|
| 変更前 | `https://formspree.io/f/yourFormId` |
| 変更後 | `https://formspree.io/f/maqllrnj` |

コメント（「漢那さんの Formspree ID に差し替えてください」）は削除すること。

---

### B. GA4 トラッキングコードの組み込み

`site/src/components/Layout.astro` の `<head>` に GA4 スクリプトを追加する。

| 項目 | 値 |
|------|-----|
| GA4 測定 ID | `G-04S9SZW07N` |

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-04S9SZW07N"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-04S9SZW07N');
</script>
```

`<head>` 内、`<title>` タグの直後に追加すること。

---

### C. GitHub Pages 公開設定

#### C-1. `astro.config.mjs` の更新

GitHub Pages 用に `site` と `base` を設定する。

| 項目 | 値 |
|------|-----|
| 公開ドメイン | `https://bizsys.jp`（カスタムドメイン） |
| `site` | `https://bizsys.jp` |
| `base` | `/`（カスタムドメインのため、サブパス不要） |

#### C-2. `site/public/CNAME` ファイルの作成

GitHub Pages カスタムドメイン設定用に CNAME ファイルを作成する。

```
bizsys.jp
```

#### C-3. GitHub Actions デプロイワークフローの作成

`.github/workflows/deploy.yml` を作成する。

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: site/package-lock.json
      - run: npm ci
        working-directory: site
      - run: npm run build
        working-directory: site
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

**注意：** `.github/` ディレクトリはプロジェクトルート（`c:/Dev/bizsys-pj/`）直下に作成すること。`site/` の中ではない。

---

### D. Google Search Console（GA4 連携方式）

コード対応は不要。Search Console の設定は漢那さんが以下の手順で行う：

1. [Google Search Console](https://search.google.com/search-console) にアクセス
2. 「プロパティを追加」→ URL プレフィックス → `https://bizsys.jp` を入力
3. 確認方法で「Google アナリティクス」を選択
4. GA4 が設定済みであれば自動認証される

この手順を `docs/handover.md` に記載すること（E を参照）。

---

### E. handover.md の作成

`docs/handover.md` を作成し、漢那さんが独立して運用を開始するために必要な情報をまとめる。

記載する内容：

1. **サイト概要**：URL・技術構成・ディレクトリ構成の説明
2. **更新手順**：記事追加・LP文言修正の手順
3. **デプロイ手順**：`git push` → 自動デプロイの流れ
4. **各種サービスアカウント**：Formspree・GA4・Search Console のログイン先とダッシュボードの見方
5. **Search Console の初回設定手順**（上記 D の手順）
6. **トラブル対応**：よくある問題と対処法

---

## 完了基準

- [ ] `contact.astro` の Formspree エンドポイントが `maqllrnj` に変更されている
- [ ] `Layout.astro` に GA4 スクリプトが追加されている
- [ ] `astro.config.mjs` に `site: 'https://bizsys.jp'` が設定されている
- [ ] `site/public/CNAME` に `bizsys.jp` が記載されている
- [ ] `.github/workflows/deploy.yml` が作成されている
- [ ] `astro build` でエラーが出ない
- [ ] `docs/handover.md` が作成されている

---

## 完了後の作業

`docs/sprint/sprint-05/report.md` を作成し、以下を記載すること：

1. A〜E 各作業の完了確認
2. PM・漢那さんへの確認事項（あれば）
3. GitHub リポジトリへのプッシュ前に漢那さんに確認が必要な事項
