from tool_selector import select_tool, validate_tools
import json


test_inputs = [
    "Pythonを120分勉強する目標にしたい",
    "Pythonの目標まであとどれくらい？"
]


for user_input in test_inputs:
    print("=" * 50)
    print("入力:", user_input)

    result = select_tool(user_input)

    print("AIの判断:", result)

    tool_data = json.loads(result)

    tools = tool_data.get("tools", [])

    validated_tools = validate_tools(
        user_input,
        tools
    )

    print("検証後:", validated_tools)