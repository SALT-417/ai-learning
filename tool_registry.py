from study_topic_tools import (
    add_study_topic,
    get_study_topics
)

from study_tools import (
    add_study_minutes,
    get_total_study_minutes,
    convert_minutes_to_hours
)


TOOL_REGISTRY = {
    "add_study_minutes": {
        "function": add_study_minutes,
        "argument": "minutes"
    },
    "get_total_study_minutes": {
        "function": get_total_study_minutes,
        "argument": None
    },
    "convert_minutes_to_hours": {
        "function": convert_minutes_to_hours,
        "argument": "minutes"
    },
    "add_study_topic": {
        "function": add_study_topic,
        "argument": "topic"
    },
    "get_study_topics": {
        "function": get_study_topics,
        "argument": None
    }
}