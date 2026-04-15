import fear_and_greed
import csv
from pathlib import Path

CSV_PATH = Path("data/fear_greed.csv")

def read_last_update():
    """CSV の最後の 更新日時 を返す。無ければ None。"""
    if not CSV_PATH.exists():
        return None

    with open(CSV_PATH, "r", encoding="cp932") as f:
        rows = list(csv.reader(f))
        if len(rows) <= 1:
            return None  # ヘッダーのみ or 空
        last_row = rows[-1]
        return last_row[0]  # 更新日時 列

def main():
    result = fear_and_greed.get()

    new_last_update = result.last_update.strftime("%Y-%m-%d %H:%M:%S")
    prev_last_update = read_last_update()

    # すでに同じ更新日時ならスキップ
    if prev_last_update == new_last_update:
        print("No update. 更新日時が同じためスキップ:", new_last_update)
        return

    # 初回はヘッダー付きで作成
    write_header = not CSV_PATH.exists()

    row = [
        new_last_update,   # 更新日時
        result.value,      # 指数
        result.description # 状態
    ]

    with open(CSV_PATH, "a", newline="", encoding="cp932", errors="ignore") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["更新日時", "指数", "状態"])
        writer.writerow(row)

    print("Saved:", row)

if __name__ == "__main__":
    main()
