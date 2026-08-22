import csv

day = input("曜日を入力してください：")

try:
    minutes = int(input("学習時間（分）を入力してください："))

except ValueError:
    print("エラー：学習時間には数字を入力してください。")

else:
    with open("study_data.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([day, minutes])

    print("学習記録を保存しました。")