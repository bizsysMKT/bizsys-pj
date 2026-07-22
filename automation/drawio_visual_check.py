# -*- coding: utf-8 -*-
"""
drawioファイルをPNGに描画するビジュアルチェック用スクリプト。

AIがシステムイメージ（.drawio）を生成・修正した後、実際の見た目を確認するために使う。
出力されたPNGをAIに読み込ませて「重なり・整列・余白・はみ出し」を目視確認する。

使い方:
  python automation/drawio_visual_check.py <drawioファイル> <出力PNG>

必要環境: pip install playwright && playwright install chromium（要ネットワーク接続）
"""
import json
import os
import sys
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright


def check_overlaps(src):
    """図形同士の部分的な重なりを座標から機械検出する（目視で見逃しやすい角の重なり対策）"""
    root = ET.parse(src).getroot()
    rects = []
    for c in root.findall(".//mxCell"):
        g = c.find("mxGeometry")
        if g is None or c.get("vertex") != "1":
            continue
        style = c.get("style") or ""

        # 塗りなし（外枠・タイトル等のコンテナ）と矢印は意図的な交差が多いため除外
        if "fillColor=none" in style or "singleArrow" in style:
            continue
        x, y = float(g.get("x", 0)), float(g.get("y", 0))
        w, h = float(g.get("width", 0)), float(g.get("height", 0))
        rects.append((c.get("id"), (c.get("value") or "")[:15], x, y, x + w, y + h))

    found = 0
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a = rects[i]
            b = rects[j]
            ix = min(a[4], b[4]) - max(a[2], b[2])
            iy = min(a[5], b[5]) - max(a[3], b[3])

            # 交差なし、または片方が完全に内包される親子関係（画面ボックス内の部品）は対象外
            if ix <= 0 or iy <= 0:
                continue
            a_in_b = a[2] >= b[2] and a[3] >= b[3] and a[4] <= b[4] and a[5] <= b[5]
            b_in_a = b[2] >= a[2] and b[3] >= a[3] and b[4] <= a[4] and b[5] <= a[5]
            if a_in_b or b_in_a:
                continue
            found += 1
            print("重なり検出: %s「%s」 と %s「%s」 (交差 %.0fx%.0fpx)" % (a[0], a[1], b[0], b[1], ix, iy))
    if found == 0:
        print("重なり検査: OK（部分的な重なりなし）")
    return found


def main():
    if len(sys.argv) < 3:
        print("usage: python drawio_visual_check.py <drawioファイル> <出力PNG>")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]

    check_overlaps(src)

    xml = open(src, encoding="utf-8").read()

    # ------------------------------------------
    # ビューアHTMLの生成
    # ------------------------------------------

    # 重要：HTML属性へ埋め込む前に必ず & をエスケープする。
    # 怠るとブラウザの属性デコードで &lt;br&gt; が生の < に戻り、
    # XMLパースが静かに失敗して「途中のセルから先が描画されない」状態になる（2026-07 実績）
    payload = json.dumps({"nav": False, "xml": xml}).replace("&", "&amp;").replace("'", "&#39;")
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'></head>"
        "<body style='margin:0;background:#fff;'>"
        "<div class='mxgraph' style='width:2100px;' data-mxgraph='" + payload + "'></div>"
        "<script src='https://viewer.diagrams.net/js/viewer-static.min.js'></script>"
        "</body></html>"
    )
    tmp_html = os.path.splitext(dst)[0] + "_viewer.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    # ------------------------------------------
    # ヘッドレスブラウザで描画してスクリーンショット
    # ------------------------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 2150, "height": 1400}, device_scale_factor=1)
        page.goto("file:///" + os.path.abspath(tmp_html).replace("\\", "/"))
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # 描画要素数を出す（極端に少ない場合は描画が壊れているサイン）
        n = page.evaluate('document.querySelectorAll("svg rect, svg path, svg image").length')
        print("描画要素数:", n)
        page.screenshot(path=dst, full_page=True)
        browser.close()

    os.remove(tmp_html)
    print("出力:", dst)


if __name__ == "__main__":
    main()
