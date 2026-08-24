from memory_manager import split_history


test_history = [
    {"role": "user", "content": "メッセージ1"},
    {"role": "assistant", "content": "メッセージ2"},
    {"role": "user", "content": "メッセージ3"},
    {"role": "assistant", "content": "メッセージ4"},
    {"role": "user", "content": "メッセージ5"},
    {"role": "assistant", "content": "メッセージ6"},
    {"role": "user", "content": "メッセージ7"},
    {"role": "assistant", "content": "メッセージ8"},
]


old_history, recent_history = split_history(
    test_history,
    recent_count=6
)


print("=== 古い履歴 ===")

for message in old_history:
    print(
        message["role"],
        ":",
        message["content"]
    )


print("=== 直近履歴 ===")

for message in recent_history:
    print(
        message["role"],
        ":",
        message["content"]
    )