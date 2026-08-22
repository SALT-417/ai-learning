import json
import os
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"
HISTORY_FILE = "chat_history.json"


def generate_reply(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    except requests.RequestException as error:
        print(f"通信エラー：{error}")
        return None


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            messages = json.load(file)

        print("前回の会話履歴を読み込みました。")
        return messages

    messages = [
        {
            "role": "system",
            "content": (
                "あなたはAI学習をサポートする先生です。"
                "現在あなたはOllama上のqwen2.5:3bとして動作しています。"
                "自分自身のモデル名や実行環境について質問された場合は、"
                "Ollama上のqwen2.5:3bであると回答してください。"
                "分からない事実については推測せず、分からないと回答してください。"
            )
        }
    ]

    print("新しい会話を開始します。")
    return messages


def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            messages,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("会話履歴を保存しました。")


def main():
    messages = load_history()

    while True:
        user_input = input("あなた：")

        if user_input == "終了":
            print("チャットを終了します。")
            break

        user_message = {
            "role": "user",
            "content": user_input
        }

        messages.append(user_message)

        assistant_reply = generate_reply(messages)

        if assistant_reply is None:
            messages.pop()
            print("AIから回答を取得できませんでした。")
            continue

        assistant_message = {
            "role": "assistant",
            "content": assistant_reply
        }

        messages.append(assistant_message)

        print(f"AI：{assistant_reply}")

    print("\n=== 保存された会話履歴 ===")

    for message in messages:
        print(f"{message['role']}: {message['content']}")

    save_history(messages)


if __name__ == "__main__":
    main()