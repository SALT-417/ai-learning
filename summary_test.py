from memory_manager import summarize_history


old_history = [
    {
        "role": "user",
        "content": "Pythonを重点的に勉強したいです。"
    },
    {
        "role": "assistant",
        "content": "Pythonを中心に学習を進めましょう。"
    },
    {
        "role": "user",
        "content": "特にAI開発に使えるようになりたいです。"
    },
    {
        "role": "assistant",
        "content": "PythonとAI開発を組み合わせて学ぶと良いです。"
    }
]


summary = summarize_history(old_history)

print("=== 要約 ===")
print(summary)