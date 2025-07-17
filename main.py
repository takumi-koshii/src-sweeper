import os
import sys
import argparse
from pathlib import Path

def is_text_file(file_path, max_size_mb):
    """ファイルがテキストファイルかどうかを判定する"""
    try:
        # ファイルサイズチェック
        file_size = os.path.getsize(file_path)
        if file_size > max_size_mb * 1024 * 1024:
            return False, None, "ファイルサイズが上限を超過"
        
        if file_size == 0:
            return True, "", "空ファイル"
        
        # UTF-8 で試行
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return True, content, "UTF-8"
        except UnicodeDecodeError:
            pass
        
        # Shift_JIS で試行
        try:
            with open(file_path, 'r', encoding='shift_jis') as f:
                content = f.read()
            return True, content, "Shift_JIS"
        except UnicodeDecodeError:
            pass
        
        return False, None, "バイナリファイル"
        
    except Exception as e:
        return False, None, f"エラー: {str(e)}"

def should_exclude_file(file_path, exclude_extensions):
    """ファイルを除外するかどうかを判定する"""
    file_extension = Path(file_path).suffix.lower()
    return file_extension in exclude_extensions

def should_exclude_folder(folder_path, target_dir, exclude_folders):
    """フォルダーを除外するかどうかを判定する"""
    folder_path = Path(folder_path)
    target_path = Path(target_dir)
    
    # 相対パスの各部分をチェック
    try:
        relative_path = folder_path.relative_to(target_path)
        path_parts = relative_path.parts
        
        # パスの各部分が除外フォルダーに含まれているかチェック
        for part in path_parts:
            if part.lower() in exclude_folders:
                return True, part
        
        return False, None
    except ValueError:
        # relative_to が失敗した場合（パスが target_dir の外にある場合）
        return False, None

def extract_files(target_dir, output_file, exclude_extensions, exclude_folders, max_size_mb):
    """指定されたディレクトリから可読ファイルを抽出する"""
    target_path = Path(target_dir)
    output_path = Path(output_file)
    
    if not target_path.exists():
        print(f"エラー: 指定されたディレクトリが存在しません: {target_dir}")
        return False
    
    extracted_files = []
    skipped_files = []
    excluded_folders_count = 0
    
    # 再帰的にファイルを検索
    for file_path in target_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(target_path)
            
            # 除外フォルダーチェック
            should_exclude, excluded_folder = should_exclude_folder(file_path.parent, target_dir, exclude_folders)
            if should_exclude:
                skipped_files.append((str(relative_path), f"除外フォルダー内 ({excluded_folder})"))
                continue
            
            # 除外拡張子チェック
            if should_exclude_file(file_path, exclude_extensions):
                skipped_files.append((str(relative_path), "除外拡張子"))
                continue
            
            # テキストファイル判定
            is_text, content, reason = is_text_file(file_path, max_size_mb)
            
            if is_text:
                extracted_files.append((str(relative_path), content))
                print(f"抽出: {relative_path} ({reason})")
            else:
                skipped_files.append((str(relative_path), reason))
                print(f"スキップ: {relative_path} ({reason})")
    
    # 除外されたフォルダーの数を計算
    excluded_folder_paths = set()
    for file_path in target_path.rglob('*'):
        if file_path.is_dir():
            should_exclude, excluded_folder = should_exclude_folder(file_path, target_dir, exclude_folders)
            if should_exclude:
                excluded_folder_paths.add(str(file_path.relative_to(target_path)))
    
    excluded_folders_count = len(excluded_folder_paths)
    
    # 結果をファイルに出力
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, (file_path, content) in enumerate(extracted_files):
                if i > 0:
                    f.write("\n")
                f.write(f"{file_path}\n\n")
                f.write(content)
                f.write("\n\n---")
            
            # 最後の --- を削除
            if extracted_files:
                f.seek(f.tell() - 4)
                f.truncate()
        
        print(f"\n抽出完了: {len(extracted_files)} ファイルを {output_file} に保存しました")
        print(f"スキップ: {len(skipped_files)} ファイル")
        if excluded_folders_count > 0:
            print(f"除外フォルダー: {excluded_folders_count} フォルダー")
        
        return True
        
    except Exception as e:
        print(f"エラー: ファイル出力に失敗しました: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='フォルダー内の可読ファイルを抽出します')
    parser.add_argument('target_dir', help='対象ディレクトリ')
    parser.add_argument('output_file', help='出力ファイル')
    parser.add_argument('--exclude', default='', help='除外する拡張子 (カンマ区切り)')
    parser.add_argument('--exclude-folders', default='', help='除外するフォルダー名 (カンマ区切り)')
    parser.add_argument('--max-size', type=float, default=10.0, help='最大ファイルサイズ (MB)')
    
    args = parser.parse_args()
    
    # 除外拡張子を処理
    exclude_extensions = set()
    if args.exclude:
        exclude_extensions = {ext.strip().lower() for ext in args.exclude.split(',')}
        # ドットが付いていない場合は追加
        exclude_extensions = {ext if ext.startswith('.') else f'.{ext}' for ext in exclude_extensions}
    
    # 除外フォルダーを処理
    exclude_folders = set()
    if args.exclude_folders:
        exclude_folders = {folder.strip().lower() for folder in args.exclude_folders.split(',')}
    
    print(f"対象ディレクトリ: {args.target_dir}")
    print(f"出力ファイル: {args.output_file}")
    print(f"除外拡張子: {exclude_extensions if exclude_extensions else 'なし'}")
    print(f"除外フォルダー: {exclude_folders if exclude_folders else 'なし'}")
    print(f"最大ファイルサイズ: {args.max_size} MB")
    print("-" * 50)
    
    success = extract_files(args.target_dir, args.output_file, exclude_extensions, exclude_folders, args.max_size)
    
    if success:
        print("\n処理が正常に完了しました")
    else:
        print("\n処理中にエラーが発生しました")
        sys.exit(1)

if __name__ == "__main__":
    main()