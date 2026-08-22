import requests

url = "https://jsonplaceholder.typicode.com/todos/1"

try:
    response = requests.get(url, timeout=10)

    print(f"ステータスコード：{response.status_code}")

    response.raise_for_status()

    data = response.json()

    print("=== TODO情報 ===")
    print(f"ユーザーID：{data['userId']}")
    print(f"TODO ID：{data['id']}")
    print(f"タイトル：{data['title']}")
    print(f"完了済み：{data['completed']}")

except requests.RequestException as error:
    print(f"通信エラー：{error}")