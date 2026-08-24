import csv


TOPIC_FILE = "study_topics.csv"


def add_study_topic(topic):
    if not isinstance(topic, str) or not topic.strip():
        return "学習トピックを記録できませんでした。"

    topic = topic.strip()

    with open(
        TOPIC_FILE,
        "a",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([topic])

    return f"「{topic}」を学習トピックとして記録しました。"


def get_study_topics():
    topics = []

    try:
        with open(
            TOPIC_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            reader = csv.reader(file)

            for row in reader:
                if row:
                    topics.append(row[0])

    except FileNotFoundError:
        return "まだ学習トピックの記録がありません。"

    if not topics:
        return "まだ学習トピックの記録がありません。"

    return "これまでの学習トピック：" + "、".join(topics)