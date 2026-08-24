from study_tools import add_study_minutes, get_total_study_minutes
import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def select_tool(user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "あなたはユーザーの依頼を分析し、必要なToolを選ぶAIです。"
                "必ずJSONだけを返してください。"
                "JSON以外の文字は絶対に出力しないでください。"

                "最上位キーは必ずtoolsとanswerの2つです。"
                "最上位にtoolというキーを使ってはいけません。"

                "学習時間を記録する場合："
                '{"tools": ['
                '{"tool": "add_study_minutes", "minutes": 30}'
                '], "answer": null}'

                "合計学習時間を確認する場合："
                '{"tools": ['
                '{"tool": "get_total_study_minutes", "minutes": null}'
                '], "answer": null}'

                "ユーザーの依頼に複数の要求が含まれている場合は、"
                "必要なToolをすべて実行順にtoolsへ追加してください。"

                "例："
                "ユーザー：今日は30分勉強した。合計時間も教えて"
                "回答："
                '{"tools": ['
                '{"tool": "add_study_minutes", "minutes": 30},'
                '{"tool": "get_total_study_minutes", "minutes": null}'
                '], "answer": null}'

                "ユーザー：45分勉強したから記録して、"
                "今までの合計も知りたい"
                "回答："
                '{"tools": ['
                '{"tool": "add_study_minutes", "minutes": 45},'
                '{"tool": "get_total_study_minutes", "minutes": null}'
                '], "answer": null}'

                "Toolが不要な普通の質問の場合："
                '{"tools": [], "answer": "質問への回答"}'

                "ユーザーが学習したことや記録することを"
                "明示していない場合は、"
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


def validate_tools(user_input, tools):
    tool_names = [
        tool.get("tool")
        for tool in tools
    ]

    wants_total = any(
        word in user_input
        for word in [
            "合計",
            "全部で",
            "今まで",
            "これまで"
        ]
    )

    wants_add = any(
        word in user_input
        for word in [
            "勉強した",
            "学習した",
            "記録して"
        ]
    )

    if (
        wants_add
        and "add_study_minutes" not in tool_names
    ):
        match = re.search(r"(\d+)分", user_input)

        if match:
            minutes = int(match.group(1))

            tools.insert(
                0,
                {
                    "tool": "add_study_minutes",
                    "minutes": minutes
                }
            )

    if (
        wants_total
        and "get_total_study_minutes" not in tool_names
    ):
        tools.append(
            {
                "tool": "get_total_study_minutes",
                "minutes": None
            }
        )

    return tools


def execute_tools(tools):
    tool_results = []

    for tool in tools:
        tool_name = tool.get("tool")

        if tool_name == "add_study_minutes":
            minutes = tool.get("minutes")

            if isinstance(minutes, int) and minutes > 0:
                result = add_study_minutes(minutes)
                tool_results.append(result)

            else:
                tool_results.append(
                    "学習時間を記録できませんでした。"
                )

        elif tool_name == "get_total_study_minutes":
            result = get_total_study_minutes()
            tool_results.append(result)

        else:
            tool_results.append(
                f"未対応のToolです：{tool_name}"
            )

    return tool_results


def generate_final_answer(user_input, tool_results):
    combined_result = "\n".join(tool_results)

    messages = [
        {
            "role": "system",
            "content": (
                "あなたはAI学習をサポートするアシスタントです。"
                "Toolの実行結果だけを根拠に最終回答してください。"
                "Tool実行結果にない情報を推測してはいけません。"
                "実行されていない処理を実行済みとして"
                "回答してはいけません。"
                "短く自然な日本語で回答してください。"
                "分数を時間に換算する場合は正確に計算し、勝手に丸めないでください。"
            )
        },
        {
            "role": "user",
            "content": (
                f"ユーザーの依頼：{user_input}\n"
                f"Tool実行結果：\n{combined_result}"
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
        return

    tools = tool_data.get("tools", [])

    tools = validate_tools(
        user_input,
        tools
    )


    if tools:
        tool_results = execute_tools(tools)

        final_answer = generate_final_answer(
            user_input,
            tool_results
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