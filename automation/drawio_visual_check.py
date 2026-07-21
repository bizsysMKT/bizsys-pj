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

from playwright.sync_api import sync_playwright


def main():
    if len(sys.argv) < 3:
        print("usage: python drawio_visual_check.py <drawioファイル> <出力PNG>")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]

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


main()
