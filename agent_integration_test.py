from tool_selector import select_tool, validate_tools
import json


test_cases = [
    {
        "input": "今までの合計学習時間を教えて",
        "expected": [
            "get_total_study_minutes"
        ]
    },
    {
        "input": "今日はRAGを勉強した",
        "expected": [
            "add_study_topic"
        ]
    },
    {
        "input": "今日はPythonを20分勉強した",
        "expected": [
            "add_detailed_study"
        ]
    },
    {
        "input": "トピック別の学習時間を教えて",
        "expected": [
            "get_topic_study_totals"
        ]
    },
    {
        "input": "今の学習状況を分析して",
        "expected": [
            "get_study_analysis_facts"
        ]
    },
    {
        "input": "Pythonを120分勉強する目標にしたい",
        "expected": [
            "set_study_goal"
        ]
    },
    {
        "input": "Pythonの目標まであとどれくらい？",
        "expected": [
            "get_goal_progress"
        ]
    },
    {
        "input": (
            "今日はPythonを20分勉強した。"
            "目標まであとどれくらい？"
        ),
        "expected": [
            "add_detailed_study",
            "get_goal_progress"
        ]
    },
    {
        "input": "Pythonとは何ですか？",
        "expected": []
    }
]


passed = 0


for case in test_cases:
    user_input = case["input"]
    expected = case["expected"]

    print("=" * 60)
    print("入力:", user_input)

    result = select_tool(user_input)

    if result is None:
        print("結果: FAIL")
        print("理由: AIとの通信失敗")
        continue

    try:
        tool_data = json.loads(result)

    except json.JSONDecodeError:
        print("結果: FAIL")
        print("理由: JSON解析エラー")
        print("AIの返答:", result)
        continue

    tools = tool_data.get("tools", [])

    validated_tools = validate_tools(
        user_input,
        tools
    )

    actual = [
        tool.get("tool")
        for tool in validated_tools
    ]

    print("期待:", expected)
    print("実際:", actual)

    if actual == expected:
        print("結果: PASS")
        passed += 1

    else:
        print("結果: FAIL")
        print("AIの元の返答:", result)


print("=" * 60)
print(
    f"統合テスト結果: "
    f"{passed}/{len(test_cases)} PASS"
)