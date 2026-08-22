from study_tools import add_study_minutes, get_total_study_minutes
import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def select_tool(user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "あなたはユーザーの依頼を分類するAIです。"
                "必ずJSONだけで回答してください。"
                "JSON以外の文字は絶対に出力しないでください。"

                "学習時間を記録する場合："
                '{"tool": "add_study_minutes", "minutes": 数字, "answer": null}'

                "合計学習時間を確認する場合："
                '{"tool": "get_total_study_minutes", "minutes": null, "answer": null}'

                "それ以外の普通の質問の場合："
                '{"tool": null, "minutes": null, "answer": "質問への回答"}'

                "ユーザーが明示的に学習時間を記録したいと言っていない場合、"
                "add_study_minutesを選んではいけません。"
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "format": "json"
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def generate_final_answer(user_input, tool_result):
    messages = [
        {
            "role": "system",
            "content": (
                "あなたはAI学習をサポートするアシスタントです。"
                "ユーザーの依頼とToolの実行結果をもとに、"
                "短く自然な日本語で最終回答してください。"
                "Toolが成功している場合は、"
                "実行結果を正確に伝えてください。"
            )
        },
        {
            "role": "user",
            "content": (
                f"ユーザーの依頼：{user_input}\n"
                f"Tool実行結果：{tool_result}"
            )
        }
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def main():
    user_input = input("あなた：")

    result = select_tool(user_input)

    try:
        tool_data = json.loads(result)

    except json.JSONDecodeError:
        print("AIの返答をJSONとして解析できませんでした。")

    else:
        tool_name = tool_data.get("tool")

        if tool_name == "add_study_minutes":
            minutes = tool_data.get("minutes")

            tool_result = add_study_minutes(minutes)

            final_answer = generate_final_answer(
                user_input,
                tool_result
            )

            print("=== AIの最終回答 ===")
            print(final_answer)

        elif tool_name == "get_total_study_minutes":
            tool_result = get_total_study_minutes()

            final_answer = generate_final_answer(
                user_input,
                tool_result
            )

            print("=== AIの最終回答 ===")
            print(final_answer)

        else:
            print("=== AIの回答 ===")
            print(
                tool_data.get(
                    "answer",
                    "回答を取得できませんでした。"
                )
            )


if __name__ == "__main__":
    main()

user_input = input("あなた：")

result = select_tool(user_input)

try:
    tool_data = json.loads(result)

except json.JSONDecodeError:
    print("AIの返答をJSONとして解析できませんでした。")

else:
    tool_name = tool_data.get("tool")

    if tool_name == "add_study_minutes":
        minutes = tool_data.get("minutes")

        tool_result = add_study_minutes(minutes)

        final_answer = generate_final_answer(
            user_input,
            tool_result
        )

        print("=== AIの最終回答 ===")
        print(final_answer)

    elif tool_name == "get_total_study_minutes":
        tool_result = get_total_study_minutes()

        final_answer = generate_final_answer(
            user_input,
            tool_result
        )

        print("=== AIの最終回答 ===")
        print(final_answer)

    else:
        print("=== AIの回答 ===")
        print(
            tool_data.get(
                "answer",
                "回答を取得できませんでした。"
            )
        )