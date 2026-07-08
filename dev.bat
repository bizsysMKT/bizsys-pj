@echo off
setlocal

rem ============================================================
rem ローカル開発サーバー起動用バッチ
rem tools\node のポータブルNode.jsを使うため、グローバル環境を汚さない
rem 起動後 http://localhost:4321/ でLPを確認できる（Ctrl+C で停止）
rem ============================================================

set "PATH=%~dp0tools\node;%PATH%"

echo [dev.bat] Node.js バージョン確認
node -v

cd /d "%~dp0site"
call npm run dev %*

endlocal
