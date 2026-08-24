from tool_selector import (
    select_tool,
    validate_tools,
    execute_tools
)
from response_formatter import format_tool_results

import json

from memory_manager import (
    save_history,
    load_history,
    split_history,
    summarize_history
)


def main():
    conversation_history = load_history()

    print("AI学習エージェントを開始します。")
    print("終了するには「終了」と入力してください。")

    while True:
        user_input = input("あなた：")

        if user_input == "終了":
            print("AI学習エージェントを終了します。")
            break

        old_history, recent_history = split_history(
            conversation_history,
            recent_count=6
        )

        memory_summary = summarize_history(
            old_history
        )

        context_history = []

        if memory_summary:
            context_history.append(
                {
                    "role": "system",
                    "content": (
                        "過去の会話から作成した長期記憶です。"
                        "必要な場合だけ参考にしてください。\n"
                        f"{memory_summary}"
                    )
                }
            )

        context_history.extend(recent_history)

        result = select_tool(
            user_input,
            context_history
        )


        if result is None:
            print(
                "AI：AIとの通信に失敗したため、"
                "処理を実行できませんでした。"
            )
            continue

        try:
            tool_data = json.loads(result)

        except json.JSONDecodeError:
            print(
                "AI：AIの返答を解析できませんでした。"
            )
            continue

        if not isinstance(tool_data, dict):
            print(
                "AI：AIの返答形式が正しくありませんでした。"
            )
            continue

        tools = tool_data.get("tools", [])
        answer = tool_data.get("answer")

        if (
            not isinstance(tools, list)
            or not all(
                isinstance(tool, dict)
                for tool in tools
            )
        ):
            print(
                "AI：AIの返答形式が正しくありませんでした。"
            )
            continue

        tools = validate_tools(
            user_input,
            tools,
            context_history
        )

        if (
            not tools
            and not isinstance(answer, str)
        ):
            print(
                "AI：有効な回答を取得できませんでした。"
            )
            continue

        conversation_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        if tools:
            tool_results = execute_tools(tools)
            final_answer = format_tool_results(
                tool_results
            )

            print("AI：", final_answer)

            conversation_history.append(
                {
                    "role": "assistant",
                    "content": final_answer
                }
            )

            save_history(conversation_history)

        else:
            print("AI：", answer)

            conversation_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            save_history(conversation_history)


if __name__ == "__main__":
    main()
