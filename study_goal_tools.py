import csv
from detailed_study_tools import get_study_analysis_data
from storage_paths import get_data_path

GOAL_FILE = "study_goals.csv"


def set_study_goal(topic, target_minutes):
    if not isinstance(topic, str) or not topic.strip():
        return "学習目標を設定できませんでした。"

    if not isinstance(target_minutes, int) or target_minutes <= 0:
        return "目標時間を設定できませんでした。"

    topic = topic.strip()

    goals = {}

    try:
        with open(
            get_data_path(GOAL_FILE),
            "r",
            encoding="utf-8"
        ) as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 2:
                    goals[row[0]] = int(row[1])

    except FileNotFoundError:
        pass

    goals[topic] = target_minutes

    with open(
        get_data_path(GOAL_FILE),
        "w",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.writer(file)

        for goal_topic, minutes in goals.items():
            writer.writerow(
                [goal_topic, minutes]
            )

    return (
        f"「{topic}」の学習目標を"
        f"{target_minutes}分に設定しました。"
    )

def get_goal_progress(topic):
    if not isinstance(topic, str) or not topic.strip():
        return {
            "error": "学習トピックを指定してください。"
        }

    topic = topic.strip()

    goals = {}

    try:
        with open(
            get_data_path(GOAL_FILE),
            "r",
            encoding="utf-8"
        ) as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 2:
                    goals[row[0]] = int(row[1])

    except FileNotFoundError:
        return {
            "error": "学習目標がまだ設定されていません。"
        }

    if topic not in goals:
        return {
            "error": f"「{topic}」の学習目標は設定されていません。"
        }

    study_data = get_study_analysis_data()

    current_minutes = study_data["topics"].get(
        topic,
        0
    )

    target_minutes = goals[topic]

    remaining_minutes = max(
        target_minutes - current_minutes,
        0
    )

    achieved = current_minutes >= target_minutes

    return {
        "topic": topic,
        "target_minutes": target_minutes,
        "current_minutes": current_minutes,
        "remaining_minutes": remaining_minutes,
        "achieved": achieved
    }
