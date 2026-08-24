# AI学習記録ツール

AI学習の時間、トピック、詳細記録、目標を対話形式で記録・確認するWindows向けCLIツールです。

正式入口は `chat_agent.py` だけです。ほかのPythonファイルは、内部モジュール、テスト、初期学習用、確認用のいずれかです。

## CLI版MVPの主要機能

- 学習時間の追加と合計確認
- 学習トピックの追加と一覧表示
- トピックと時間を組み合わせた詳細記録
- トピック別学習時間の集計
- 合計時間、トピック数、最多・最少を含む学習分析
- トピック別目標の設定と進捗確認
- 記録と読取りを組み合わせた複数依頼
- Ollamaを使った一般会話

Toolの実行結果はOllamaへ再送せず、確定した書式で表示します。一般会話だけはOllamaの回答を使用します。

## 確認済み環境

- Windows
- Python 3.13
- Ollama
- Ollamaモデル `qwen2.5:3b`
- Ollama接続先 `http://localhost:11434/api/chat`

ほかのOS、Pythonバージョン、Ollamaモデルとの互換性は要確認です。

## 環境構築

### 1. PowerShellでリポジトリへ移動する

個人固有のパスではなく、実際に配置したフォルダへ移動してください。

```powershell
cd C:\path\to\ai-learning
```

### 2. Pythonを確認する

```powershell
python --version
```

確認済みのバージョンはPython 3.13です。

### 3. 仮想環境を作成する

```powershell
python -m venv .venv
```

### 4. 仮想環境を有効化する

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. 必要なPythonライブラリを導入する

正式入口に必要な外部ライブラリは `requests` だけです。

```powershell
python -m pip install -r requirements.txt
```

個別に導入する場合は次のコマンドです。

```powershell
python -m pip install requests
```

## Ollamaの準備

### モデルを導入する

```powershell
ollama pull qwen2.5:3b
```

### モデルを確認する

```powershell
ollama list
```

一覧に `qwen2.5:3b` が表示されることを確認してください。

### Ollamaを起動する

Ollamaが起動していない場合は、次のコマンドを使用します。

```powershell
ollama serve
```

すでにOllamaがサービスや別プロセスとして起動している場合は、追加で起動する必要はありません。

## 起動と終了

正式な起動方法は次の1つだけです。

```powershell
python -B chat_agent.py
```

終了するには、入力待ちで次のように入力します。

```text
終了
```

## 基本操作例

以下は架空の入力例です。

### 学習時間

```text
今日は25分勉強した
これまでの合計学習時間を教えて
```

### 学習トピック

```text
今日はベクトル検索を勉強した
これまで何を勉強した？
```

### 詳細記録と集計

```text
今日は機械学習を15分勉強した
トピック別の学習時間を教えて
今の学習状況を分析して
```

### 学習目標

```text
データ分析を90分勉強する目標にしたい
データ分析の目標まであとどれくらい？
```

### 複数依頼

```text
今日は20分勉強した。今の学習状況も分析して
学習したトピックとこれまでの学習時間を教えて
```

## 保存データ

通常時は、次の5ファイルをリポジトリ直下で使用します。

| ファイル | 用途 |
|---|---|
| `study_records.csv` | 学習時間 |
| `study_topics.csv` | 学習したトピック |
| `detailed_study_records.csv` | トピックと学習時間の詳細記録 |
| `study_goals.csv` | トピック別の目標時間 |
| `conversation_history.json` | CLIの会話履歴 |

これらのファイルには個人の学習記録が含まれるため、内容をREADME、Issue、チャット、公開リポジトリなどへ貼り付けないでください。

## 保存先を分離する

環境変数 `AI_LEARNING_DATA_DIR` を設定すると、5つの保存ファイルを別のフォルダへ切り替えられます。テストや検証を本番データから分離するために使用します。

指定先には次の条件があります。

- 絶対パスであること
- すでに存在するフォルダであること
- ファイルではないこと
- 空文字ではないこと
- ツールは保存先フォルダを自動作成しないこと

空文字、相対パス、存在しないパス、ファイルを指定すると `StorageConfigurationError` になります。

### PowerShellで設定する

先に検証専用フォルダを用意し、その絶対パスを指定します。

```powershell
$env:AI_LEARNING_DATA_DIR = "C:\absolute\path\to\test-data"
```

書込み処理を実行する前に、保存先が検証専用フォルダを指していることを確認してください。

### 設定を解除する

```powershell
Remove-Item Env:AI_LEARNING_DATA_DIR
```

検証後は環境変数を解除し、通常保存先へ戻してください。

## 本番データを変更しない安全なテスト

通常のWindows PowerShellから、正式に整備した次の4テストファイルだけを明示指定して実行します。

- `test_storage_isolation.py`
- `test_generate_final_answer_fallback.py`
- `test_response_formatter.py`
- `test_topic_list_routing.py`

### 実行前のメタデータ確認

本番ファイルの内容は開かず、存在状態、サイズ、更新日時だけを記録します。新規cloneなどで5ファイルがまだ存在しない場合も、`Exists=False`として記録します。

```powershell
$dataFiles = @(
  ".\study_records.csv"
  ".\study_topics.csv"
  ".\detailed_study_records.csv"
  ".\study_goals.csv"
  ".\conversation_history.json"
)

function Get-DataFileMetadata {
  foreach ($path in $dataFiles) {
    $item = Get-Item -LiteralPath $path -ErrorAction SilentlyContinue

    if ($null -eq $item) {
      [pscustomobject]@{
        Name = $path
        Exists = $false
        Length = $null
        LastWriteTimeUtc = $null
      }
    }
    else {
      [pscustomobject]@{
        Name = $path
        Exists = $true
        Length = $item.Length
        LastWriteTimeUtc = $item.LastWriteTimeUtc
      }
    }
  }
}

$before = @(Get-DataFileMetadata)
$before
```

### テストを実行する

```powershell
python -B -m unittest -v `
  test_storage_isolation.py `
  test_generate_final_answer_fallback.py `
  test_response_formatter.py `
  test_topic_list_routing.py
```

### 実行後のメタデータ比較

実行前と同じPowerShellセッションで、存在状態、サイズ、更新日時を比較します。

```powershell
$after = @(Get-DataFileMetadata)
$after

$changes = Compare-Object `
  -ReferenceObject $before `
  -DifferenceObject $after `
  -Property Name, Exists, Length, LastWriteTimeUtc

if ($changes) {
  $changes
  throw "本番5ファイルの存在、サイズ、更新日時に差があります。"
}
else {
  Write-Host "本番5ファイルの前後状態は一致しています。"
}
```

新規環境では未存在のファイルが前後とも`Exists=False`であること、既存環境では存在するファイルのサイズと更新日時が前後で一致することを確認できます。実行前の`$before`を保持するため、メタデータ取得、テスト、比較は同じPowerShellセッションで行ってください。

CodexのWindowsサンドボックスでは、AppData配下の `TemporaryDirectory` への書込み権限により `PermissionError` が発生した実績があります。安全な分離テストは通常のWindows PowerShellで実行してください。

### `unittest discover`を使用しない

このリポジトリには学習用・確認用の `*_test.py` が多数あり、すべてが安全なunittestとは限りません。`unittest discover`は使用せず、上記4ファイルを明示指定してください。

## 学習用・確認用スクリプトの注意

- `weekly_study.py` は固定された曜日別データを扱う初期学習用の補助スクリプトです。正式入口ではありません。
- 既存の `*_test.py` や `*_preview.py` は、安全なunittestとは限りません。
- `api_*.py`、`ollama_test.py`などは外部通信を行う可能性があります。
- 確認用スクリプトには、本番CSV・JSONを書き換える可能性があるものがあります。
- `study_tools.py` を直接実行すると学習時間を書き込むため、直接実行しないでください。
- 内容、通信先、保存先を確認していないスクリプトは実行しないでください。

## CLI版MVPの対象外

- GUI
- 日付別・週別集計
- 記録の編集・削除
- 既存CSVの統合
- `chat_loop.py`
- `csv_reader.py`
- `csv_writer.py`
- `study_data.csv`
- `chat_history.json`

`weekly_study.py` はMVP機能ではなく、初期学習用の補助スクリプトです。

## トラブルシューティング

### Ollamaとの通信に失敗する

Ollamaが起動しているか確認してください。停止中の場合は次を実行します。

```powershell
ollama serve
```

すでに起動済みの場合は、追加起動せず現在のプロセスを使用してください。

### `qwen2.5:3b` が導入されていない

モデル一覧を確認します。

```powershell
ollama list
```

モデルがない場合は導入します。

```powershell
ollama pull qwen2.5:3b
```

### 保存先設定エラーになる

次を確認してください。

- `AI_LEARNING_DATA_DIR` が空ではないか
- 相対パスではなく絶対パスか
- 指定したパスが存在するか
- フォルダではなくファイルを指定していないか

通常保存先へ戻す場合は設定を解除します。

```powershell
Remove-Item Env:AI_LEARNING_DATA_DIR
```

### Codex端末だけで日本語が文字化けする

`weekly_study.py` の確認では、Codex端末だけで日本語が文字化けし、通常PowerShellでは正常に表示された実績があります。処理結果の数値を確認したうえで、通常PowerShellから表示を確認してください。原因は断定していません。

## 機密情報の取り扱い

次の情報をREADME、ソースコード、テスト、Issue、チャット、公開リポジトリへ記録しないでください。

- APIキー、トークン、パスワード
- `.env` の内容
- 認証情報
- 個人固有の絶対パス
- 実際の学習時間、トピック、目標
- 個人の会話履歴
- 個人名やアカウント情報

Ollamaはローカル接続ですが、入力内容や保存データには個人情報・機密情報を含めないでください。
