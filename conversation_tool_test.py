from tool_selector import select_tool
import json


conversation_history = [
    {
        "role": "user",
        "content": "今までの合計学習時間を教えて"
    },
    {
        "role": "assistant",
        "content": "これまでの合計学習時間は527分です。"
    }
]


user_input = "それは何時間何分ですか？"

result = select_tool(
    user_input,
    conversation_history
)

print("AIの判断:", result)

tool_data = json.loads(result)

tools = tool_data.get("tools", [])

print("選択されたTool:", tools)