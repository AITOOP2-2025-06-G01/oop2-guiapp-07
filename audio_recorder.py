# audio_recorder.py
import ffmpeg

class AudioRecorder:
    """
    FFmpeg-python を使って 10 秒間、マイク入力を録音して WAV (PCM 16bit/44.1kHz/モノラル) で保存する。
    ※ macOS の avfoundation を前提に ':0' (音声デバイスID 0) を使用
    """
    def __init__(self):
        self.duration = 10
        self.output_file = 'python-audio-output.wav'

    def record(self) -> None:
        try:
            print(f"{self.duration}秒間、マイクからの録音を開始します...")
            (
                ffmpeg
                .input(':0', format='avfoundation', t=self.duration)  # macOS の例
                .output(self.output_file, acodec='pcm_s16le', ar='44100', ac=1)
                .run(overwrite_output=True)
            )
            print(f"録音が完了しました。{self.output_file}に保存されました。")
        except ffmpeg.Error as e:
            # ffmpeg 実行時の標準エラーをそのまま表示
            print(f"エラーが発生しました: {e.stderr.decode(errors='ignore')}")
        except Exception as e:
            print(f"予期せぬエラー: {e}")
