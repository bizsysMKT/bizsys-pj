# ドメイン名誤記一括修正タスク

> 作成者：PM  
> 作成日：2026-04-10  
> 担当：実装担当  
> 優先度：**高（コードに誤りあり）**

---

## 背景

正しいドメインは `bizsys.jp` だが、全ファイルに `biz-sys.jp` と誤記されている。
コードファイル（CNAME・astro.config.mjs）の誤りは公開設定に直結するため、早急に修正して push すること。

---

## 修正対象ファイル一覧

### コードファイル（必須・push 必要）

| ファイル | 修正箇所 |
|---------|---------|
| `site/public/CNAME` | `biz-sys.jp` → `bizsys.jp` |
| `site/astro.config.mjs` | `https://biz-sys.jp` → `https://bizsys.jp` |

### ドキュメントファイル（必須・push 必要）

以下のファイルすべてで `biz-sys.jp` → `bizsys.jp` に一括置換すること。

- `docs/handover.md`
- `docs/architecture.md`
- `docs/overview.md`
- `docs/operation.md`
- `docs/project_plan.md`
- `docs/phase1-report.md`
- `docs/phase1-report-draft.md`
- `docs/progress.md`
- `docs/templates/blog_template.md`
- `docs/sprint/sprint-05/briefing.md`
- `docs/sprint/sprint-05/report.md`
- `docs/sprint/sprint-05/task-handover-dns.md`

### 修正不要（読み取り専用）

- `input/` 配下の全ファイル → 触れないこと

---

## 作業手順

1. 上記ファイルの `biz-sys.jp` をすべて `bizsys.jp` に置換する
2. `astro build` でエラーがないことを確認する
3. GitHub に push する
4. GitHub Actions が正常完了（緑チェック）したことを確認する
5. 完了後 PM に報告する（report は不要、口頭で可）
