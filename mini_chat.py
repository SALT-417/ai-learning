messages = [
    {
        "role": "system",
        "content": "あなたはAI学習をサポートする先生です。"
    }
]

user_input = input("あなた：")

user_message = {
    "role": "user",
    "content": user_input
}

messages.append(user_message)

if "Python" in user_input:
    assistant_reply = "Pythonは、AI開発でもよく使われるプログラミング言語です。"

elif "AI" in user_input:
    assistant_reply = "AIを学ぶには、Python、データ処理、APIなどを順番に学ぶとよいでしょう。"

else:
    assistant_reply = "その質問については、まだうまく回答できません。"

assistant_message = {
    "role": "assistant",
    "content": assistant_reply
}

messages.append(assistant_message)

print("=== 会話履歴 ===")

for message in messages:
    print(f"{message['role']}: {message['content']}")