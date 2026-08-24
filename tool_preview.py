from tool_selector import select_tool, validate_tools
import json


user_input = "今日は10分勉強した。合計時間も教えて"

result = select_tool(user_input)

print("DEBUG（AIの判断）:", result)

tool_data = json.loads(result)

tools = tool_data.get("tools", [])

tools = validate_tools(user_input, tools)

print("DEBUG（検証後）:", tools)