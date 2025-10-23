import ffmpeg
import sys
from pathlib import Path

def convert_mp3_to_mp4_black(input_folder: Path, output_folder: Path, resolution: str = '1280x720'):
    """
    フォルダ内のMP3を、黒画面のMP4動画に一括変換します。
    (要: FFmpeg, pip install ffmpeg-python)
    """

    # 出力フォルダがなければ作成
    output_folder.mkdir(parents=True, exist_ok=True)
    print(f"出力先: {output_folder.resolve()}")

    print(f"スキャン中: {input_folder.resolve()}")
    converted_count = 0
    failed_files = []

    # 入力フォルダ内の .mp3 ファイルをスキャン
    # .glob("*.mp3") は大文字の .MP3 を見逃すため、より柔軟な方法に変更
    mp3_files = [p for p in input_folder.glob("*") if p.suffix.lower() == ".mp3"]

    if not mp3_files:
        print("MP3ファイルが見つかりませんでした。")
        return

    for input_path in mp3_files:
        
        # 出力ファイルパスを生成 (例: music.mp3 -> music.mp4)
        output_filename = input_path.stem + ".mp4"
        output_path = output_folder / output_filename

        print(f"変換中: {input_path.name} -> {output_filename}")

        try:
            # 1. 黒画面のビデオストリームを生成 (lavfi)
            # 'r=1' (1fps) を指定して実質的な静止画とする
            video_input = ffmpeg.input(
                f'color=c=black:s={resolution}:r=1', 
                f='lavfi'
            )

            # 2. MP3のオーディオストリーム
            audio_input = ffmpeg.input(str(input_path))

            # 3. 実行
            (
                ffmpeg
                .output(
                    video_input,          # 映像入力
                    audio_input,          # 音声入力
                    str(output_path),     # 出力パス
                    vcodec='libx264',     # H.264 ビデオコーデック (一般的)
                    acodec='aac',         # AAC オーディオコーデック (MP4標準)
                    pix_fmt='yuv420p',    # 互換性の高いピクセルフォーマット
                    shortest=None         # 音声の長さに映像を合わせる
                )
                .overwrite_output() # 既存ファイルを上書き
                .run(capture_stdout=True, capture_stderr=True) 
            )
            
            converted_count += 1
            print(f"  -> 成功: {output_filename}")

        except ffmpeg.Error as e:
            # FFmpeg実行エラー
            print(f"  -> 失敗: {input_path.name}", file=sys.stderr)
            print(e.stderr.decode('utf8'), file=sys.stderr) # エラー詳細
            failed_files.append(input_path.name)
        except Exception as e:
            # その他のエラー
            print(f"  -> 予期せぬエラー: {input_path.name} ({e})", file=sys.stderr)
            failed_files.append(input_path.name)

    print("\n--- 処理完了 ---")
    print(f"成功: {converted_count} 件")
    if failed_files:
        print(f"失敗: {len(failed_files)} 件")
        print(f"失敗したファイル: {', '.join(failed_files)}")

# --- 使い方 ---

# 1. このPythonスクリプトを保存します (例: convert.py)
# 2. 以下のパスを環境に合わせて書き換えてください

# MP3ファイルが入っているフォルダのパス
INPUT_DIR = Path(r"C:\Users\hikar\Downloads\運動会　アナウンス - コピー") 
# MP4ファイルを出力したいフォルダのパス
OUTPUT_DIR = Path(r"C:\Users\hikar\Downloads\運動会　アナウンス - コピー") 
# 動画の解像度 (オプション)
RESOLUTION = '1920x1080' # '1280x720' など

# -------------------------------------------------
# スクリプト実行
if __name__ == "__main__":
    # テスト用の入力フォルダ確認
    INPUT_DIR.mkdir(exist_ok=True)
    if not any(p for p in INPUT_DIR.glob("*") if p.suffix.lower() == ".mp3"):
         print(f"注意: {INPUT_DIR.resolve()} にMP3ファイルが見つかりません。")
         print("フォルダにMP3ファイルを入れてから、再度実行してください。")
    else:
        # 実行
        convert_mp3_to_mp4_black(INPUT_DIR, OUTPUT_DIR, RESOLUTION)