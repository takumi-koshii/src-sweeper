@echo off
setlocal enabledelayedexpansion

REM ========================================
REM 設定項目
REM ========================================

REM 除外する拡張子 (カンマ区切り、ドットは不要)
set EXCLUDE_EXTENSIONS=exe,dll,bin,obj,pdb,lib,so,dylib,zip,rar,7z,tar,gz,jpg,jpeg,png,gif,bmp,ico,mp3,mp4,avi,mov,pdf

REM 除外するフォルダー名 (カンマ区切り、大文字小文字は区別しません)
set EXCLUDE_FOLDERS=node_modules,.venv,venv,.git,.svn,.hg,__pycache__,.pytest_cache,.mypy_cache,.tox,dist,build,.godot,.vs,.vscode,bin,obj,target,.gradle,.idea,.next

REM 最大ファイルサイズ (MB)
set MAX_FILE_SIZE=10

REM ========================================
REM メイン処理
REM ========================================

REM 引数チェック
if "%~1"=="" (
    echo エラー: フォルダーをこの bat ファイルにドラッグアンドドロップしてください
    pause
    exit /b 1
)

REM ドラッグされたパスを取得
set TARGET_DIR=%~1

REM ディレクトリかどうかチェック
if not exist "%TARGET_DIR%" (
    echo エラー: 指定されたパスが存在しません: %TARGET_DIR%
    pause
    exit /b 1
)

REM ファイルの場合はエラー
if not exist "%TARGET_DIR%\*" (
    echo エラー: フォルダーを指定してください。ファイルは指定できません。
    pause
    exit /b 1
)

REM 出力ファイルパス (bat ファイルと同じディレクトリ)
set OUTPUT_FILE=%~dp0extracted.txt

REM Python スクリプトのパス
set PYTHON_SCRIPT=%~dp0main.py

REM Python スクリプトの存在チェック
if not exist "%PYTHON_SCRIPT%" (
    echo エラー: main.py が見つかりません
    echo %PYTHON_SCRIPT%
    pause
    exit /b 1
)

echo ========================================
echo ファイル抽出ツール
echo ========================================
echo 対象フォルダー: %TARGET_DIR%
echo 出力ファイル: %OUTPUT_FILE%
echo 除外拡張子: %EXCLUDE_EXTENSIONS%
echo 除外フォルダー: %EXCLUDE_FOLDERS%
echo 最大ファイルサイズ: %MAX_FILE_SIZE% MB
echo ========================================
echo.

REM Python スクリプトを実行
python "%PYTHON_SCRIPT%" "%TARGET_DIR%" "%OUTPUT_FILE%" --exclude "%EXCLUDE_EXTENSIONS%" --exclude-folders "%EXCLUDE_FOLDERS%" --max-size %MAX_FILE_SIZE%

REM 実行結果チェック
if %errorlevel% neq 0 (
    echo.
    echo エラーが発生しました
    pause
    exit /b 1
)

echo.
echo 処理が完了しました
echo 結果ファイル: %OUTPUT_FILE%
pause