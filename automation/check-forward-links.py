# ブログ記事の内部リンク公開順チェック
#
# 予約投稿（未来日付）の仕組み上、「リンク元より後に公開されるリンク先」への
# 内部リンクは、リンク先が公開されるまで本番で404になる。
# 記事追加・日付変更のたびに実行し、「違反なし」を確認してからpushすること。
#
# 実行方法（プロジェクトルートから）:
#   python -X utf8 automation/check-forward-links.py
import os
import re
import glob
import datetime

# プロジェクト内で完結させるため、このファイルからの相対パスで解決する
BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "src", "content", "blog")

# 全記事の date を収集
dates = {}
bodies = {}
for path in glob.glob(os.path.join(BLOG_DIR, "*.md")):
    slug = os.path.splitext(os.path.basename(path))[0]

    # テンプレートはチェック対象外
    if slug == "article-template":
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    dates[slug] = m.group(1)
    bodies[slug] = text

today = datetime.date.today().isoformat()

# /blog/スラッグ への内部リンクを抽出して日付比較
violations = []
for slug, text in bodies.items():
    links = set(re.findall(r'/blog/([a-z0-9-]+)', text))
    for target in links:

        # タグページは記事ではないため除外
        if target == "tag":
            continue

        # リンク先スラッグが存在しない（打ち間違い等）
        if target not in dates:
            violations.append((slug, dates[slug], target, "リンク先が存在しない"))
            continue

        # 過去分（既に両方公開済み）は問題にならないため、リンク先が未来日付のものだけ検出
        if dates[target] > dates[slug] and dates[target] > today:
            violations.append((slug, dates[slug], target, dates[target]))

print("=== リンク元より後に公開されるリンク先（一時404の原因） ===")
if not violations:
    print("  違反なし")
for v in sorted(violations, key=lambda x: x[1]):
    print(f"  {v[0]} ({v[1]}) -> {v[2]} ({v[3]})")
