#!/usr/bin/env python3
"""X (Twitter) 自動投稿スクリプト

新規ブログ記事のfrontmatterを読み取り、X（Twitter）に投稿する。
GitHub Actions の post-to-x.yml から呼び出される。

投稿フォーマット:
    {title}

    {description（140字制限に合わせて切り詰め）}

    #ビズシス #業務システム #Excel脱却

    https://bizsys.jp/blog/{slug}
"""

import os
import re
import sys
import time

import tweepy
import yaml

HASHTAGS = "#ビズシス #業務システム #Excel脱却"
BASE_URL = "https://bizsys.jp/blog"
TWEET_MAX_CHARS = 140
# Twitter は URL を常に23文字換算する
URL_CHAR_COUNT = 23
# 複数記事を連続投稿する場合のインターバル（秒）
POST_INTERVAL_SEC = 5


def parse_frontmatter(filepath: str) -> dict:
    """Markdown ファイルの YAML frontmatter を解析して返す。"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError(f"frontmatter が見つかりません: {filepath}")

    return yaml.safe_load(match.group(1))


def get_slug(filepath: str) -> str:
    """ファイルパスからスラッグ（拡張子なしファイル名）を返す。"""
    return os.path.splitext(os.path.basename(filepath))[0]


def build_tweet(title: str, description: str, slug: str) -> str:
    """投稿テキストを組み立てる。

    140文字を超える場合は description を切り詰める。
    URL は末尾固定で Twitter が23文字換算。
    """
    url = f"{BASE_URL}/{slug}"

    # 固定部分: title + 区切り文字 + hashtags + 区切り文字 + URL(23換算)
    # フォーマット: "{title}\n\n{desc}\n\n{hashtags}\n\n{url}"
    fixed_chars = len(title) + len("\n\n") + len("\n\n") + len(HASHTAGS) + len("\n\n") + URL_CHAR_COUNT
    desc_budget = TWEET_MAX_CHARS - fixed_chars

    if desc_budget <= 0:
        # タイトルだけで上限に達する極端なケース
        trimmed_desc = ""
    elif len(description) > desc_budget:
        trimmed_desc = description[: desc_budget - 1] + "…"
    else:
        trimmed_desc = description

    if trimmed_desc:
        return f"{title}\n\n{trimmed_desc}\n\n{HASHTAGS}\n\n{url}"
    else:
        return f"{title}\n\n{HASHTAGS}\n\n{url}"


def post_tweet(client: tweepy.Client, text: str) -> str:
    """X に投稿し、tweet ID を返す。"""
    response = client.create_tweet(text=text)
    return str(response.data["id"])


def main() -> None:
    api_key = os.environ["X_API_KEY"]
    api_secret = os.environ["X_API_SECRET"]
    access_token = os.environ["X_ACCESS_TOKEN"]
    access_token_secret = os.environ["X_ACCESS_TOKEN_SECRET"]
    new_files_str = os.environ.get("NEW_FILES", "").strip()

    if not new_files_str:
        print("新規ブログ記事なし。投稿をスキップします。")
        return

    new_files = [f for f in new_files_str.split() if f.endswith(".md")]

    if not new_files:
        print("対象の .md ファイルなし。投稿をスキップします。")
        return

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    errors: list[str] = []

    for i, filepath in enumerate(new_files):
        if i > 0:
            print(f"次の投稿まで {POST_INTERVAL_SEC} 秒待機...")
            time.sleep(POST_INTERVAL_SEC)

        try:
            fm = parse_frontmatter(filepath)
            title = fm.get("title", "")
            description = fm.get("description", "")
            slug = get_slug(filepath)

            tweet_text = build_tweet(title, description, slug)
            char_count = len(tweet_text) - len(f"{BASE_URL}/{slug}") + URL_CHAR_COUNT
            print(f"投稿内容（推定{char_count}文字）:\n{tweet_text}\n")

            tweet_id = post_tweet(client, tweet_text)
            print(f"✓ 投稿成功: {filepath} → tweet_id={tweet_id}")

        except Exception as e:
            msg = f"投稿失敗: {filepath} → {e}"
            print(f"::error::{msg}")
            errors.append(msg)

    if errors:
        print(f"\n{len(errors)} 件の投稿に失敗しました:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
