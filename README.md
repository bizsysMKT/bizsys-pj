# bizsys-pj

ビズシスLP自動運営プロジェクト

システム開発会社「ビズシス」の集客を、Webサイト（LP＋ブログ）＋X自動投稿で自動化するマーケティング基盤。Astro + GitHub Pages + GitHub Actions で構築し、最終的に運用担当者へ引き継ぐことを前提とする。

- 本番サイト：https://bizsys.jp

---

## はじめに読むドキュメント（迷ったらここから）

| ドキュメント | 内容 |
|---|---|
| [docs/overview.md](docs/overview.md) | **プロジェクト概要書。まずこれ。** 目的・対象範囲・フェーズ・KPIをワンページで |
| [docs/architecture.md](docs/architecture.md) | システム構成図（GitHub→Pages→X→GA4の繋がり）・URL正規化ポリシー |
| [docs/operation.md](docs/operation.md) | 日常運用フロー・ローカルプレビュー（dev.bat）・トラブル対応 |
| [docs/handover.md](docs/handover.md) | 引き継ぎチェックリスト・各サービス設定値のクイックリファレンス |

## 作業ルール・手順

| ドキュメント | 内容 |
|---|---|
| [docs/article-generation.md](docs/article-generation.md) | **ブログ記事作成の唯一の正**（ルール・テンプレート・公開前チェック） |
| [docs/monthly-analysis.md](docs/monthly-analysis.md) | 月次 GA4 + Search Console 分析手順 |
| [docs/keyword-research.md](docs/keyword-research.md) | 記事テーマのキーワード調査手順 |

## 記録・計画

| ドキュメント | 内容 |
|---|---|
| [docs/project_plan.md](docs/project_plan.md) | プロジェクト計画書（上位方針） |
| [docs/progress.md](docs/progress.md) | 進捗管理（WBS形式） |
| [docs/phase1-report.md](docs/phase1-report.md) | フェーズ1 完了報告書 |
| [input/②_依頼書.md](input/②_依頼書.md) | 依頼主からの元依頼書（HP構成・実績・記事テーマの一次情報） |

---

## ディレクトリ構成

| ディレクトリ | 役割 |
|---|---|
| `site/` | Astro ソース（LP・ブログ・ビルド設定） |
| `automation/` | 分析・自動投稿などのスクリプト |
| `docs/` | 設計・運用・引き継ぎドキュメント |
| `input/` | 依頼書・戦略メモ（読み取り専用） |
| `output/` | 成果物・分析レポートの出力先 |
| `tools/` | ローカル開発用ポータブルNode.js（読み取り専用） |

## ローカルでプレビューする

プロジェクト直下の **`dev.bat`** をダブルクリック → ブラウザで http://localhost:4321/ を開く（停止は Ctrl + C）。
同梱のポータブルNode.jsを使うため、PCへのNode.jsインストールは不要。詳細は [docs/operation.md](docs/operation.md) の「1.1.1 ローカルで下書きを確認する」を参照。

## 公開の流れ

`main` ブランチへ push すると GitHub Actions が自動でビルド＆デプロイし、数分で https://bizsys.jp に反映される。ブログ記事を push すると X（@bizsys_x）へ自動投稿される。
