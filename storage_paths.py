import os
from pathlib import Path


DATA_DIR_ENV_VAR = "AI_LEARNING_DATA_DIR"


class StorageConfigurationError(Exception):
    pass


def get_data_directory():
    configured_directory = os.getenv(DATA_DIR_ENV_VAR)

    if configured_directory is None:
        return Path(__file__).resolve().parent

    if not configured_directory.strip():
        raise StorageConfigurationError(
            f"{DATA_DIR_ENV_VAR}が空です。絶対パスのフォルダを指定してください。"
        )

    data_directory = Path(configured_directory).expanduser()

    if not data_directory.is_absolute():
        raise StorageConfigurationError(
            f"{DATA_DIR_ENV_VAR}に相対パスが指定されています。"
            "絶対パスのフォルダを指定してください。"
        )

    if not data_directory.exists():
        raise StorageConfigurationError(
            f"{DATA_DIR_ENV_VAR}で指定された保存先が存在しません: "
            f"{data_directory}"
        )

    if not data_directory.is_dir():
        raise StorageConfigurationError(
            f"{DATA_DIR_ENV_VAR}で指定された保存先はフォルダではありません: "
            f"{data_directory}"
        )

    return data_directory


def get_data_path(filename):
    return get_data_directory() / filename
