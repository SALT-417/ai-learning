import json

student = {
    "name": "YASU",
    "goal": "AI人材としてキャリアを築く",
    "study_minutes": 60
}

print(student)
print(type(student))

json_text = json.dumps(student, ensure_ascii=False, indent=2)

print(json_text)
print(type(json_text))

restored_student = json.loads(json_text)

print(restored_student)
print(type(restored_student))

print(restored_student["name"])
print(restored_student["goal"])
print(restored_student["study_minutes"])

api_response = '''
{
    "model": "ai-assistant",
    "status": "success",
    "tokens": 1250
}
'''

data = json.loads(api_response)

print("=== APIレスポンス ===")
print(f"モデル：{data['model']}")
print(f"状態：{data['status']}")
print(f"トークン数：{data['tokens']}")

print(data.get("message"))
print(data.get("message", "メッセージなし"))