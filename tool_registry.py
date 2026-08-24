from study_tools import (
    add_study_minutes,
    get_total_study_minutes,
    convert_minutes_to_hours
)


TOOL_REGISTRY = {
    "add_study_minutes": {
        "function": add_study_minutes,
        "requires_minutes": True
    },
    "get_total_study_minutes": {
        "function": get_total_study_minutes,
        "requires_minutes": False
    },
    "convert_minutes_to_hours": {
        "function": convert_minutes_to_hours,
        "requires_minutes": True
    }
}