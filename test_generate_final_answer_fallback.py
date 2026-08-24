import json
import unittest
from unittest.mock import patch

import requests

from tool_selector import generate_final_answer


class GenerateFinalAnswerFallbackTest(unittest.TestCase):
    @patch(
        "tool_selector.requests.post",
        side_effect=requests.RequestException("通信失敗"),
    )
    def test_string_result(self, mock_post):
        result = generate_final_answer(
            "合計を教えて",
            ["合計は30分です。"],
        )

        self.assertEqual(
            result,
            "合計は30分です。",
        )
        mock_post.assert_called_once()

    @patch(
        "tool_selector.requests.post",
        side_effect=requests.RequestException("通信失敗"),
    )
    def test_dictionary_result(self, mock_post):
        tool_result = {
            "total_minutes": 30,
            "achieved": False,
        }

        result = generate_final_answer(
            "分析して",
            [tool_result],
        )

        self.assertEqual(
            result,
            json.dumps(
                tool_result,
                ensure_ascii=False,
                indent=2,
            ),
        )
        mock_post.assert_called_once()

    @patch(
        "tool_selector.requests.post",
        side_effect=requests.RequestException("通信失敗"),
    )
    def test_mixed_results(self, mock_post):
        tool_results = [
            "記録しました。",
            {"total_minutes": 30},
            123,
            None,
        ]

        result = generate_final_answer(
            "記録して結果も教えて",
            tool_results,
        )

        self.assertEqual(
            result,
            "\n".join(
                [
                    "記録しました。",
                    json.dumps(
                        {"total_minutes": 30},
                        ensure_ascii=False,
                        indent=2,
                    ),
                    "123",
                    "None",
                ]
            ),
        )
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
