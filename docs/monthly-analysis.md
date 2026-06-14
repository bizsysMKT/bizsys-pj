# BizSys GA4 + Search Console 分析手順書

> 更新日：2026-06-14

---

## 概要

Pythonスクリプト1本で GA4・Search Console のデータを取得し、Claude Code で分析・HTMLレポートを出力する手順。

- **所要時間：** 5〜10分
- **必要なもの：** サービスアカウントJSON / Python / Claude Code

---

## 認証方式

サービスアカウントJSON（`google_credentials.json`）を使う方式。  
**他のPCでもJSONを置けばそのまま動く。**

| ファイル | パス |
|---------|------|
| サービスアカウントキー | `C:\Users\tk171\claude-work\google_credentials.json` |
| 分析スクリプト | `C:\Users\tk171\claude-work\work\bizsys_analytics.py` |

---

## 設定値（変更不要）

| 項目 | 値 |
|------|---|
| GA4 プロパティID | `properties/531295406` |
| Search Console サイトURL | `https://bizsys.jp/` |
| GA4 測定ID | `G-04S9SZW07N` |

---

## 起動コマンド（これだけ言えばOK）

```
gaとサーチコンソールのデータ取得して、分析結果をHTMLで出力して
```

Claude Code がスクリプト実行 → 分析 → HTML出力 → ブラウザ表示まで自動でやる。

---

## 実施手順（Claude Code が内部でやること）

### Step 1：初回のみ ── Pythonパッケージをインストール

```bash
pip install google-analytics-data google-api-python-client google-auth
```

### Step 2：分析スクリプトを実行

```bash
python -X utf8 C:\Users\tk171\claude-work\work\bizsys_analytics.py
```

ターミナルにGA4・Search Consoleのデータが表示される。

### Step 3：Claude Code で HTMLレポートを出力

表示されたデータをそのままClaudeに貼り付けて：

```
↑のデータを分析してHTMLで出力して
```

出力先：`C:\Users\tk171\claude-work\work\bizsys_analytics_report_YYYY-MM-DD.html`

---

## 他のPCで実行する場合

1. `google_credentials.json` を新しいPCの任意の場所に置く
2. スクリプト内の `CREDS_FILE` のパスを書き換える
3. Step 1〜3 を実施

```python
# bizsys_analytics.py の先頭付近
CREDS_FILE = r"C:\Users\（PCごとのパスに変更）\google_credentials.json"
```

---

## よくあるトラブル

| エラー | 原因 | 対処 |
|--------|------|------|
| `403 Permission denied` | サービスアカウントがGA4/SCに追加されていない | GA4管理画面でアカウント追加 |
| `文字化け` | PowerShellのエンコーディング問題 | `-X utf8` オプションをつけて実行 |
| `ModuleNotFoundError` | パッケージ未インストール | Step 1 を実施 |
| データが少ない・0件 | SC は3〜4日遅延あり | 正常。最新データは4日前まで |

---

## GA4 サービスアカウント権限確認

サービスアカウント：`bizsys-analytics-reader@bizsys-analytics.iam.gserviceaccount.com`

GA4管理画面 → プロパティ → プロパティのアクセス管理 → 上記アカウントが「閲覧者」以上で登録されていること。

---

## 参考：スクリプトの取得指標一覧

| 区分 | 指標 |
|------|------|
| GA4 サマリ | セッション・ユーザー・PV・直帰率・平均滞在時間（直近30日 + 前30日比較） |
| GA4 チャネル | Organic/Direct/Referral 別セッション |
| GA4 ページ | ページ別PV上位15・ランディングページ別直帰率 |
| GA4 デバイス | Desktop/Mobile/Tablet 別セッション |
| GA4 月別 | 直近90日の月別セッション推移 |
| SC サマリ | クリック・表示回数・CTR・平均順位（直近30日） |
| SC クエリ | 検索クエリ上位25（クリック順） |
| SC ページ | ページ別上位20（クリック順） |
| SC 月別 | 直近3ヶ月の月別クリック・表示回数 |
| SC 改善候補 | 表示50回以上 かつ 11位以下のクエリ |
