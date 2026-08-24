from tool_selector import execute_tools


tools = [
    {
        "tool": "set_study_goal",
        "topic": "Python",
        "target_minutes": 120
    },
    {
        "tool": "get_goal_progress",
        "topic": "Python"
    }
]


results = execute_tools(tools)

for result in results:
    print(result)