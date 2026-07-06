# 引き継ぎドキュメント（Handover）

## 設計意図
このドキュメントは『プロジェクト実装チーム（Yusuke 等）から漢那さんへのシステム引き継ぎ』を確実にするためのチェックリストです。引き継ぎ完了時点で『漢那さんが 100% 独立運用できる状態』が目的です。

---

## 0. サイト概要（クイックリファレンス）

### URL
- 本番サイト：https://bizsys.jp

### 技術構成

| 項目 | 内容 |
|------|------|
| フレームワーク | Astro 6.1.3（静的サイト生成） |
| ホスティング | GitHub Pages（カスタムドメイン） |
| フォント | Noto Sans JP（Google Fonts） |
| お問い合わせ | Formspree（ID: maqllrnj） |
| アクセス解析 | Google Analytics 4（測定ID: G-04S9SZW07N） |

### ディレクトリ構成

```
bizsys-pj/
├── .github/workflows/deploy.yml      # 自動デプロイ設定（mainブランチへのpushで起動）
├── .github/workflows/post-to-x.yml  # X 自動投稿設定（ブログ記事 push で起動）
├── automation/post_to_x.py          # X 投稿スクリプト
├── docs/                         # 設計・手順ドキュメント
│   └── handover.md               # このファイル
├── site/                         # Astro サイトのソースコード
│   ├── public/CNAME              # カスタムドメイン設定
│   ├── src/
│   │   ├── components/Layout.astro  # 共通レイアウト（ヘッダー・フッター・CSS）
│   │   ├── content/blog/            # ブログ記事（Markdown形式）
│   │   └── pages/                   # 各ページ（.astroファイル）
│   └── astro.config.mjs
└── tools/                        # ローカル開発用 Node.js（読み取り専用）
```

### ブログ記事の追加方法

1. `site/src/content/blog/` に新しいMarkdownファイルを作成する
2. ファイル名は `YYYY-MM-DD-記事スラッグ.md` の形式にする
3. 冒頭に以下の frontmatter を記述する：

```markdown
---
title: 記事タイトル
date: 2026-04-09
description: 記事の説明文（一覧ページに表示される）
tags: [タグ1, タグ2]
---

## 見出し

本文をMarkdown形式で書く。
```

4. git push すると自動デプロイで公開される

### LP 文言の修正方法

`site/src/pages/` の `.astro` ファイルをテキストエディタで開き、HTMLタグの中のテキストを直接編集 → git push で自動公開。

### 公開前準備：DNS設定 & GitHub設定

サイトを `bizsys.jp` で公開するには、以下の2つの設定が必要です。**初回のみ。一度設定すれば以後は不要。**

#### STEP 1：お名前.com で DNS の A レコードを設定する

1. [お名前.com Navi](https://www.onamae.com/navi/) にログイン
2. 「ドメイン」→「ドメイン機能一覧」→「DNS関連機能の設定」をクリック
3. `bizsys.jp` を選択し「次へ」
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

#### STEP 2：GitHub リポジトリを作成し GitHub Pages を有効にする

1. GitHub（github.com）に `bizsysMKT` アカウントでログイン
2. 「New repository」で `bizsys-pj` というリポジトリを作成（Public・mainブランチ）
3. リポジトリの「Settings」→「Pages」を開く
4. 「Build and deployment」セクションの「Source」ドロップダウンを **「GitHub Actions」** に変更する（デフォルトは「Deploy from a branch」になっている）
5. 「Custom domain」に `bizsys.jp` を入力して「Save」

#### STEP 3：コードを push して公開する

```bash
git remote add origin https://github.com/bizsysMKT/bizsys-pj.git
git branch -M main
git push -u origin main
```

GitHub の「Actions」タブで緑チェックが付けば自動デプロイ完了。  
DNS 反映後（最大48時間）、`https://bizsys.jp` にアクセスして表示を確認する。

---

### デプロイ手順（git push → 自動公開）

```bash
git add .
git commit -m "変更内容の説明"
git push origin main
```

GitHub の「Actions」タブで緑チェックが付けば公開完了（通常1〜2分）。

### Search Console 初回設定手順（GA4 連携方式）

GA4 が設定済みのため、ファイルアップロードなしで認証できる。

1. [Google Search Console](https://search.google.com/search-console) にアクセス（Google アカウントでログイン）
2. 「プロパティを追加」→「URL プレフィックス」→ `https://bizsys.jp` を入力して「続行」
3. **「所有権を自動確認しました」と表示された場合：** そのまま「プロパティに移動」をクリックして完了（手順4〜5は不要）
4. 自動確認されなかった場合：確認方法の一覧から **「Google アナリティクス」** を選択
5. GA4 プロパティ（G-04S9SZW07N）が表示されたら「確認」をクリック
6. データ反映まで数日かかる場合がある

### トラブル対応（よくある問題）

| 症状 | 確認場所 | 対処 |
|------|---------|------|
| サイトが更新されない | GitHub「Actions」タブ | エラーログを確認。Markdownの`---`が抜けているケースが多い |
| 問い合わせメールが届かない | https://formspree.io/ | フォーム `maqllrnj` の通知メールアドレスを確認 |
| GA4でアクセスが見えない | GA4「リアルタイム」タブ | トラッキングIDがLayoutに埋め込まれているか確認 |
| ページが真っ白になる | GitHub「Actions」タブ | ビルドエラーのログを確認 |

---

## 1. 引き継ぎ前チェックリスト（実装チーム用）

### 技術構成＆アカウント準備

以下をすべてチェックしてから引き継ぎを開始してください。

```
【GitHub】
✅ bizsys-pj リポジトリ作成完了
✅ site/src/content/blog/, automation/ ディレクトリ構造確認
✅ GitHub Actions ワークフロー（deploy.yml・post-to-x.yml）が正常動作
✅ X API キーを GitHub Secrets（X_API_KEY / X_API_SECRET / X_ACCESS_TOKEN / X_ACCESS_TOKEN_SECRET）に登録済み
□ バックアップリポジトリ（別アカウント）作成 & 定期バックアップ設定（引き継ぎ後に漢那さんが実施可）

【GitHub Pages】
✅ bizsys.jp ドメイン設定完了（DNS 反映確認）
✅ HP・ブログが公開状態で確認可能
□ www.bizsys.jp CNAME設定（漢那さんが対応予定）
✅ HTTPS の自動化（GitHub Pages）が有効

【X (Twitter)】
✅ @bizsys_x アカウント作成完了
✅ アカウント所有者設定：漢那さん
✅ X API キー取得・GitHub Secrets に登録
✅ テスト投稿（自動・手動両方）で動作確認（2026-05-01 確認）
□ アカウントのセキュリティ設定（2段階認証等）→ 引き継ぎセッションで確認

【Google Analytics 4】
✅ GA4 プロパティ作成
✅ bizsys.jp 全ページへのトラッキング ID 設定
✅ リアルタイムレポートで計測確認
✅ 漢那さんの Google アカウントにアクセス権限付与（漢那さんが設定済み）
✅ 「所有者」権限で漢那さんを登録（漢那さんが設定済み）

【Google Search Console】
✅ bizsys.jp をプロパティ登録
✅ 漢那さんの Google アカウントにアクセス権限付与（漢那さんが設定済み）
✅ DNS/HTML ファイル確認完了
✅ サイトマップ送信（sitemap-index.xml / 2026-05-01 送信済み）

【Formspree】
✅ フォーム作成・HP に埋め込み完了（フォームID: maqllrnj）
✅ 送信先メールを漢那さんのメールアドレスに設定（漢那さんが設定済み）
□ テスト送信：引き継ぎセッションで漢那さんが受信確認

【ドキュメント】
✅ docs/overview.md 完成 & レビュー完了（2026-05-01 更新）
✅ docs/architecture.md 完成 & レビュー完了（2026-05-01 更新）
✅ docs/operation.md 完成 & レビュー完了（2026-05-01 更新）
✅ docs/handover.md（このファイル）完成（2026-05-01 更新）
✅ docs/templates/monthly_report.md 完成
✅ docs/article-generation.md 完成（記事のルール・テンプレート・手順を一元化。旧blog_template.md/blog-workflow.mdは2026-07-06に統合・廃止）
✅ docs/monthly-analysis.md 完成（月次分析手順書）
✅ 各ドキュメントに「非エンジニア向け説明」が含まれている

【その他】
✅ GitHub Desktop インストール方法（handover.md 内に記載）
✅ 緊急時の連絡先・エスカレーション方法（operation.md セクション6に記載）
□ 月次レビュースケジュール（第1営業日）→ 引き継ぎセッションで確定
```

---

## 2. 引き継ぎセッション（漢那さん自己完結型）

### 概要

このセッションは漢那さんが **Claude Code を起動して一人で実施** します。チームメンバーへの依存はありません。わからないことはすべて Claude Code に質問してください。

**所要時間目安**：2〜3時間（自分のペースで分割してもよい）  
**準備するもの**：PC、bizsys-pj リポジトリへのアクセス、Claude Code

---

### ステップ1：環境確認（30分）

**1-1. GitHub Desktop**
```
□ GitHub Desktop をインストール・ログインできた
□ bizsys-pj リポジトリをクローンできた
□ Commit & Push の操作を確認した
```
→ わからない場合：Claude Code に「GitHub Desktop でリポジトリをクローンする方法を教えて」と聞く

**1-2. 各サービスへのログイン確認**
```
□ GitHub（github.com/bizsysMKT/bizsys-pj）にアクセスできた
□ Google Analytics 4（analytics.google.com）にログインできた
□ Google Search Console（search.google.com/search-console）にログインできた
□ X（@bizsys_x）にログインできた
□ Formspree（formspree.io）にログインできた
```

---

### ステップ2：記事を1本投稿する（30分）

Claude Code に「ブログ記事の下書きを作って」と依頼して、実際に1本投稿してください。

```
□ docs/article-generation.md（記事ルール・テンプレート）を確認した
□ Claude Code で下書きを生成した（docs/article-generation.md のプロンプト参照）
□ site/src/content/blog/ に保存した
□ GitHub Desktop で Commit & Push した
□ bizsys.jp/blog で記事が公開されたことを確認した
□ X（@bizsys_x）に自動投稿されたことを確認した
```
→ エラーが出た場合：GitHub Actions のログをコピーして Claude Code に貼り付ける

---

### ステップ3：月次レビューの流れを確認する（30分）

```
□ GA4 で先月のアクセス数を確認した
□ Search Console で上位クエリを確認した
□ docs/templates/monthly_report.md を開いて記入方法を確認した
□ docs/monthly-analysis.md を読んで分析手順を把握した
```
→ 「GA4 の見方がわからない」場合：Claude Code に「GA4 で月間アクセス数を確認する方法」と聞く

---

### ステップ4：トラブル対応の確認（30分）

docs/operation.md の「トラブルシューティング」を読んで、以下を確認してください。

```
□ GitHub Actions のログ確認方法を理解した
□ Markdown 形式エラーの対応方法を理解した
□ X 自動投稿が失敗した場合の対応を理解した
□ 困ったときに Claude Code に相談する流れを把握した
```

---

### ステップ5：セッション完了チェック

```
□ ステップ1〜4をすべて完了した
□ 疑問点を Claude Code で解消した
□ 以降は自分一人で運用できると判断できた
```

完了したら、このファイルのセクション8「引き継ぎ確認書」に実施日を記入してください。

---

## 3. 引き継ぎ完了チェックリスト（漢那さん用）

### ツール・アカウント操作

以下のすべてを『自分で』実際にやってみて、チェックしてください。

#### GitHub Desktop
```
□ GitHub Desktop をインストール・ログインできた
□ bizsys-pj リポジトリをクローンできた
□ 新しいブランチを作成できた
□ 新しいファイルを追加してCommitできた
□ Pushして GitHub.com で反映を確認できた
□ その後、自動デプロイで bizsys.jp に反映されたことを確認
```

**チェック基準**：迷わずできる状態（カンペなしで実行可能）

---

#### ブログ記事作成＆投稿
```
□ docs/article-generation.md のテンプレートを見ながら ✓ 新規記事を書ける
□ Markdown 形式（# 見出し、**太字** 等）が理解できる
□ Front-matter（---の間）の役割が理解できている
□ 記事を site/src/content/blog/ に保存できた
□ GitHub Desktop で Commit & Push できた
□ 2～3分後、bizsys.jp/blog で記事が公開されたことを確認
□ X (@bizsys_x) に自動投稿されたことを確認
```

**チェック基準**：『記事を書いて公開』の全フロー を1人で完結できる

---

#### Google Analytics 4（GA4）
```
□ GA4 にログインできた
□ 「レポート > ユーザー」で訪問者数の推移を見られる
□ 「レポート > ページとスクリーン」で各ページの PV を見られる
□ 先月のデータを確認できた
□ データの『意味』が大まかに理解できている
  例）「このページは 15 PV = 15人が見た」
```

**チェック基準**：GA4 の基本レポートが読める

---

#### Google Search Console
```
□ Google Search Console にログインできた
□ 「検索パフォーマンス」で検索キーワード・クリック数を見られる
□ 「サイトマップ」で bizsys.jp のページが登録されているか確認
□ 「カバレッジ」で『エラー』がないか確認
```

**チェック基準**：検索パフォーマンスレポートが読める

---

#### X (Twitter)
```
□ @bizsys_x にログインできた
□ タイムラインで自動投稿が表示されている
□ 手動で投稿ができた（テスト投稿、その後削除 OK）
□ アカウント設定（プロフィール・セキュリティ）が理解できている
```

**チェック基準**：@bizsys_x の管理ができる

---

#### Formspree（問い合わせフォーム）
```
□ bizsys.jp/contact の問い合わせフォームが見える
□ テスト送信を実施
□ 自分のメールに問い合わせメールが受信されたことを確認
□ Formspree 管理画面にも記録されていることを確認
```

**チェック基準**：フォーム受信の一連の流れが理解できている

---

### ドキュメント理解

```
□ docs/overview.md を読んで「このプロジェクトは何か」が説明できる
□ docs/architecture.md を読んで「どう繋がっているか」が図で説明できる
□ docs/operation.md を読んで「毎月何をするか」が説明できる
□ docs/article-generation.md を参照せずに記事テンプレートを作成できる
□ docs/templates/monthly_report.md を理解して月次レポートが記入できる
```

**チェック基準**：ドキュメント全体が『一貫性』を持って理解できている状態

---

### 月次運用体験

```
□ 『記事追加 → デプロイ → X投稿 → GA4確認』の全フロー を1周実施
□ 実施時間：1～2時間程度（毎周）であることを確認
□ トラブルが起きた場合、operation.md または Claude Code で対応できた
□ 月次レビューを自己実施した
  - KPI確認
  - 来月の施策決定
  - docs/templates/monthly_report.md に記入
```

**チェック基準**：月次運用が『習慣』として実行できている

---

### トラブル対応体験

以下のいずれかが発生し、漢那さんが対応できたこと：

```
□ 記事が公開されない → GitHub Actions のログで原因を特定できた
  または
□ X に投稿されない → operation.md を参照して対応できた
  または
□ GA4 でアクセスが見えない → 計測トラッキングを確認できた
  または
□ 問い合わせメールが来ない → Formspree を確認できた
```

**チェック基準**：『困ったときに自分で調べる力』が備わっている

---

## 4. 引き継ぎ完了基準（最終ゴール）

以下のすべてが満たされた時点で『引き継ぎ完了』とします。

### A. 技術的な独立性
```
✅ GitHub Desktop でブログ記事の追加・更新ができる
✅ エラーが出た時に operation.md を参照して対応できる
✅ GA4・Search Console の基本レポートが読める
✅ トラブル時は operation.md → Claude Code の順で自己解決できる
```

### B. 運用スキルの習得
```
✅ 週2～3本のブログ記事を『テンプレートなしで』作成できる
✅ 月1回の KPI 確認・レポート記入を『一人で』できる
✅ 月次レビューを自己実施できる（monthly_report.md に記入）
✅ 緊急対応（記事削除・X投稿修正 等）を判断できる
```

### C. ドキュメント継承
```
✅ overview.md / architecture.md / operation.md を『何度も読んで』理解
✅ テンプレート（article-generation.md内の記事テンプレート / monthly_report.md）を使いこなせる
✅『何か出てきた時に、最初にどのドキュメントを開くか』が判断できる
✅ 必要に応じて operation.md に『新しいトラブル対応』を追記できる
```

### D. 組織的な継続性
```
✅ サポートウィーニング（段階的な支援削減）スケジュールが合意済み
✅ 引き継ぎ完了後の『定期チェックイン』（例：月1回）の予定が決定
✅ 漢那さんが『このシステムのオーナー』という認識を持っている
✅ 変更・追加したい場合は Claude Code に相談できる
```

---

## 5. 引き継ぎ完了後の運用体制

引き継ぎ後は漢那さんが完全にオーナーとして自己管理します。

### 定期作業スケジュール

```
【毎週】
□ ブログ記事を2〜3本追加
□ X 自動投稿が成功しているか確認

【毎月初旬】
□ GA4・Search Console でKPIを確認
□ docs/templates/monthly_report.md に記入
□ 来月の施策（記事テーマ・本数）を決定
□ operation.md に新しいトラブル対応があれば追記

【3ヶ月ごと】
□ X API キー有効期限を X Developer Portal で確認
□ GitHub・Google・X の2段階認証設定を確認
```

### 困ったときの対応

1. `docs/operation.md` のトラブルシューティングを確認する
2. 解決しない場合は **Claude Code** にエラーログを貼り付けて相談する
3. Claude Code で解決したら operation.md に対応手順を追記する（次回のために）

---

## 6. 引き継ぎが不完全だと感じたら

```
以下の項目で不安がある場合、引き継ぎセッション（セクション2）を再実施してください：

□ GitHub Desktop の操作に不安がある
□ Markdown 形式エラーへの対応が不明確
□ GA4・Search Console の見方が分からない
□ Claude Code の使い方が分からない

対応：
1. 不安な項目のステップを再実施する
2. Claude Code に「○○の手順を教えて」と質問して補足する
3. 解消したらセクション3のチェックリストを再確認する
```

---

## 7. 引き継ぎ確認書

```
実施日：2026年____月____日

セッション完了チェック：
  □ ステップ1：環境確認 ✅ 完了
  □ ステップ2：記事投稿実践 ✅ 完了
  □ ステップ3：月次レビュー確認 ✅ 完了
  □ ステップ4：トラブル対応確認 ✅ 完了

判定：
  □ 技術的な独立性   ✅ 達成
  □ 運用スキル習得   ✅ 達成
  □ ドキュメント理解 ✅ 達成
  □ Claude Code 活用 ✅ 達成

最終判定：✅ 引き継ぎ完了（漢那さん、単独運用可能）

確認日：____年____月____日
```

---

## 9. 引き継ぎ後の定期チェック（テンプレート）

毎月の月次レビューで、以下を確認：

```
【月次レビュー（____年____月____日実施）】

KPI確認：
  □ HP月間アクセス数：____ （目標50以上）
  □ 記事平均PV：____ （目標5以上）
  □ X自動投稿成功率：____% （目標95%以上）

運用状況：
  □ 記事追加ペース：週____本（目標2～3本）
  □ トラブル発生：有 / 無 → あれば内容：
  □ GitHub Actions：エラー／正常
  □ 作業時間：____時間／月（効率化に課題？）

来月の施策：
  □ 記事ネタ：
  □ 投稿頻度：
  □ その他：

サポート必要性：
  □ 今月：実施内容____
  □ 来月：必要 / 不要
```

---

**最終更新日**：2026年5月1日
