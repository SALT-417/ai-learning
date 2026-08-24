study_minutes = [60, 45, 30, 90, 20, 60, 75]
days = ["月", "火", "水", "木", "金", "土", "日"]


def show_daily_study(days, study_minutes):
    print("=== 1週間の学習記録 ===")

    good_days = 0

    for day, minutes in zip(days, study_minutes):
        print(f"{day}曜日：{minutes}分")

        if minutes >= 60:
            good_days += 1

    return good_days


good_days = show_daily_study(days, study_minutes)

total = sum(study_minutes)
average = total / len(study_minutes)


def show_summary(total, average, good_days):
    print("=== 集計 ===")
    print(f"1週間の合計学習時間：{total}分")
    print(f"1日の平均学習時間：{average:.1f}分")
    print(f"60分以上学習した日：{good_days}日")


show_summary(total, average, good_days)
