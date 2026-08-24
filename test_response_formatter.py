import json
import unittest
from unittest.mock import Mock, patch

import chat_agent
import tool_selector
from response_formatter import (
    format_tool_result,
    format_tool_results
)


class ResponseFormatterTest(unittest.TestCase):
    def test_string_is_returned_unchanged(self):
        result = "これまでの学習トピック：RAG\n次の行"
        self.assertEqual(format_tool_result(result), result)

    def test_empty_analysis(self):
        result = {
            "total_minutes": 0,
            "topic_count": 0,
            "topics": {},
            "most_studied": None,
            "least_studied": None,
        }

        self.assertEqual(
            format_tool_result(result),
            "学習分析：\n"
            "合計時間：0分\n"
            "トピック数：0\n"
            "トピック別学習時間：なし\n"
            "最多：なし\n"
            "最少：なし",
        )

    def test_analysis_with_multiple_topics(self):
        result = {
            "total_minutes": 180,
            "topic_count": 2,
            "topics": {"RAG": 120, "Python": 60},
            "most_studied": {"topic": "RAG", "minutes": 120},
            "least_studied": {"topic": "Python", "minutes": 60},
        }

        self.assertEqual(
            format_tool_result(result),
            "学習分析：\n"
            "合計時間：180分\n"
            "トピック数：2\n"
            "トピック別学習時間：\n"
            "RAG：120分\n"
            "Python：60分\n"
            "最多：RAG（120分）\n"
            "最少：Python（60分）",
        )

    def test_same_topic_is_most_and_least(self):
        result = {
            "total_minutes": 30,
            "topic_count": 1,
            "topics": {"RAG": 30},
            "most_studied": {"topic": "RAG", "minutes": 30},
            "least_studied": {"topic": "RAG", "minutes": 30},
        }

        formatted = format_tool_result(result)
        self.assertIn("最多：RAG（30分）", formatted)
        self.assertIn("最少：RAG（30分）", formatted)

    def test_achieved_goal(self):
        result = {
            "topic": "Python",
            "target_minutes": 120,
            "current_minutes": 150,
            "remaining_minutes": 0,
            "achieved": True,
        }

        self.assertEqual(
            format_tool_result(result),
            "目標進捗：\n"
            "トピック：Python\n"
            "目標：120分\n"
            "現在：150分\n"
            "残り：0分\n"
            "達成状態：達成",
        )

    def test_unachieved_goal(self):
        result = {
            "topic": "Python",
            "target_minutes": 120,
            "current_minutes": 90,
            "remaining_minutes": 30,
            "achieved": False,
        }

        self.assertEqual(
            format_tool_result(result),
            "目標進捗：\n"
            "トピック：Python\n"
            "目標：120分\n"
            "現在：90分\n"
            "残り：30分\n"
            "達成状態：未達成",
        )

    def test_error_dictionary_returns_only_message(self):
        self.assertEqual(
            format_tool_result({"error": "目標がありません。"}),
            "目標がありません。",
        )

    def test_none(self):
        self.assertEqual(format_tool_result(None), "結果なし")

    def test_integer(self):
        self.assertEqual(format_tool_result(42), "42")

    def test_list_uses_json_fallback(self):
        result = ["RAG", {"minutes": 30}]
        self.assertEqual(
            format_tool_result(result),
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                default=str,
            ),
        )

    def test_unknown_dictionary_uses_json_fallback(self):
        result = {"z": 1, "a": "RAG"}
        self.assertEqual(
            format_tool_result(result),
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                default=str,
            ),
        )

    def test_invalid_analysis_types_use_json_fallback(self):
        result = {
            "total_minutes": True,
            "topic_count": 1,
            "topics": {"RAG": 30},
            "most_studied": {"topic": "RAG", "minutes": 30},
            "least_studied": {"topic": "RAG", "minutes": 30},
        }
        self.assertEqual(
            format_tool_result(result),
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                default=str,
            ),
        )

    def test_invalid_goal_types_use_json_fallback(self):
        result = {
            "topic": "Python",
            "target_minutes": True,
            "current_minutes": 90,
            "remaining_minutes": 30,
            "achieved": False,
        }
        self.assertEqual(
            format_tool_result(result),
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                default=str,
            ),
        )

    def test_multiple_results_keep_input_order_and_duplicates(self):
        self.assertEqual(
            format_tool_results(["最初", "次", "最初"]),
            "最初\n次\n最初",
        )


class ChatAgentFormattingTest(unittest.TestCase):
    def assert_invalid_chat_response(
        self,
        selected_result,
        expected_message,
        validated_tools=None,
    ):
        if validated_tools is None:
            validated_tools = []

        with patch(
            "builtins.input",
            side_effect=["テスト入力", "終了"],
        ) as mock_input, patch(
            "builtins.print"
        ) as mock_print, patch(
            "chat_agent.load_history",
            return_value=[],
        ), patch(
            "chat_agent.split_history",
            return_value=([], []),
        ), patch(
            "chat_agent.summarize_history",
            return_value="",
        ), patch(
            "chat_agent.select_tool",
            return_value=selected_result,
        ), patch(
            "chat_agent.validate_tools",
            return_value=validated_tools,
        ) as mock_validate_tools, patch(
            "chat_agent.execute_tools"
        ) as mock_execute_tools, patch(
            "chat_agent.format_tool_results"
        ) as mock_formatter, patch(
            "chat_agent.save_history"
        ) as mock_save_history:
            chat_agent.main()

        mock_input.assert_called_with("あなた：")
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call(expected_message)
        mock_print.assert_any_call(
            "AI学習エージェントを終了します。"
        )
        mock_execute_tools.assert_not_called()
        mock_formatter.assert_not_called()
        mock_save_history.assert_not_called()

        return mock_validate_tools

    def test_tool_results_are_passed_to_formatter(self):
        selected = json.dumps(
            {
                "tools": [{"tool": "get_study_analysis_facts"}],
                "answer": None,
            },
            ensure_ascii=False,
        )
        tool_results = [{"total_minutes": 0}]

        with patch(
            "builtins.input",
            side_effect=["学習状況を分析して", "終了"],
        ), patch(
            "builtins.print"
        ) as mock_print, patch(
            "chat_agent.load_history",
            return_value=[],
        ), patch(
            "chat_agent.split_history",
            return_value=([], []),
        ), patch(
            "chat_agent.summarize_history",
            return_value="",
        ), patch(
            "chat_agent.select_tool",
            return_value=selected,
        ), patch(
            "chat_agent.validate_tools",
            return_value=[{"tool": "get_study_analysis_facts"}],
        ), patch(
            "chat_agent.execute_tools",
            return_value=tool_results,
        ) as mock_execute_tools, patch(
            "chat_agent.format_tool_results",
            return_value="整形済み結果",
        ) as mock_formatter, patch(
            "chat_agent.save_history"
        ) as mock_save_history:
            chat_agent.main()

        mock_execute_tools.assert_called_once()
        mock_formatter.assert_called_once_with(tool_results)
        mock_print.assert_any_call("AI：", "整形済み結果")
        mock_save_history.assert_called_once()

    def test_general_conversation_uses_existing_answer(self):
        selected = json.dumps(
            {
                "tools": [],
                "answer": "従来の一般会話回答",
            },
            ensure_ascii=False,
        )

        with patch(
            "builtins.input",
            side_effect=["こんにちは", "終了"],
        ), patch(
            "builtins.print"
        ) as mock_print, patch(
            "chat_agent.load_history",
            return_value=[],
        ), patch(
            "chat_agent.split_history",
            return_value=([], []),
        ), patch(
            "chat_agent.summarize_history",
            return_value="",
        ), patch(
            "chat_agent.select_tool",
            return_value=selected,
        ), patch(
            "chat_agent.validate_tools",
            return_value=[],
        ), patch(
            "chat_agent.execute_tools"
        ) as mock_execute_tools, patch(
            "chat_agent.format_tool_results"
        ) as mock_formatter, patch(
            "chat_agent.save_history"
        ) as mock_save_history:
            chat_agent.main()

        mock_execute_tools.assert_not_called()
        mock_formatter.assert_not_called()
        mock_print.assert_any_call("AI：", "従来の一般会話回答")
        mock_save_history.assert_called_once()

    def test_chat_agent_handles_communication_failure(self):
        mock_validate_tools = self.assert_invalid_chat_response(
            None,
            "AI：AIとの通信に失敗したため、"
            "処理を実行できませんでした。",
        )
        mock_validate_tools.assert_not_called()

    def test_chat_agent_handles_invalid_json(self):
        mock_validate_tools = self.assert_invalid_chat_response(
            "not-json",
            "AI：AIの返答を解析できませんでした。",
        )
        mock_validate_tools.assert_not_called()

    def test_chat_agent_rejects_invalid_top_level_types(self):
        for selected_result in [
            "[]",
            "null",
            '"文字列"',
        ]:
            with self.subTest(selected_result=selected_result):
                mock_validate_tools = self.assert_invalid_chat_response(
                    selected_result,
                    "AI：AIの返答形式が正しくありませんでした。",
                )
                mock_validate_tools.assert_not_called()

    def test_chat_agent_rejects_invalid_tools_types(self):
        invalid_results = [
            {"tools": None, "answer": None},
            {"tools": "text", "answer": None},
            {"tools": [1], "answer": None},
        ]

        for invalid_result in invalid_results:
            with self.subTest(invalid_result=invalid_result):
                mock_validate_tools = self.assert_invalid_chat_response(
                    json.dumps(
                        invalid_result,
                        ensure_ascii=False,
                    ),
                    "AI：AIの返答形式が正しくありませんでした。",
                )
                mock_validate_tools.assert_not_called()

    def test_chat_agent_rejects_invalid_or_missing_answer(self):
        invalid_results = [
            {"tools": [], "answer": 123},
            {"tools": [], "answer": {}},
            {"tools": [], "answer": None},
            {"tools": []},
        ]

        for invalid_result in invalid_results:
            with self.subTest(invalid_result=invalid_result):
                self.assert_invalid_chat_response(
                    json.dumps(
                        invalid_result,
                        ensure_ascii=False,
                    ),
                    "AI：有効な回答を取得できませんでした。",
                    validated_tools=[],
                )


class ToolSelectorResponseHandlingTest(unittest.TestCase):
    def test_select_tool_rejects_invalid_ollama_response_structure(self):
        invalid_responses = [
            {},
            {"message": {}},
            {"message": {"content": None}},
            {"message": {"content": 123}},
            [],
        ]

        for response_data in invalid_responses:
            with self.subTest(response_data=response_data):
                mock_response = Mock()
                mock_response.json.return_value = response_data

                with patch(
                    "tool_selector.requests.post",
                    return_value=mock_response,
                ) as mock_post, patch(
                    "builtins.print"
                ) as mock_print:
                    result = tool_selector.select_tool("テスト入力")

                self.assertIsNone(result)
                mock_response.raise_for_status.assert_called_once()
                mock_post.assert_called_once()
                mock_print.assert_any_call(
                    "Ollamaの返答を解析できませんでした。"
                )


if __name__ == "__main__":
    unittest.main()
