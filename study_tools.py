import csv


STUDY_FILE = "study_records.csv"


def add_study_minutes(minutes):
    with open(
        STUDY_FILE,
        "a",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([minutes])

    return f"{minutes}分の学習を記録しました。"


if __name__ == "__main__":
    result = add_study_minutes(60)
    print(result)

def get_total_study_minutes():
    total = 0

    try:
        with open(STUDY_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if row:
                    total += int(row[0])

    except FileNotFoundError:
        return "まだ学習記録がありません。"

    return f"これまでの合計学習時間は{total}分です。"

def convert_minutes_to_hours(minutes):
    if not isinstance(minutes, int) or minutes < 0:
        return "正しい分数を指定してください。"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    return (
        f"{minutes}分は"
        f"{hours}時間{remaining_minutes}分です。"
    )