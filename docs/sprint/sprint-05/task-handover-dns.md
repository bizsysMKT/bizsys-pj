# handover.md 追記依頼：DNS設定手順（お名前.com）

> 作成者：PM  
> 作成日：2026-04-09  
> 担当：実装担当  
> 対象ファイル：docs/handover.md

---

## 依頼内容

`docs/handover.md` の「0. サイト概要（クイックリファレンス）」セクション内、「デプロイ手順」の直前に、以下の「公開前準備：DNS設定 & GitHub設定」セクションを追記してください。

---

## 追記する内容

### 公開前準備：DNS設定 & GitHub設定

サイトを `biz-sys.jp` で公開するには、以下の2つの設定が必要です。**初回のみ。一度設定すれば以後は不要。**

---

#### STEP 1：お名前.com で DNS の A レコードを設定する

1. [お名前.com Navi](https://www.onamae.com/navi/) にログイン
2. 「ドメイン」→「ドメイン機能一覧」→「DNS関連機能の設定」をクリック
3. `biz-sys.jp` を選択し「次へ」
4. 「DNSレコード設定を利用する」→「設定する」をクリック
5. 以下の A レコードを4件追加する：

| TYPE | HOST | VALUE | TTL |
|------|------|-------|-----|
| A | @ | 185.199.108.153 | 3600 |
| A | @ | 185.199.109.153 | 3600 |
| A | @ | 185.199.110.153 | 3600 |
| A | @ | 185.199.111.153 | 3600 |

6. 「確認画面へ進む」→「設定する」で保存
7. DNS の反映には最大24〜48時間かかる場合がある

---

#### STEP 2：GitHub リポジトリを作成し GitHub Pages を有効にする

1. GitHub（github.com）に `bizsysMKT` アカウントでログイン
2. 「New repository」で `bizsys-pj` というリポジトリを作成（Public・mainブランチ）
3. リポジトリの「Settings」→「Pages」を開く
4. 「Source」を **「GitHub Actions」** に設定する
5. 「Custom domain」に `biz-sys.jp` を入力して「Save」

---

#### STEP 3：コードを push して公開する

```bash
git remote add origin https://github.com/bizsysMKT/bizsys-pj.git
git branch -M main
git push -u origin main
```

GitHub の「Actions」タブで緑チェックが付けば自動デプロイ完了。  
DNS 反映後（最大48時間）、`https://biz-sys.jp` にアクセスして表示を確認する。

---

## 配置場所の指定

`docs/handover.md` の「デプロイ手順（git push → 自動公開）」セクションの**直前**に挿入してください。

追記後、別途 report は不要です。完了したら PM に口頭で報告してください。
