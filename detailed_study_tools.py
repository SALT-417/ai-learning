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

def get_study_analysis_data():
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
        return {
            "total_minutes": 0,
            "topics": {}
        }

    total_minutes = sum(totals.values())

    return {
        "total_minutes": total_minutes,
        "topics": totals
    }    


def get_study_analysis_facts():
    data = get_study_analysis_data()

    topics = data["topics"]
    total_minutes = data["total_minutes"]

    if not topics:
        return {
            "total_minutes": 0,
            "topic_count": 0,
            "topics": {},
            "most_studied": None,
            "least_studied": None
        }

    most_studied_topic = max(
        topics,
        key=topics.get
    )

    least_studied_topic = min(
        topics,
        key=topics.get
    )

    return {
        "total_minutes": total_minutes,
        "topic_count": len(topics),
        "topics": topics,
        "most_studied": {
            "topic": most_studied_topic,
            "minutes": topics[most_studied_topic]
        },
        "least_studied": {
            "topic": least_studied_topic,
            "minutes": topics[least_studied_topic]
        }
    }