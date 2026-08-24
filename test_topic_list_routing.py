import json
import unittest
from unittest.mock import patch

import chat_agent
from tool_selector import validate_tools


class TopicListRoutingTest(unittest.TestCase):
    def test_topic_list_inputs_override_incorrect_analysis_tool(self):
        topic_list_inputs = [
            "これまで何を勉強した？",
            "学習したトピックを教えて",
            "勉強した内容の一覧を見せて",
            "学習トピックの一覧",
        ]

        for user_input in topic_list_inputs:
            with self.subTest(user_input=user_input):
                result = validate_tools(
                    user_input,
                    [
                        {
                            "tool": "get_study_analysis_facts"
                        }
                    ],
                )

                self.assertEqual(
                    result,
                    [
                        {
                            "tool": "get_study_topics"
                        }
                    ],
                )

    def test_analysis_and_advice_inputs_are_not_forced_to_topic_list(self):
        cases = [
            (
                "今の学習状況を分析して",
                [{"tool": "get_study_analysis_facts"}],
                [{"tool": "get_study_analysis_facts"}],
            ),
            (
                "一番勉強したトピックは？",
                [{"tool": "get_study_analysis_facts"}],
                [{"tool": "get_study_analysis_facts"}],
            ),
            (
                "トピック別の学習時間を教えて",
                [],
                [{"tool": "get_topic_study_totals"}],
            ),
            (
                "Pythonを学ぶなら何を勉強したらいい？",
                [],
                [],
            ),
        ]

        for user_input, tools, expected in cases:
            with self.subTest(user_input=user_input):
                self.assertEqual(
                    validate_tools(user_input, tools),
                    expected,
                )

    def test_topic_list_and_total_inputs_are_fixed_to_two_tools(self):
        combined_inputs = [
            "勉強した内容の一覧と合計時間を教えて",
            "学習したトピックとこれまでの学習時間を教えて",
            "勉強した内容の一覧と累計を教えて",
        ]

        expected = [
            {
                "tool": "get_study_topics"
            },
            {
                "tool": "get_total_study_minutes",
                "minutes": None,
            },
        ]

        for user_input in combined_inputs:
            with self.subTest(user_input=user_input):
                self.assertEqual(
                    validate_tools(
                        user_input,
                        [
                            {"tool": "get_study_topics"},
                            {"tool": "get_study_topics"},
                            {
                                "tool": "get_total_study_minutes",
                                "minutes": None,
                            },
                            {"tool": "get_study_analysis_facts"},
                        ],
                    ),
                    expected,
                )

    def test_analysis_inputs_are_fixed_to_one_analysis_tool(self):
        analysis_inputs = [
            "今の学習状況を分析して",
            "一番勉強したトピックは？",
            "最も学習したトピックを教えて",
        ]

        selected_tools = [
            {"tool": "get_topic_study_totals"},
            {"tool": "get_study_analysis_facts"},
            {"tool": "get_study_analysis_facts"},
        ]

        for user_input in analysis_inputs:
            with self.subTest(user_input=user_input):
                self.assertEqual(
                    validate_tools(user_input, selected_tools),
                    [
                        {
                            "tool": "get_study_analysis_facts"
                        }
                    ],
                )

    def test_topic_totals_take_priority_over_analysis_tool(self):
        self.assertEqual(
            validate_tools(
                "トピック別の学習時間を教えて",
                [
                    {"tool": "get_study_analysis_facts"},
                    {"tool": "get_topic_study_totals"},
                ],
            ),
            [
                {
                    "tool": "get_topic_study_totals"
                }
            ],
        )

    def test_unrelated_analysis_is_not_fixed_to_study_analysis(self):
        selected_tools = [
            {"tool": "get_topic_study_totals"},
            {"tool": "get_study_analysis_facts"},
        ]

        self.assertEqual(
            validate_tools("売上を分析して", selected_tools),
            selected_tools,
        )

    def test_confirmed_recording_precedes_fixed_read_tool(self):
        cases = [
            (
                "今日はPythonを20分勉強した。"
                "トピック別の学習時間も教えて",
                [
                    {
                        "tool": "add_detailed_study",
                        "topic": "Python",
                        "minutes": 20,
                    },
                    {
                        "tool": "get_topic_study_totals"
                    },
                ],
            ),
            (
                "今日はPythonを20分勉強した。"
                "今の学習状況も分析して",
                [
                    {
                        "tool": "add_detailed_study",
                        "topic": "Python",
                        "minutes": 20,
                    },
                    {
                        "tool": "get_study_analysis_facts"
                    },
                ],
            ),
            (
                "今日は30分勉強した。今の学習状況も分析して",
                [
                    {
                        "tool": "add_study_minutes",
                        "minutes": 30,
                    },
                    {
                        "tool": "get_study_analysis_facts"
                    },
                ],
            ),
        ]

        model_tools = [
            {"tool": "get_study_analysis_facts"},
            {"tool": "get_topic_study_totals"},
            {"tool": "add_study_minutes", "minutes": 999},
            {"tool": "add_study_topic", "topic": "誤ったトピック"},
        ]

        for user_input, expected in cases:
            with self.subTest(user_input=user_input):
                self.assertEqual(
                    validate_tools(user_input, model_tools),
                    expected,
                )

    def test_unconfirmed_write_tools_are_removed_from_analysis(self):
        self.assertEqual(
            validate_tools(
                "今の学習状況を分析して",
                [
                    {"tool": "add_study_minutes", "minutes": 30},
                    {"tool": "add_study_topic", "topic": "RAG"},
                    {
                        "tool": "set_study_goal",
                        "topic": "Python",
                        "target_minutes": 120,
                    },
                    {"tool": "get_study_analysis_facts"},
                ],
            ),
            [
                {
                    "tool": "get_study_analysis_facts"
                }
            ],
        )

    def test_chat_agent_uses_direct_topic_list_response(self):
        incorrect_tool_selection = json.dumps(
            {
                "tools": [
                    {
                        "tool": "get_study_analysis_facts"
                    }
                ],
                "answer": None,
            },
            ensure_ascii=False,
        )
        topic_result = "これまでの学習トピック：RAG"

        with patch(
            "builtins.input",
            side_effect=[
                "これまで何を勉強した？",
                "終了",
            ],
        ), patch(
            "builtins.print"
        ) as mock_print, patch(
            "chat_agent.load_history",
            return_value=[],
        ), patch(
            "chat_agent.summarize_history",
            return_value="",
        ), patch(
            "chat_agent.select_tool",
            return_value=incorrect_tool_selection,
        ), patch(
            "chat_agent.execute_tools",
            return_value=[topic_result],
        ) as mock_execute_tools, patch(
            "chat_agent.format_tool_results",
            return_value=topic_result,
        ) as mock_format_tool_results, patch(
            "chat_agent.save_history"
        ) as mock_save_history:
            chat_agent.main()

        mock_execute_tools.assert_called_once_with(
            [
                {
                    "tool": "get_study_topics"
                }
            ]
        )
        mock_format_tool_results.assert_called_once_with(
            [topic_result]
        )
        mock_save_history.assert_called_once()
        mock_print.assert_any_call(
            "AI：",
            topic_result,
        )


if __name__ == "__main__":
    unittest.main()
