name = input("あなたの名前を入力してください：")
minutes = int(input("今日の学習時間（分）を入力してください："))

print(f"こんにちは、{name}さん！")
print(f"今日は{minutes}分学習します。")

if minutes >= 60:
    print("素晴らしい！しっかり学習時間を確保できています。")
elif minutes >= 30:
    print("いいペースです！この調子で続けましょう。")  
else:
    print("少しずつ学習時間を増やしていきましょう。")