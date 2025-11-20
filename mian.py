# main.py
import sys
from whisper_transcriber import WhisperTranscriber
from pydub import AudioSegment


def print_result(prefix: str, result):
    """
    mlx_whisper.transcribe の戻り値から text を取り出して表示する補助関数
    """
    print(f"\n=== {prefix} の結果 ===")
    if isinstance(result, dict):
        text = result.get("text", "")
        print(text if text else result)
    else:
        # 想定外の型だったらそのまま表示
        print(result)


def main() -> None:
    if len(sys.argv) < 2:
        print("使い方: python main.py <音声ファイルパス>")
        print("例:     python main.py python-audio-output.wav")
        sys.exit(1)

    audio_path = sys.argv[1]

    # WhisperTranscriber のインスタンス作成
    transcriber = WhisperTranscriber()

    # 1) ファイルパスから直接文字起こし
    try:
        result_file = transcriber.transcribe_file(audio_path)
        print_result("transcribe_file", result_file)
    except Exception as e:
        print(f"transcribe_file でエラーが発生しました: {e}")

    # 2) pydub.AudioSegment を使った文字起こし
    try:
        sound = AudioSegment.from_file(audio_path)
        result_segment = transcriber.transcribe_segment(sound)
        print_result("transcribe_segment", result_segment)
    except Exception as e:
        print(f"transcribe_segment でエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
