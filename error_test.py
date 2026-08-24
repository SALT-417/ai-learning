from tool_selector import execute_tools


tools = [
    {
        "tool": "unknown_tool",
        "minutes": None
    }
]


results = execute_tools(tools)

print(results)