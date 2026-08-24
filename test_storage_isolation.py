import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import detailed_study_tools
import memory_manager
import storage_paths
import study_goal_tools
import study_tools
import study_topic_tools


DATA_ENV_VAR = "AI_LEARNING_DATA_DIR"
PRODUCTION_DATA_FILES = (
    "study_records.csv",
    "study_topics.csv",
    "detailed_study_records.csv",
    "study_goals.csv",
    "conversation_history.json",
)


class StorageIsolationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repository_root = Path(storage_paths.__file__).resolve().parent
        cls.production_metadata_before = cls._get_production_metadata()

    @classmethod
    def tearDownClass(cls):
        production_metadata_after = cls._get_production_metadata()

        if production_metadata_after != cls.production_metadata_before:
            raise AssertionError(
                "本番CSV・JSONのサイズまたは更新日時が変化しました。"
            )

    @classmethod
    def _get_production_metadata(cls):
        metadata = {}

        for filename in PRODUCTION_DATA_FILES:
            file_path = cls.repository_root / filename

            if not file_path.exists():
                metadata[filename] = None
                continue

            file_stat = file_path.stat()
            metadata[filename] = (
                file_stat.st_size,
                file_stat.st_mtime_ns,
            )

        return metadata

    def test_production_metadata_when_all_files_are_missing(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.object(
                StorageIsolationTest,
                "repository_root",
                temporary_directory,
            ):
                metadata_before = self._get_production_metadata()
                metadata_after = self._get_production_metadata()

        expected = {
            filename: None
            for filename in PRODUCTION_DATA_FILES
        }

        self.assertEqual(metadata_before, expected)
        self.assertEqual(metadata_after, metadata_before)

    def test_production_metadata_when_some_files_exist(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()
            existing_file = temporary_directory / "study_records.csv"
            existing_file.touch()

            with patch.object(
                StorageIsolationTest,
                "repository_root",
                temporary_directory,
            ):
                metadata = self._get_production_metadata()

        self.assertIsNotNone(metadata["study_records.csv"])

        for filename in PRODUCTION_DATA_FILES[1:]:
            self.assertIsNone(metadata[filename])

    def test_default_data_directory(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop(DATA_ENV_VAR, None)

            self.assertEqual(
                storage_paths.get_data_directory(),
                self.repository_root,
            )

    def test_existing_absolute_directory(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                self.assertEqual(
                    storage_paths.get_data_directory(),
                    temporary_directory,
                )

    def test_empty_environment_value(self):
        with patch.dict(
            os.environ,
            {DATA_ENV_VAR: ""},
            clear=False,
        ):
            with self.assertRaisesRegex(
                storage_paths.StorageConfigurationError,
                "AI_LEARNING_DATA_DIRが空",
            ):
                storage_paths.get_data_directory()

    def test_relative_directory(self):
        with patch.dict(
            os.environ,
            {DATA_ENV_VAR: "relative-data-directory"},
            clear=False,
        ):
            with self.assertRaisesRegex(
                storage_paths.StorageConfigurationError,
                "AI_LEARNING_DATA_DIRに相対パス",
            ):
                storage_paths.get_data_directory()

    def test_missing_absolute_directory(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            missing_directory = (
                Path(temporary_name).resolve()
                / "missing-directory"
            )

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(missing_directory)},
                clear=False,
            ):
                with self.assertRaisesRegex(
                    storage_paths.StorageConfigurationError,
                    "AI_LEARNING_DATA_DIRで指定された保存先が存在しません",
                ):
                    storage_paths.get_data_directory()

            self.assertFalse(missing_directory.exists())

    def test_file_path(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_file = (
                Path(temporary_name).resolve()
                / "not-a-directory.txt"
            )
            temporary_file.touch()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_file)},
                clear=False,
            ):
                with self.assertRaisesRegex(
                    storage_paths.StorageConfigurationError,
                    "AI_LEARNING_DATA_DIRで指定された保存先はフォルダではありません",
                ):
                    storage_paths.get_data_directory()

    def test_environment_is_resolved_at_call_time(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop(DATA_ENV_VAR, None)

            self.assertEqual(
                storage_paths.get_data_path("example.csv"),
                self.repository_root / "example.csv",
            )

            with tempfile.TemporaryDirectory() as temporary_name:
                temporary_directory = Path(temporary_name).resolve()

                with patch.dict(
                    os.environ,
                    {DATA_ENV_VAR: str(temporary_directory)},
                    clear=False,
                ):
                    self.assertEqual(
                        storage_paths.get_data_path("example.csv"),
                        temporary_directory / "example.csv",
                    )

    def test_study_minutes_in_temporary_directory(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                study_tools.add_study_minutes(30)
                study_tools.add_study_minutes(45)

                self.assertEqual(
                    study_tools.get_total_study_minutes(),
                    "これまでの合計学習時間は75分です。",
                )
                self.assertTrue(
                    (temporary_directory / "study_records.csv").is_file()
                )

    def test_study_topics_in_temporary_directory(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                study_topic_tools.add_study_topic("Python")
                study_topic_tools.add_study_topic("RAG")

                self.assertEqual(
                    study_topic_tools.get_study_topics(),
                    "これまでの学習トピック：Python、RAG",
                )
                self.assertTrue(
                    (temporary_directory / "study_topics.csv").is_file()
                )

    def test_detailed_records_in_temporary_directory(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                detailed_study_tools.add_detailed_study("Python", 30)
                detailed_study_tools.add_detailed_study("Python", 45)
                detailed_study_tools.add_detailed_study("RAG", 20)

                self.assertEqual(
                    detailed_study_tools.get_topic_study_totals(),
                    "トピック別学習時間：\nPython：75分\nRAG：20分",
                )
                self.assertEqual(
                    detailed_study_tools.get_study_analysis_facts(),
                    {
                        "total_minutes": 95,
                        "topic_count": 2,
                        "topics": {
                            "Python": 75,
                            "RAG": 20,
                        },
                        "most_studied": {
                            "topic": "Python",
                            "minutes": 75,
                        },
                        "least_studied": {
                            "topic": "RAG",
                            "minutes": 20,
                        },
                    },
                )
                self.assertTrue(
                    (
                        temporary_directory
                        / "detailed_study_records.csv"
                    ).is_file()
                )

    def test_study_goal_in_temporary_directory(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                detailed_study_tools.add_detailed_study("Python", 30)
                study_goal_tools.set_study_goal("Python", 120)

                self.assertEqual(
                    study_goal_tools.get_goal_progress("Python"),
                    {
                        "topic": "Python",
                        "target_minutes": 120,
                        "current_minutes": 30,
                        "remaining_minutes": 90,
                        "achieved": False,
                    },
                )
                self.assertTrue(
                    (temporary_directory / "study_goals.csv").is_file()
                )

    def test_conversation_history_in_temporary_directory(self):
        test_history = [
            {
                "role": "user",
                "content": "テスト用メッセージ",
            },
            {
                "role": "assistant",
                "content": "テスト用の返答",
            },
        ]

        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                memory_manager.save_history(test_history)

                self.assertEqual(
                    memory_manager.load_history(),
                    test_history,
                )
                self.assertTrue(
                    (
                        temporary_directory
                        / "conversation_history.json"
                    ).is_file()
                )

    def test_temporary_directory_is_removed(self):
        with tempfile.TemporaryDirectory() as temporary_name:
            temporary_directory = Path(temporary_name).resolve()

            with patch.dict(
                os.environ,
                {DATA_ENV_VAR: str(temporary_directory)},
                clear=False,
            ):
                self.assertTrue(temporary_directory.is_dir())

        self.assertFalse(temporary_directory.exists())


if __name__ == "__main__":
    unittest.main()
