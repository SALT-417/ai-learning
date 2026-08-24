import json


MEMORY_FILE = "conversation_history.json"


def save_history(conversation_history):
    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            conversation_history,
            file,
            ensure_ascii=False,
            indent=2
        )


def load_history():
    try:
        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def get_recent_history(
    conversation_history,
    max_messages=6
):
    return conversation_history[-max_messages:]