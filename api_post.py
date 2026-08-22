import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "AI学習",
    "body": "PythonからPOSTリクエストを送信しました。",
    "userId": 1
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    print(f"ステータスコード：{response.status_code}")
    print("=== APIレスポンス ===")
    print(data)
    print(type(data))
    print("=== 作成されたデータ ===")
    print(f"ID：{data['id']}")
    print(f"タイトル：{data['title']}")
    print(f"本文：{data['body']}")
    print(f"ユーザーID：{data['userId']}")

except requests.RequestException as error:
    print(f"通信エラー：{error}")