#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
keyword-research.py

ブログ記事の方向性を調査するスクリプト。
  - Googleサジェスト（オートコンプリート）：実際に検索されている関連語を収集（認証不要・無料）
  - Search Console：自サイトが既に表示されている検索語を確認（直近90日）

サジェストで「世の中の検索需要（記事ネタ）」を、Search Consoleで「自サイトの現状」を把握し、
両者を突き合わせて次に書くべき記事テーマを決める。

前提：
  - pip install google-api-python-client google-auth
  - サービスアカウントJSONが配置されていること（Search Console閲覧権限つき）

実行方法：
  python -X utf8 automation/keyword-research.py

認証情報のパス：
  環境変数 GOOGLE_APPLICATION_CREDENTIALS で指定可能。
  未指定の場合は下記 DEFAULT_CREDS_FILE を使用する。
"""

import os
import json
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ─── 設定 ───────────────────────────────────────────────

# サービスアカウントJSON（環境変数優先・なければデフォルト）
DEFAULT_CREDS_FILE = r"C:\Users\tk171\claude-work\google_credentials.json"
CREDS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", DEFAULT_CREDS_FILE)

# Search Console サイトURL
SITE_URL = os.environ.get("SEARCH_CONSOLE_SITE_URL", "https://bizsys.jp/")

# シード（ターゲットに沿った起点キーワード）。必要に応じて増減する。
SEEDS = [
    # Excel横断
    "Excel 管理", "Excel 脱却", "Excel 限界",
    # 業務系
    "在庫管理 システム", "受注管理 システム", "顧客管理 システム",
    "原価管理 システム", "日報 システム",
    # システム化検討
    "業務システム 費用", "システム化 中小企業", "システム 発注",
    # 業種特化（ターゲット4業種）
    "運送業 システム", "製造業 システム", "介護 システム", "EC 在庫管理",
]


# ─── Googleサジェスト取得 ────────────────────────────────

def get_suggest(keyword):
    """
    Googleサジェスト（オートコンプリート）を取得する。
    client=firefox を指定すると [入力語, [候補, ...]] のクリーンなJSONが返る。
    認証不要・無料。
    """
    url = "http://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode({
        "client": "firefox",
        "hl": "ja",
        "q": keyword,
    })
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data[1] if len(data) > 1 else []
    except Exception as e:
        # 取得失敗してもスクリプト全体は止めない（節目のログは残す）
        print(f"    [WARN] サジェスト取得失敗: {keyword} ({e})")
        return []


# ─── メイン ──────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Googleサジェスト調査（実際に検索されている関連語）")
    print("=" * 60)

    for seed in SEEDS:
        sugg = get_suggest(seed)
        print(f"\n■ 「{seed}」")
        for s in sugg:
            print(f"    - {s}")

        # 連続アクセスでブロックされないよう間隔をあける
        time.sleep(0.3)

    # ── Search Console（90日：自サイトが既に表示されている語句）──
    print("\n" + "=" * 60)
    print("  Search Console（90日：自サイトが拾えている検索語）")
    print("=" * 60)

    creds = Credentials.from_service_account_file(
        CREDS_FILE, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    sc = build("searchconsole", "v1", credentials=creds)

    today = date.today()
    body = {
        # Search Consoleは最新3〜4日が未確定のため4日前まで
        "startDate": (today - timedelta(days=94)).isoformat(),
        "endDate": (today - timedelta(days=4)).isoformat(),
        "dimensions": ["query"],
        "rowLimit": 100,
        "dataState": "all",
    }
    rows = sc.searchanalytics().query(siteUrl=SITE_URL, body=body).execute().get("rows", [])

    if rows:
        for r in sorted(rows, key=lambda x: x.get("impressions", 0), reverse=True):
            q = r["keys"][0]
            print(f"    {q:<30} 表示{int(r.get('impressions',0))} "
                  f"クリック{int(r.get('clicks',0))} 順位{r.get('position',0):.1f}")
    else:
        print("    （表示データなし＝サイトがまだ初期段階）")

    print("\n" + "=" * 60)
    print("  完了")
    print(f"  サイト: {SITE_URL} / 認証: {CREDS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
