from tool_selector import execute_tools


tools = [
    {
        "tool": "add_study_topic",
        "topic": "AI Agent"
    },
    {
        "tool": "get_study_topics"
    }
]


results = execute_tools(tools)

for result in results:
    print(result)