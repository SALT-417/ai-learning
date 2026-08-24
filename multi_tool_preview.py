from tool_selector import select_tool, validate_tools
import json


user_input = (
    "今日はPythonを20分勉強した。"
    "目標まであとどれくらい？"
)

result = select_tool(user_input)

print("AIの判断:", result)

tool_data = json.loads(result)

tools = tool_data.get("tools", [])

validated_tools = validate_tools(
    user_input,
    tools
)

print("検証後:", validated_tools)