# whisper_transcriber.py
import mlx_whisper
from pydub import AudioSegment
import numpy as np

class WhisperTranscriber:
    """
    MLX Whisper を用いた文字起こし（ファイル入力／AudioSegment入力）
    """

    def __init__(self, model_repo: str = "mlx-community/whisper-base-mlx"):
        self.model_repo = model_repo

    def transcribe_file(self, audio_file_path: str):
        """
        音声ファイルパスを指定して文字起こし
        """
        return mlx_whisper.transcribe(
            audio_file_path, path_or_hf_repo=self.model_repo
        )

    def transcribe_segment(self, sound: AudioSegment):
        """
        pydub.AudioSegment を受け取り、前処理して文字起こし
        """
        # 前処理：16kHz / 16bit / モノラル
        if sound.frame_rate != 16000:
            sound = sound.set_frame_rate(16000)
        if sound.sample_width != 2:
            sound = sound.set_sample_width(2)
        if sound.channels != 1:
            sound = sound.set_channels(1)

        # Metal(GPU)が扱える Numpy Array へ変換（float32, -1.0〜1.0）
        arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0

        return mlx_whisper.transcribe(
            arr, path_or_hf_repo=self.model_repo
        )