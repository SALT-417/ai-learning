import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AI_API_KEY")

if api_key:
    print("APIキーを読み込みました。")
else:
    print("APIキーが設定されていません。")