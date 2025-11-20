# transcript_saver.py
from pathlib import Path

class TranscriptSaver:
    """
    文字起こしされた文字列をテキストファイルに保存する。
    既存ファイルがある場合は上書きせず、_001, _002... の連番を付けて保存する。
    """

    def __init__(self, output_dir: str = "transcripts", default_filename: str = "transcript.txt"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.default_filename = default_filename

    def _unique_path(self, path: Path) -> Path:
        if not path.exists():
            return path
        stem, suffix = path.stem, path.suffix
        i = 1
        while True:
            candidate = path.with_name(f"{stem}_{i:03d}{suffix}")
            if not candidate.exists():
                return candidate
            i += 1

    def save(self, text: str, filename: str | None = None) -> str:
        """
        text: 保存する文字列
        filename: 明示的に指定がない場合は default_filename を使用
        return: 実際に保存したファイルパス（文字列）
        """
        base = self.output_dir / (filename or self.default_filename)
        out_path = self._unique_path(base)
        out_path.write_text(text, encoding="utf-8")
        return str(out_path)
