from tool_selector import execute_tools


tools = [
    {
        "tool": "add_detailed_study",
        "topic": "Tool Registry",
        "minutes": 25
    },
    {
        "tool": "get_topic_study_totals"
    }
]


results = execute_tools(tools)

for result in results:
    print(result)