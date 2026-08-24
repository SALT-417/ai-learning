import json
import requests
from storage_paths import get_data_path

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"

MEMORY_FILE = "conversation_history.json"


def save_history(conversation_history):
    with open(
        get_data_path(MEMORY_FILE),
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            conversation_history,
            file,
            ensure_ascii=False,
            indent=2
        )


def load_history():
    try:
        with open(
            get_data_path(MEMORY_FILE),
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def get_recent_history(
    conversation_history,
    max_messages=6
):
    return conversation_history[-max_messages:]


def split_history(
    conversation_history,
    recent_count=6
):
    if len(conversation_history) <= recent_count:
        return [], conversation_history

    old_history = conversation_history[:-recent_count]
    recent_history = conversation_history[-recent_count:]

    return old_history, recent_history


def summarize_history(old_history):
    if not old_history:
        return ""

    history_text = ""

    for message in old_history:
        role = message.get("role", "")
        content = message.get("content", "")

        history_text += (
            f"{role}: {content}\n"
        )

    messages = [
        {
            "role": "system",
            "content": (
                "あなたは会話履歴から長期記憶を作成するAIです。"
                "会話そのものを書き直してはいけません。"
                "重要な事実だけを短く要約してください。"

                "必ず次のルールを守ってください。"
                "・1〜3文の日本語だけで回答する"
                "・userやassistantなどの役割名を書かない"
                "・会話文をそのまま引用しない"
                "・同じ内容を繰り返さない"
                "・ユーザーの目標、希望、重要な事実を優先する"
                "・会話に存在しない情報を追加しない"

                "例："
                "会話："
                "ユーザー：Pythonを重点的に勉強したい"
                "アシスタント：Pythonを中心に進めましょう"
                "ユーザー：AI開発に使えるようになりたい"
                "要約："
                "ユーザーはPythonを重点的に学び、"
                "AI開発に活用できるようになりたい。"

                "回答には要約本文だけを出力してください。"

                "アシスタントが過去に話したTool名、関数名、"
                "内部処理、エラーメッセージは長期記憶に残してはいけません。"
                "長期記憶には主にユーザー自身が話した目標、希望、"
                "継続的に役立つ事実を残してください。"
            )
        },
        {
            "role": "user",
            "content": (
                "次の会話を要約してください。\n\n"
                f"{history_text}"
            )
        }
    ]

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
        print("会話履歴の要約に失敗しました。")
        print("詳細:", error)

        return ""
