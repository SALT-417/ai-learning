import json
from numbers import Number


ANALYSIS_KEYS = {
    "total_minutes",
    "topic_count",
    "topics",
    "most_studied",
    "least_studied"
}

GOAL_PROGRESS_KEYS = {
    "topic",
    "target_minutes",
    "current_minutes",
    "remaining_minutes",
    "achieved"
}


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _is_topic_summary(value):
    if value is None:
        return True

    return (
        isinstance(value, dict)
        and isinstance(value.get("topic"), str)
        and _is_integer(value.get("minutes"))
    )


def _is_analysis_result(result):
    if not isinstance(result, dict):
        return False

    if not ANALYSIS_KEYS.issubset(result):
        return False

    topics = result["topics"]

    return (
        _is_integer(result["total_minutes"])
        and _is_integer(result["topic_count"])
        and isinstance(topics, dict)
        and all(
            isinstance(topic, str)
            and _is_integer(minutes)
            for topic, minutes in topics.items()
        )
        and _is_topic_summary(result["most_studied"])
        and _is_topic_summary(result["least_studied"])
    )


def _is_goal_progress_result(result):
    if not isinstance(result, dict):
        return False

    if not GOAL_PROGRESS_KEYS.issubset(result):
        return False

    return (
        isinstance(result["topic"], str)
        and _is_integer(result["target_minutes"])
        and _is_integer(result["current_minutes"])
        and _is_integer(result["remaining_minutes"])
        and isinstance(result["achieved"], bool)
    )


def _format_topic_summary(value):
    if value is None:
        return "なし"

    return f"{value['topic']}（{value['minutes']}分）"


def _format_analysis_result(result):
    lines = [
        "学習分析：",
        f"合計時間：{result['total_minutes']}分",
        f"トピック数：{result['topic_count']}"
    ]

    if result["topics"]:
        lines.append("トピック別学習時間：")

        for topic, minutes in result["topics"].items():
            lines.append(f"{topic}：{minutes}分")
    else:
        lines.append("トピック別学習時間：なし")

    lines.extend(
        [
            "最多："
            + _format_topic_summary(result["most_studied"]),
            "最少："
            + _format_topic_summary(result["least_studied"])
        ]
    )

    return "\n".join(lines)


def _format_goal_progress_result(result):
    achieved_text = "達成" if result["achieved"] else "未達成"

    return "\n".join(
        [
            "目標進捗：",
            f"トピック：{result['topic']}",
            f"目標：{result['target_minutes']}分",
            f"現在：{result['current_minutes']}分",
            f"残り：{result['remaining_minutes']}分",
            f"達成状態：{achieved_text}"
        ]
    )


def _format_json_fallback(result):
    return json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        default=str
    )


def format_tool_result(result):
    if isinstance(result, str):
        return result

    if _is_analysis_result(result):
        return _format_analysis_result(result)

    if _is_goal_progress_result(result):
        return _format_goal_progress_result(result)

    if (
        isinstance(result, dict)
        and set(result) == {"error"}
        and isinstance(result["error"], str)
    ):
        return result["error"]

    if result is None:
        return "結果なし"

    if isinstance(result, Number) and not isinstance(result, bool):
        return str(result)

    if isinstance(result, (list, dict)):
        return _format_json_fallback(result)

    return str(result)


def format_tool_results(results):
    return "\n".join(
        format_tool_result(result)
        for result in results
    )
