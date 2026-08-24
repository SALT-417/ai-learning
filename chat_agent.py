from tool_selector import (
    select_tool,
    validate_tools,
    execute_tools,
    generate_final_answer
)

import json

from memory_manager import save_history, load_history

def main():
    conversation_history = load_history()

    print("AI学習エージェントを開始します。")
    print("終了するには「終了」と入力してください。")

    while True:
        user_input = input("あなた：")

        if user_input == "終了":
            print("AI学習エージェントを終了します。")
            break

        result = select_tool(
            user_input,
            conversation_history
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

        tools = tool_data.get("tools", [])

        tools = validate_tools(
            user_input,
            tools,
            conversation_history
        )

        conversation_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        if tools:
            tool_results = execute_tools(tools)

            final_answer = generate_final_answer(
                user_input,
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
            answer = tool_data.get(
                "answer",
                "回答を取得できませんでした。"
            )

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