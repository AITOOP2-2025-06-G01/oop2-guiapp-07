# lecture04_main.py
from audio_recorder import AudioRecorder
from whisper_transcriber import WhisperTranscriber
from transcript_saver import TranscriptSaver

def main():
    # 1) 10秒録音（audio_recorder.py）
    recorder = AudioRecorder()
    recorder.record()  # 出力ファイルは recorder.output_file に保存される（既定: 'python-audio-output.wav'）

    # 2) 文字起こし（whisper_transcriber.py）
    transcriber = WhisperTranscriber()  # 既定モデル: "whisper-base-mlx"
    result = transcriber.transcribe_file(recorder.output_file)

    # 3) 文字列抽出（結果が dict で "text" を含む想定。無い場合のフォールバックあり）
    text = result["text"] if isinstance(result, dict) and "text" in result else str(result)

    # 4) 保存（上書きしない）（transcript_saver.py）
    saver = TranscriptSaver()  # 既定: transcripts/transcript.txt を基準に連番で保存
    saved_path = saver.save(text)

    # 5) 確認表示
    print("\n--- 文字起こし結果 ---")
    print(text)
    print("\n保存先:", saved_path)

if __name__ == "__main__":
    main()