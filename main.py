# main.py
from transcript_saver import TranscriptSaver

def main():
    # 保存したいテキスト（適当にサンプル）
    text = "これはサンプルテキストです。\n文字起こし結果がここに入ります。"

    # TranscriptSaver を使って保存
    saver = TranscriptSaver()
    saved_path = saver.save(text)

    # 保存先確認
    print("保存が完了しました。")
    print("保存先:", saved_path)

if __name__ == "__main__":
    main()
