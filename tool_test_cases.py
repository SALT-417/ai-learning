from tool_selector import select_tool, validate_tools
import json


test_cases = [
    {
        "input": "今までの合計学習時間を教えて",
        "expected": ["get_total_study_minutes"]
    },
    {
        "input": "今日は20分勉強した",
        "expected": ["add_study_minutes"]
    },
    {
        "input": "今日は20分勉強した。合計時間も教えて",
        "expected": [
            "add_study_minutes",
            "get_total_study_minutes"
        ]
    },
    {
        "input": "45分学習したから記録して、これまでの合計も知りたい",
        "expected": [
            "add_study_minutes",
            "get_total_study_minutes"
        ]
    },
    {
        "input": "Pythonとは何ですか？",
        "expected": []
    },
    {
        "input": "今日25分やったから追加して、トータルも教えて",
        "expected": [
            "add_study_minutes",
            "get_total_study_minutes"
        ]
    },
    {
        "input": "さっき15分勉強したので記録お願いします",
        "expected": [
            "add_study_minutes"
        ]
    },
    {
        "input": "累計の勉強時間を知りたい",
        "expected": [
            "get_total_study_minutes"
        ]
    },
    {
        "input": "30分だけ追加して",
        "expected": [
            "add_study_minutes"
        ]
    },
    {
        "input": "今日は勉強していません",
        "expected": []
    },
    {
        "input": "合計は気になるけど今は記録しないで",
        "expected": [
            "get_total_study_minutes"
        ]
    }
]


passed = 0


for case in test_cases:
    user_input = case["input"]
    expected = case["expected"]

    print("=" * 50)
    print("入力:", user_input)

    result = select_tool(user_input)

    try:
        tool_data = json.loads(result)

    except json.JSONDecodeError:
        print("結果: FAIL")
        print("理由: JSON解析エラー")
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
        print("期待との差分を確認してください。")


print("=" * 50)
print(
    f"テスト結果: {passed}/{len(test_cases)} PASS"
)