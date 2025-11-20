# lecture04_gui.py
import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
)

from audio_recorder import AudioRecorder
from whisper_transcriber import WhisperTranscriber
from transcript_saver import TranscriptSaver


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("音声録音 & 文字起こし（GUI版）")

        # --- ウィジェット作成 ---
        self.info_label = QLabel(
            "「録音して文字起こし」ボタンを押すと、10秒録音して文字起こしします。"
        )
        self.record_button = QPushButton("録音して文字起こし")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # --- レイアウト ---
        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.record_button)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # --- シグナル接続 ---
        self.record_button.clicked.connect(self.on_record_clicked)

    def on_record_clicked(self):
        """録音～文字起こし～保存までを1ボタンで実行"""

        # ボタン連打防止
        self.record_button.setEnabled(False)

        # ① まず「録音中」に変えて画面を更新
        self.info_label.setText("録音中...（10秒）")
        QApplication.processEvents()  # ← これでラベルの表示を即反映させる

        try:
            # ② 録音（ここで10秒ブロックされる）
            recorder = AudioRecorder()
            recorder.record()

            # ③ 録音が終わったら「文字起こし中」に変更して更新
            self.info_label.setText("文字起こし中...")
            QApplication.processEvents()

            # ④ 文字起こし
            transcriber = WhisperTranscriber()  # __init__ 内の model_repo は修正済み想定
            result = transcriber.transcribe_file(recorder.output_file)

            # 結果が dict で "text" キーを持つ場合を優先
            if isinstance(result, dict) and "text" in result:
                text = result["text"]
            else:
                text = str(result)

            # ⑤ 保存
            saver = TranscriptSaver()
            saved_path = saver.save(text)

            # ⑥ 画面に表示
            self.text_edit.setPlainText(text)
            self.info_label.setText(f"完了！ 保存先: {saved_path}")

        except Exception as e:
            # 何かエラーが起きた場合もラベルに表示しておく
            self.info_label.setText(f"エラーが発生しました: {e}")
        finally:
            # ⑦ ボタンを再度有効化
            self.record_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
