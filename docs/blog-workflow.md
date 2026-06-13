# ブログ記事追加 — 実施手順

> ブログ記事を追加するときは**必ずこの順序**で行う。いきなり記事作成に入らない。

---

## 手順

### Step 1：GA4 + Search Console データ取得

```bash
cd c:\Dev\bizsys-pj
node automation/fetch-analytics.js
```

→ `output/analysis/YYYY-MM-data.json` が生成される

### Step 2：分析レポート作成

生成された JSON の内容を Claude Code に貼り付け、`docs/monthly-analysis.md` の分析プロンプトテンプレートで分析させる。

レポートは `output/analysis/YYYY-MM-report.md` に保存する。

### Step 3：来月追加すべき記事テーマを確認

レポートの「来月に追加すべき記事テーマ」セクションをもとにテーマを決定する。

### Step 4：ブログ記事を作成・push

記事の書き方は `docs/article-generation.md` を参照。

```bash
git add site/src/content/blog/（ファイル名）
git commit -m "feat: ブログ記事を追加 — タイトル"
git push origin main
```

push 後、GitHub Actions が自動デプロイ＋X 自動投稿まで実行される。
