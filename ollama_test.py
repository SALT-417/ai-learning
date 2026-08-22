import requests

user_input = input("あなた：")

url = "http://localhost:11434/api/chat"

payload = {
    "model": "qwen2.5:3b",
    "messages": [
        {
            "role": "user",
            "content": user_input
        }
    ],
    "stream": False
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    assistant_reply = data["message"]["content"]

    print("=== AIの回答 ===")
    print(assistant_reply)

except requests.RequestException as error:
    print(f"通信エラー：{error}")