from study_topic_tools import (
    add_study_topic,
    get_study_topics
)

from study_tools import (
    add_study_minutes,
    get_total_study_minutes,
    convert_minutes_to_hours
)

from detailed_study_tools import (
    add_detailed_study,
    get_topic_study_totals,
    get_study_analysis_facts
)

from study_goal_tools import (
    set_study_goal,
    get_goal_progress
)

TOOL_REGISTRY = {
    "add_study_minutes": {
        "function": add_study_minutes,
        "arguments": ["minutes"]
    },
    "get_total_study_minutes": {
        "function": get_total_study_minutes,
        "arguments": []
    },
    "convert_minutes_to_hours": {
        "function": convert_minutes_to_hours,
        "arguments": ["minutes"]
    },
    "add_study_topic": {
        "function": add_study_topic,
        "arguments": ["topic"]
    },
    "get_study_topics": {
        "function": get_study_topics,
        "arguments": []
    },
    "add_detailed_study": {
        "function": add_detailed_study,
        "arguments": [
            "topic",
            "minutes"
        ]
    },
    "get_topic_study_totals": {
        "function": get_topic_study_totals,
        "arguments": []
    },
    "get_study_analysis_facts": {
        "function": get_study_analysis_facts,
        "arguments": []
    },
    "set_study_goal": {
        "function": set_study_goal,
        "arguments": [
            "topic",
            "target_minutes"
        ]
    },
    "get_goal_progress": {
        "function": get_goal_progress,
        "arguments": [
            "topic"
        ]
    }
}