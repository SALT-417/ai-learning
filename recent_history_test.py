from memory_manager import get_recent_history


test_history = [
    {"role": "user", "content": "メッセージ1"},
    {"role": "assistant", "content": "メッセージ2"},
    {"role": "user", "content": "メッセージ3"},
    {"role": "assistant", "content": "メッセージ4"},
    {"role": "user", "content": "メッセージ5"},
    {"role": "assistant", "content": "メッセージ6"},
    {"role": "user", "content": "メッセージ7"},
    {"role": "assistant", "content": "メッセージ8"},
    {"role": "user", "content": "メッセージ9"},
    {"role": "assistant", "content": "メッセージ10"},
]


recent_history = get_recent_history(
    test_history,
    max_messages=6
)


for message in recent_history:
    print(
        message["role"],
        ":",
        message["content"]
    )