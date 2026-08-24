from tool_selector import execute_tools


tools = [
    {
        "tool": "get_total_study_minutes",
        "minutes": None
    },
    {
        "tool": "convert_minutes_to_hours",
        "minutes": 527
    }
]


results = execute_tools(tools)

for result in results:
    print(result)