# 月次分析 実施手順書

> 対象：Yusukeさん・漢那さん  
> 更新日：2026-04-11

---

## 概要

毎月1回、前月のサイトデータ（GA4・Search Console）を自動取得し、Claude Code で分析・レポートを作成する手順書です。

**所要時間の目安：** 初回セットアップ30分 / 2回目以降は15分程度

---

## Part 1：初回のみ — 認証設定（Yusukeさん対応）

> 2回目以降はこのPartをスキップしてください。
> JSONキーファイルは使用しません。ブラウザでGoogleアカウントにサインインする方式（Application Default Credentials）を使用します。

### Step 1：Google Cloud CLI をインストールする

1. ブラウザで [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) を開く
2. Windows版インストーラーをダウンロードして実行する
3. インストール完了後、ターミナル（PowerShell or コマンドプロンプト）を**新しく開き直す**

インストール確認：
```bash
gcloud --version
```
バージョン番号が表示されればOK。

### Step 2：Google Cloud プロジェクトを作成し API を有効化する

1. ブラウザで [https://console.cloud.google.com/](https://console.cloud.google.com/) を開く
2. 右上のアカウントが `bizsys.mkt@gmail.com` であることを確認する
3. 画面上部のプロジェクト選択欄 → 「新しいプロジェクト」→ プロジェクト名 `bizsys-analytics` → 「作成」
4. 左メニュー →「APIとサービス」→「ライブラリ」
5. `Google Analytics Data API` を検索 → 「有効にする」
6. `Google Search Console API` を検索 → 「有効にする」

### Step 3：ブラウザでGoogleアカウント認証を行う

ターミナルで以下を実行する：

```bash
gcloud auth application-default login
```

ブラウザが自動的に開く。`bizsys.mkt@gmail.com` でサインインし、アクセスを許可する。

成功すると以下のように表示される：
```
Credentials saved to file: [C:\Users\...\.config\gcloud\application_default_credentials.json]
```

> この認証情報は**このPCにのみ保存**され、GitにはコミットされないためGitHub経由で漏洩しません。

### Step 4：スクリプトの設定値を修正する

[automation/fetch-analytics.js](../automation/fetch-analytics.js) を開き、以下の2か所を実際の値に変更する：

```js
const GA4_PROPERTY_ID = 'properties/XXXXXXXXX';  // ← 実際の数値IDに変更
const SEARCH_CONSOLE_SITE_URL = 'https://bizsys.jp/';  // ← 通常このままでOK
```

**GA4 プロパティIDの確認方法：**
1. [https://analytics.google.com/](https://analytics.google.com/) を開く
2. 対象プロパティを選択 →「管理」（歯車）→「プロパティ設定」
3. 画面右上に表示される数字（例：`123456789`）が プロパティID
4. `properties/123456789` の形式でファイルに記入する

### Step 5：依存パッケージのインストール（初回のみ）

```bash
cd c:\Dev\bizsys-pj
npm install
```

### Step 6：動作確認

```bash
node automation/fetch-analytics.js
```

`✓ 出力完了` が表示されれば設定完了。

---

## Part 2：毎月の実施手順（漢那さん対応）

> 毎月初旬（1〜5日を目安）に実施してください。

### Step 1：前提条件を確認する

以下のファイルが存在することを確認する：

```
c:\Dev\bizsys-pj\automation\credentials\service-account.json
```

存在しない場合は、Yusukeさんに「Part 1：初回セットアップ」の実施を依頼してください。

### Step 2：データを取得する

ターミナルで実行：

```bash
cd c:\Dev\bizsys-pj
node automation/fetch-analytics.js
```

成功すると以下のように表示される：

```
=== fetch-analytics.js 開始 ===
対象期間: 2026-04-01 〜 2026-04-30
Service Account 認証中...
GA4 データ取得中...
Search Console データ取得中...

✓ 出力完了: output/analysis/2026-04-data.json
  セッション数: 87
  ユーザー数:   62
  検索クエリ数: 18
=== 完了 ===
```

データファイルは `output/analysis/YYYY-MM-data.json` に保存される。

### Step 3：Claude Code で分析する

1. VS Code のターミナルで `claude` を起動する
2. 下記「分析プロンプトテンプレート」を**そのままコピー**して貼り付ける
3. `[　]` 内の項目のみ書き換えて送信する

---

## 分析プロンプトテンプレート

```
以下の月次データを分析し、マーケティングレポートを作成してください。

## 分析対象期間

[例：2026年4月（2026-04-01〜2026-04-30）]

## データ

以下のJSONファイルの内容を貼り付けてください：
[output/analysis/2026-04-data.json の内容をここに貼り付け]

## KPI目標値

- 月間セッション数：50以上
- 月間ユーザー数：40以上
- 目標達成判定：上記を両方達成で「達成」、片方で「一部達成」、両方未達で「未達成」

## サイト概要

- サイト名：ビズシス（https://bizsys.jp）
- ターゲット：中小企業の経営者・管理職
- コンテンツ：Excel脱却・業務改善に関するブログ記事
- X（Twitter）自動投稿：ブログ記事push時に@bizsys_xから自動投稿

## 出力してほしい内容（Markdownで）

以下の構成でレポートを作成してください：

### 1. 今月のサマリー
- セッション数・ユーザー数（目標との比較）
- KPI達成状況の評価コメント（1〜2文）

### 2. 流入チャネル分析
- organic / social / direct の内訳と比率
- 特筆すべき傾向（1〜2文）

### 3. 人気記事TOP5
- ページとPV数を一覧表示
- 人気の理由の考察（1〜2文）

### 4. 検索クエリ分析
- クリック数上位のクエリを一覧
- ユーザーが求めているテーマの読み取り（2〜3文）

### 5. 来月に追加すべき記事テーマ（3〜5件）
- 記事タイトル案と、そのテーマを選んだ理由
- 検索クエリや不人気記事の傾向を根拠にすること

### 6. 既存記事の改善候補
- titleやdescriptionの見直しが必要な記事（あれば）
- 改善案を具体的に提示すること

## 出力フォーマット

ファイルに保存できるよう、以下の形式で出力してください：

\`\`\`markdown
# 月次分析レポート：[YYYY年MM月]

> 分析日：[今日の日付]

（本文）
\`\`\`
```

---

### Step 4：レポートを保存する

1. Claude Code が生成した ` ```markdown ` ブロックの中身をコピー
2. 以下のパスに新規ファイルを作成して貼り付け・保存：
   ```
   output/analysis/YYYY-MM-report.md
   ```
   例：`output/analysis/2026-04-report.md`

### Step 5：Yusukeさんに報告する

1. [docs/sprint/current-tasks.md](sprint/current-tasks.md) を開く
2. 該当の月次分析タスクのステータスを `WAITING_APPROVAL` に更新する
3. 完了報告欄にレポートのファイルパスを記入する

例：
```
| 完了報告 | ステータス: WAITING_APPROVAL / レポート: output/analysis/2026-04-report.md |
```

---

## よくあるトラブル

| エラーメッセージ | 原因 | 対処 |
|--------------|------|------|
| `Could not load the default credentials` | `gcloud auth application-default login` が未実施 | Part 1 の Step 3 を実施する |
| `Error 403: The caller does not have permission` | GA4/Search Console のAPIが有効化されていない | Part 1 の Step 2（API有効化）を再確認 |
| `Error: Cannot find module 'googleapis'` | `npm install` が未実施 | `npm install` を実行 |
| データが0件で返ってくる | GA4 プロパティIDが誤っている | `fetch-analytics.js` 内の `GA4_PROPERTY_ID` を確認 |
| `Your application has authenticated using end user credentials` 警告 | 通常動作。問題なし | 無視してよい |
