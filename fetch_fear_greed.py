import fear_and_greed
import csv
from pathlib import Path

CSV_PATH = Path("data/fear_greed.csv")

def ensure_dir():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

def read_last_update():
    """CSV の最後の 更新日時 を返す。無ければ None。"""
    if not CSV_PATH.exists():
        return None

    with open(CSV_PATH, "r", encoding="cp932") as f:
        rows = list(csv.reader(f))
        if len(rows) <= 1:
            return None
        return rows[-1][0]  # 更新日時

def main():
    ensure_dir()  # ← これが重要！

    result = fear_and_greed.get()

    new_last_update = result.last_update.strftime("%Y-%m-%d %H:%M:%S")
    prev_last_update = read_last_update()

    if prev_last_update == new_last_update:
        print("No update. 更新日時が同じためスキップ:", new_last_update)
        return

    write_header = not CSV_PATH.exists()

    row = [
        new_last_update,
        result.value,
        result.description
    ]

    with open(CSV_PATH, "a", newline="", encoding="cp932", errors="ignore") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["更新日時", "指数", "状態"])
        writer.writerow(row)

    print("Saved:", row)

if __name__ == "__main__":
    main()
