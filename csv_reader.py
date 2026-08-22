import csv


def show_daily_study(days, study_minutes):
    print("=== CSVから読み込んだ学習記録 ===")

    good_days = 0

    for day, minutes in zip(days, study_minutes):
        print(f"{day}曜日：{minutes}分")

        if minutes >= 60:
            good_days += 1

    return good_days


def show_summary(study_minutes, good_days):
    total = sum(study_minutes)
    average = total / len(study_minutes)

    print("=== 集計 ===")
    print(f"1週間の合計学習時間：{total}分")
    print(f"1日の平均学習時間：{average:.1f}分")
    print(f"60分以上学習した日：{good_days}日")


days = []
study_minutes = []

try:
    with open("study_data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            day = row["day"]
            minutes = int(row["minutes"])

            days.append(day)
            study_minutes.append(minutes)

except FileNotFoundError:
    print("エラー：CSVファイルが見つかりません。")

except ValueError as error:
    print("エラー：学習時間には数字を入力してください。")
    print(f"詳細：{error}")

else:
    if not study_minutes:
        print("エラー：学習データがありません。")
    else:
        good_days = show_daily_study(days, study_minutes)
        show_summary(study_minutes, good_days)