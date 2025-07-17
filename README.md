# ソース収集器

可読なファイルを網羅的に走査し extracted.txt として一覧化するスクリプトです。

## 使い方

run.bat にフォルダーをドラッグアンドドロップすると、中身を再帰的に走査し extracted.txt を生成します。

### run.bat の設定項目
- 除外する拡張子 (カンマ区切り、ドットは不要)  
  EXCLUDE_EXTENSIONS=exe,dll,bin,obj,pdb,lib,so,dylib,zip,rar,7z,tar,gz,jpg,jpeg,png,gif,bmp,ico,mp3,mp4,avi,mov,pdf
- 除外するフォルダー名 (カンマ区切り、大文字小文字は区別しません)  
  EXCLUDE_FOLDERS=node_modules,.venv,venv,.git,.svn,.hg,__pycache__,.pytest_cache,.mypy_cache,.tox,dist,build,.godot,.vs,.vscode,bin,obj,target,.gradle,.idea,.next
- 最大ファイルサイズ (MB)  
  MAX_FILE_SIZE=10

## 動作環境

Python 3.x