messages = [
    {
        "role": "system",
        "content": "あなたはAI学習をサポートする先生です。"
    },
    {
        "role": "user",
        "content": "PythonでAIを作るには何を勉強すればいいですか？"
    }
]

print(messages)
print(type(messages))

print("=== 1つ目のメッセージ ===")
print(messages[0])
print(type(messages[0]))

print("=== 2つ目のメッセージ ===")
print(messages[1])
print(type(messages[1]))

print("=== メッセージの中身 ===")
print(messages[0]["role"])
print(messages[0]["content"])

print(messages[1]["role"])
print(messages[1]["content"])

assistant_message = {
    "role": "assistant",
    "content": "まずPythonの基礎、API、JSONについて学習しましょう。"
}

messages.append(assistant_message)

print("=== AIの返答を追加 ===")
print(messages)

print("=== 会話履歴 ===")

for message in messages:
    role = message["role"]
    content = message["content"]

    print(f"{role}: {content}")