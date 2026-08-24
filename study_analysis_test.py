from detailed_study_tools import get_study_analysis_facts
import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


facts = get_study_analysis_facts()

facts_json = json.dumps(
    facts,
    ensure_ascii=False,
    indent=2
)

messages = [
    {
        "role": "system",
        "content": (
            "あなたはAI学習を支援する分析アシスタントです。"
            "与えられたJSONはPythonが計算した確定済みの事実です。"
            "数値、トピック数、最多・最少の内容を変更してはいけません。"
            "自分で再計算してはいけません。"
            "新しい数値や学習時間の提案を作ってはいけません。"
            "与えられた事実だけを自然な日本語で2〜4文にまとめてください。"
        )
    },
    {
        "role": "user",
        "content": (
            "次の確定済み学習データを説明してください。\n\n"
            f"{facts_json}"
        )
    }
]

payload = {
    "model": MODEL_NAME,
    "messages": messages,
    "stream": False
}

response = requests.post(
    OLLAMA_URL,
    json=payload,
    timeout=60
)

response.raise_for_status()

data = response.json()

print("=== 確定済みデータ ===")
print(facts_json)

print("=== AI分析 ===")
print(data["message"]["content"])