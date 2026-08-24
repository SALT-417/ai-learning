import csv


DETAIL_FILE = "detailed_study_records.csv"


def add_detailed_study(topic, minutes):
    if not isinstance(topic, str) or not topic.strip():
        return "学習トピックを記録できませんでした。"

    if not isinstance(minutes, int) or minutes <= 0:
        return "学習時間を記録できませんでした。"

    topic = topic.strip()

    with open(
        DETAIL_FILE,
        "a",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([topic, minutes])

    return (
        f"「{topic}」を{minutes}分学習した記録を追加しました。"
    )

def get_topic_study_totals():
    totals = {}

    try:
        with open(
            DETAIL_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 2:
                    topic = row[0]
                    minutes = int(row[1])

                    totals[topic] = (
                        totals.get(topic, 0)
                        + minutes
                    )

    except FileNotFoundError:
        return "まだ詳細な学習記録がありません。"

    if not totals:
        return "まだ詳細な学習記録がありません。"

    result_lines = []

    for topic, minutes in totals.items():
        result_lines.append(
            f"{topic}：{minutes}分"
        )

    return "トピック別学習時間：\n" + "\n".join(result_lines)