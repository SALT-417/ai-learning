from memory_manager import save_history, load_history


test_history = [
    {
        "role": "user",
        "content": "こんにちは"
    },
    {
        "role": "assistant",
        "content": "こんにちは。"
    }
]


save_history(test_history)

loaded_history = load_history()

print(loaded_history)