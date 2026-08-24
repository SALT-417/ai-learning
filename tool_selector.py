from tool_registry import TOOL_REGISTRY
from study_tools import (
    add_study_minutes,
    get_total_study_minutes,
    convert_minutes_to_hours
)
import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def select_tool(user_input, conversation_history=None):
    if conversation_history is None:
        conversation_history = []
    
    messages = [
        {
            "role": "system",
            "content": (
                "あなたはユーザーの依頼を分析し、必要なToolを選ぶAIです。"
                "必ずJSONだけを返してください。"
                "JSON以外の文字は絶対に出力しないでください。"

                "最上位キーは必ずtoolsとanswerの2つです。"
                "最上位にtoolというキーを使ってはいけません。"

                "学習時間を記録する場合："
                '{"tools": ['
                '{"tool": "add_study_minutes", "minutes": 30}'
                '], "answer": null}'

                "合計学習時間を確認する場合："
                '{"tools": ['
                '{"tool": "get_total_study_minutes", "minutes": null}'
                '], "answer": null}'

                "ユーザーの依頼に複数の要求が含まれている場合は、"
                "必要なToolをすべて実行順にtoolsへ追加してください。"
                "過去の会話履歴も参考にしてください。"
                "現在のユーザー発言だけでは意味が不明な場合は、"
                "直前までの会話からユーザーの意図を判断してください。"
                
                "例："
                "ユーザー：今日は30分勉強した。合計時間も教えて"
                "回答："
                '{"tools": ['
                '{"tool": "add_study_minutes", "minutes": 30},'
                '{"tool": "get_total_study_minutes", "minutes": null}'
                '], "answer": null}'

                "分を時間と分に換算する場合："
                '{"tools": ['
                '{"tool": "convert_minutes_to_hours", "minutes": 527}'
                '], "answer": null}'

                "会話例："
                "ユーザー：今までの合計学習時間を教えて"
                "アシスタント：これまでの合計学習時間は527分です。"
                "ユーザー：それは何時間何分ですか？"
                "回答："
                '{"tools": ['
                '{"tool": "convert_minutes_to_hours", "minutes": 527}'
                '], "answer": null}'

                "ユーザー：45分勉強したから記録して、"
                "今までの合計も知りたい"
                "回答："
                '{"tools": ['
                '{"tool": "add_study_minutes", "minutes": 45},'
                '{"tool": "get_total_study_minutes", "minutes": null}'
                '], "answer": null}'

                "Toolが不要な普通の質問の場合："
                '{"tools": [], "answer": "質問への回答"}'

                "ユーザーが学習したことや記録することを"
                "明示していない場合は、"
                "add_study_minutesを選んではいけません。"
                "数値計算が必要な場合は、計算結果を慎重に確認してください。"
                "分を時間と分に換算する場合は、"
                "60で割った商を時間、余りを分として正確に回答してください。"
                "Toolが不要な普通の質問では、answerにユーザーへの自然な回答を書いてください。"
                "answerの中でTool名、関数名、JSON、内部処理について説明してはいけません。"
                "add_study_minutes、get_total_study_minutes、"
                "convert_minutes_to_hoursなどの内部名をユーザーに見せてはいけません。"
                "学習方法について相談された場合は、学習相談として普通に回答してください。"

                "Toolが不要な普通の質問に回答するときも、"
                "過去の会話履歴を必ず参考にしてください。"
                "ユーザーがすでに伝えた目標や希望を、"
                "もう一度質問してはいけません。"
                "過去の会話から回答できる場合は、"
                "その情報を使って具体的に回答してください。"

                "学習した内容やテーマを記録する場合："
                '{"tools": ['
                '{"tool": "add_study_topic", "topic": "RAG"}'
                '], "answer": null}'

                "これまで学習したトピックを確認する場合："
                '{"tools": ['
                '{"tool": "get_study_topics", "topic": null}'
                '], "answer": null}'

                "学習時間ではなく、何を勉強したかを記録したい場合は"
                "add_study_topicを選んでください。"

                "例："
                "ユーザー：今日はRAGを勉強した"
                "回答："
                '{"tools": ['
                '{"tool": "add_study_topic", "topic": "RAG"}'
                '], "answer": null}'

                "ユーザー：これまで何を勉強した？"
                "回答："
                '{"tools": ['
                '{"tool": "get_study_topics", "topic": null}'
                '], "answer": null}'

                "学習トピックと学習時間の両方が明示されている場合は、"
                "add_detailed_studyを選んでください。"

                "この場合、add_study_minutesやadd_study_topicを"
                "同時に選んではいけません。"

                "例："
                "ユーザー：今日はPythonを30分勉強した"
                "回答："
                '{"tools": ['
                '{"tool": "add_detailed_study", '
                '"topic": "Python", '
                '"minutes": 30}'
                '], "answer": null}'

                "例："
                "ユーザー：RAGを45分学習した"
                "回答："
                '{"tools": ['
                '{"tool": "add_detailed_study", '
                '"topic": "RAG", '
                '"minutes": 45}'
                '], "answer": null}'

                "トピック別の学習時間を確認する場合は、"
                "get_topic_study_totalsを選んでください。"

                "例："
                "ユーザー：トピック別の学習時間を教えて"
                "回答："
                '{"tools": ['
                '{"tool": "get_topic_study_totals"}'
                '], "answer": null}'

                "学習状況の分析を求められた場合は、"
                "get_study_analysis_factsを選んでください。"

                "例："
                "ユーザー：今の学習状況を分析して"
                "回答："
                '{"tools": ['
                '{"tool": "get_study_analysis_facts"}'
                '], "answer": null}'

                "学習状況の分析を求められた場合は、"
                "get_study_analysis_factsを選んでください。"

                "例："
                "ユーザー：今の学習状況を分析して"
                "回答："
                '{"tools": [{"tool": "get_study_analysis_facts"}], '
                '"answer": null}'

                "重要：回答は必ず有効なJSONだけにしてください。"
                "JSONの前後に説明文、回答文、Markdown、コードブロックを"
                "追加してはいけません。"
                "キーと文字列には必ずダブルクォートを使用してください。"
                "toolsとanswerは必ずJSONオブジェクトの直下に置いてください。"

                "学習目標を設定する場合は、"
                "set_study_goalを選んでください。"

                "例："
                "ユーザー：Pythonを120分勉強する目標にしたい"
                "回答："
                '{"tools": ['
                '{"tool": "set_study_goal", '
                '"topic": "Python", '
                '"target_minutes": 120}'
                '], "answer": null}'

                "学習目標までの進捗を確認する場合は、"
                "get_goal_progressを選んでください。"

                "例："
                "ユーザー：Pythonの目標まであとどれくらい？"
                "回答："
                '{"tools": ['
                '{"tool": "get_goal_progress", '
                '"topic": "Python"}'
                '], "answer": null}'
            )
        }
    ]

    messages.extend(conversation_history)

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()
        content = data["message"]["content"]

        if not isinstance(content, str):
            raise TypeError(
                "Ollamaのmessage.contentが文字列ではありません。"
            )

        return content

    except requests.RequestException as error:
        print("Ollamaとの通信に失敗しました。")
        print("詳細:", error)

        return None

    except (KeyError, TypeError, ValueError) as error:
        print("Ollamaの返答を解析できませんでした。")
        print("詳細:", error)

        return None


def validate_tools(
    user_input,
    tools,
    conversation_history=None
):
    if conversation_history is None:
        conversation_history = []

    # -------------------------
    # トピック別集計の判定
    # -------------------------
    wants_topic_totals = any(
        phrase in user_input
        for phrase in [
            "トピック別",
            "テーマ別",
            "内容別"
        ]
    ) and any(
        word in user_input
        for word in [
            "時間",
            "何分",
            "学習時間",
            "勉強時間"
        ]
    )

    # -------------------------
    # 全体の合計時間を知りたいか
    # -------------------------
    time_words = [
        "時間",
        "何分",
        "何時間",
        "学習時間",
        "勉強時間"
    ]

    strong_total_words = [
        "合計",
        "全部で",
        "累計",
        "トータル"
    ]

    context_total_words = [
        "今まで",
        "これまで"
    ]

    wants_total = (
        not wants_topic_totals
        and (
            any(
                word in user_input
                for word in strong_total_words
            )
            or (
                any(
                    word in user_input
                    for word in time_words
                )
                and any(
                    word in user_input
                    for word in context_total_words
                )
            )
        )
    )

    # -------------------------
    # 学習トピック一覧の判定
    # -------------------------
    topic_list_phrases = [
        "何を勉強した",
        "何を学習した",
        "学習したトピック",
        "勉強したトピック",
        "勉強した内容の一覧",
        "学習した内容の一覧",
        "学習トピックの一覧"
    ]

    topic_list_analysis_phrases = [
        "分析",
        "一番",
        "最も",
        "最多",
        "最少",
        "少ない",
        "比較"
    ]

    topic_list_advice_phrases = [
        "何を勉強したら",
        "何を学習したら",
        "何を勉強すべき",
        "何を学習すべき",
        "何を勉強したい",
        "何を学習したい"
    ]

    wants_topic_list = (
        any(
            phrase in user_input
            for phrase in topic_list_phrases
        )
        and not wants_topic_totals
        and not any(
            phrase in user_input
            for phrase in topic_list_analysis_phrases
        )
        and not any(
            phrase in user_input
            for phrase in topic_list_advice_phrases
        )
    )

    # -------------------------
    # 学習分析の判定
    # -------------------------
    wants_analysis = (
        not wants_topic_totals
        and (
            (
                "分析" in user_input
                and any(
                    word in user_input
                    for word in [
                        "学習",
                        "勉強",
                        "トピック"
                    ]
                )
            )
            or (
                any(
                    word in user_input
                    for word in [
                        "一番",
                        "最も",
                        "最多",
                        "最少",
                        "少ない"
                    ]
                )
                and "トピック" in user_input
            )
        )
    )

    # -------------------------
    # 分数の取得
    # -------------------------
    minutes_match = re.search(
        r"(\d+)分",
        user_input
    )

    has_minutes = minutes_match is not None

    # ユーザー入力に分数がない場合、
    # Qwenが勝手に作った詳細学習記録Toolを除去する
    if not has_minutes:
        tools = [
            tool
            for tool in tools
            if tool.get("tool") != "add_detailed_study"
        ]
    # -------------------------
    # トピック + 分数の詳細記録
    # -------------------------
    detailed_match = re.search(
        r"(.+?)を(\d+)分(?:勉強した|学習した)",
        user_input
    )

    wants_detailed_add = (
        detailed_match is not None
    )

    # -------------------------
    # 時間だけの記録
    # -------------------------
    wants_add = (
        has_minutes
        and not wants_detailed_add
        and any(
            word in user_input
            for word in [
                "勉強した",
                "学習した",
                "記録して",
                "追加して",
                "やった"
            ]
        )
    )

    refuses_add = any(
        phrase in user_input
        for phrase in [
            "記録しない",
            "追加しない",
            "記録しないで",
            "追加しないで",
            "勉強していません"
        ]
    )

    if refuses_add:
        wants_add = False
        wants_detailed_add = False

    # -------------------------
    # 詳細記録を最優先
    # -------------------------
    if wants_detailed_add:
        topic = detailed_match.group(1).strip()
        minutes = int(
            detailed_match.group(2)
        )

        for prefix in [
            "今日は",
            "今日",
            "さっき",
            "今"
        ]:
            if topic.startswith(prefix):
                topic = topic[
                    len(prefix):
                ].strip()

        # 競合する記録Toolを一度除去
        tools = [
            tool
            for tool in tools
            if tool.get("tool") not in [
                "add_study_minutes",
                "add_study_topic",
                "add_detailed_study"
            ]
        ]

        tools.insert(
            0,
            {
                "tool": "add_detailed_study",
                "topic": topic,
                "minutes": minutes
            }
        )

    # -------------------------
    # 時間だけの記録
    # -------------------------
    if not wants_add:
        tools = [
            tool
            for tool in tools
            if tool.get("tool") != "add_study_minutes"
        ]

    tool_names = [
        tool.get("tool")
        for tool in tools
    ]

    if (
        wants_add
        and "add_study_minutes" not in tool_names
    ):
        minutes = int(
            minutes_match.group(1)
        )

        tools.insert(
            0,
            {
                "tool": "add_study_minutes",
                "minutes": minutes
            }
        )

    # -------------------------
    # 全体の合計時間
    # -------------------------
    tool_names = [
        tool.get("tool")
        for tool in tools
    ]

    if (
        wants_total
        and "get_total_study_minutes" not in tool_names
    ):
        tools.append(
            {
                "tool": "get_total_study_minutes",
                "minutes": None
            }
        )

    # -------------------------
    # トピック別学習時間
    # -------------------------
    tool_names = [
        tool.get("tool")
        for tool in tools
    ]

    if (
        wants_topic_totals
        and "get_topic_study_totals" not in tool_names
    ):
        tools.append(
            {
                "tool": "get_topic_study_totals"
            }
        )

    # -------------------------
    # 分 → 時間・分への換算
    # -------------------------
    wants_conversion = any(
        phrase in user_input
        for phrase in [
            "何時間何分",
            "時間と分",
            "時間にすると"
        ]
    )

    tool_names = [
        tool.get("tool")
        for tool in tools
    ]

    if (
        wants_conversion
        and "convert_minutes_to_hours" not in tool_names
    ):
        previous_minutes = None

        for message in reversed(
            conversation_history
        ):
            content = message.get(
                "content",
                ""
            )

            match = re.search(
                r"(\d+)分",
                content
            )

            if match:
                previous_minutes = int(
                    match.group(1)
                )
                break

        if previous_minutes is not None:
            tools.append(
                {
                    "tool": "convert_minutes_to_hours",
                    "minutes": previous_minutes
                }
            )

    # -------------------------
    # 学習トピックだけの記録
    # -------------------------
    topic_match = re.search(
        r"(.+?)を(?:勉強した|学習した)",
        user_input
    )

    topic_question = any(
        phrase in user_input
        for phrase in [
            "何を勉強した",
            "何を学習した",
            "どんなことを勉強した",
            "どんなことを学習した"
        ]
    )

    wants_topic_add = (
        topic_match is not None
        and not has_minutes
        and not topic_question
    )

    if wants_topic_add:
        topic = topic_match.group(1).strip()

        for prefix in [
            "今日は",
            "今日",
            "さっき",
            "今"
        ]:
            if topic.startswith(prefix):
                topic = topic[
                    len(prefix):
                ].strip()

        tool_names = [
            tool.get("tool")
            for tool in tools
        ]

        if (
            topic
            and "add_study_topic" not in tool_names
        ):
            tools.append(
                {
                    "tool": "add_study_topic",
                    "topic": topic
                }
            )

    # -------------------------
    # トピック別集計・分析・一覧要求
    # -------------------------
    confirmed_write_tools = []

    if wants_detailed_add:
        confirmed_write_tools.append(
            {
                "tool": "add_detailed_study",
                "topic": topic,
                "minutes": minutes
            }
        )

    elif wants_add:
        confirmed_write_tools.append(
            {
                "tool": "add_study_minutes",
                "minutes": int(minutes_match.group(1))
            }
        )

    elif wants_topic_add:
        confirmed_write_tools.append(
            {
                "tool": "add_study_topic",
                "topic": topic
            }
        )

    if wants_topic_totals:
        tools = confirmed_write_tools + [
            {
                "tool": "get_topic_study_totals"
            }
        ]

    elif wants_analysis:
        tools = confirmed_write_tools + [
            {
                "tool": "get_study_analysis_facts"
            }
        ]

    elif wants_topic_list:
        tools = confirmed_write_tools + [
            {
                "tool": "get_study_topics"
            }
        ]

        if wants_total:
            tools.append(
                {
                    "tool": "get_total_study_minutes",
                    "minutes": None
                }
            )

    # -------------------------
    # 許可されたToolだけ残す
    # -------------------------
    allowed_tools = [
        "add_study_minutes",
        "get_total_study_minutes",
        "convert_minutes_to_hours",
        "add_study_topic",
        "get_study_topics",
        "add_detailed_study",
        "get_topic_study_totals",
        "get_study_analysis_facts",
        "set_study_goal",
        "get_goal_progress"
    ]

    tools = [
        tool
        for tool in tools
        if tool.get("tool") in allowed_tools
    ]

    return tools


def execute_tools(tools):
    tool_results = []

    for tool in tools:
        tool_name = tool.get("tool")

        tool_config = TOOL_REGISTRY.get(
            tool_name
        )

        if tool_config is None:
            tool_results.append(
                f"未対応のToolです：{tool_name}"
            )
            continue

        tool_function = tool_config["function"]
        argument_names = tool_config["arguments"]

        try:
            arguments = []

            valid = True

            for argument_name in argument_names:
                argument_value = tool.get(
                    argument_name
                )

                if argument_value is None:
                    valid = False
                    break

                if (
                    argument_name in [
                        "minutes",
                        "target_minutes"
                    ]
                    and (
                        not isinstance(argument_value, int)
                        or argument_value <= 0
                    )
                ):
                    valid = False
                    break

                if (
                    argument_name == "topic"
                    and (
                        not isinstance(argument_value, str)
                        or not argument_value.strip()
                    )
                ):
                    valid = False
                    break

                arguments.append(
                    argument_value
                )

            if not valid:
                tool_results.append(
                    f"{tool_name}を実行できませんでした。"
                )
                continue

            result = tool_function(
                *arguments
            )

            tool_results.append(result)

        except Exception as error:
            tool_results.append(
                f"{tool_name}の実行中にエラーが発生しました：{error}"
            )

    return tool_results


def generate_final_answer(user_input, tool_results):
    formatted_results = []

    for result in tool_results:
        if isinstance(result, dict):
            formatted_results.append(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2
                )
            )
        else:
            formatted_results.append(
                str(result)
            )

    combined_result = "\n".join(
        formatted_results
    )

    messages = [
        {
            "role": "system",
            "content": (
                "あなたはAI学習をサポートするアシスタントです。"
                "Toolの実行結果だけを根拠に最終回答してください。"
                "Tool実行結果にない情報を推測・追加してはいけません。"
                "実行されていない処理を実行済みとして回答してはいけません。"

                "特に重要："
                "Tool実行結果が『527分です』のように分だけを返した場合、"
                "時間や時間＋分への換算を勝手に追加してはいけません。"
                "時間換算はconvert_minutes_to_hoursの実行結果がある場合だけ"
                "回答に含めてください。"

                "数値を自分で計算してはいけません。"
                "Tool実行結果をそのまま正確に伝えてください。"
                "短く自然な日本語で回答してください。"

                "学習時間の多い・少ないという相対比較は、"
                "Tool結果に含まれる数値だけを根拠にしてください。"
                "『十分』『不足』『もっと勉強すべき』など、"
                "基準が与えられていない評価や提案を勝手に追加してはいけません。"

                "Tool結果にmost_studiedやleast_studiedが含まれている場合は、"
                "その内容をそのまま事実として説明してください。"

                "『十分』『不足』『良い』『悪い』『順調』などの評価語は、"
                "明示的な基準がTool結果に含まれていない限り使用してはいけません。"

                "学習分析では、合計時間、トピック数、各トピックの時間、"
                "most_studied、least_studiedの事実だけを説明してください。"
            )
        },
        {
            "role": "user",
            "content": (
                f"ユーザーの依頼：{user_input}\n"
                f"Tool実行結果：\n{combined_result}"
            )
        }
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]

    except requests.RequestException as error:
        print("最終回答の生成中にOllamaとの通信に失敗しました。")
        print("詳細:", error)

        return "\n".join(formatted_results)


def main():
    user_input = input("あなた：")

    result = select_tool(user_input)

    if result is None:
        print("AIとの通信に失敗したため、Toolは実行しませんでした。")
        return

    try:
        tool_data = json.loads(result)

    except json.JSONDecodeError:
        print("AIの返答をJSONとして解析できませんでした。")
        return

    tools = tool_data.get("tools", [])

    tools = validate_tools(
        user_input,
        tools
    )


    if tools:
        tool_results = execute_tools(tools)

        final_answer = generate_final_answer(
            user_input,
            tool_results
        )

        print("=== AIの最終回答 ===")
        print(final_answer)

    else:
        print("=== AIの回答 ===")
        print(
            tool_data.get(
                "answer",
                "回答を取得できませんでした。"
            )
        )


if __name__ == "__main__":
    main()
