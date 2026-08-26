# AI Learning

AIエンジニアリングの学習を、自然な日本語で記録・集計できるローカルCLIツールです。ローカルLLMに「どの処理を実行するか」を判断させ、学習時間、トピック、目標、詳細記録、会話履歴をCSV／JSONに保存します。

このリポジトリは、LLMを単なるチャット相手として使うだけでなく、自然言語とPythonの処理を安全につなぐ仕組みを学び、改善した過程をまとめたものです。

> **関連プロジェクト**
>
> **AI OFFICE** は成果を見せるためのポートフォリオアプリ、**AI Learning** は学習を継続しながらローカルLLM活用を記録・検証するためのツール、という位置付けです。

## できること

- 学習時間の追加と累計の確認
- 学習トピックの追加と履歴表示
- トピックと時間を組み合わせた詳細記録
- トピック別学習時間の集計と学習状況の分析
- トピック別目標の設定と進捗確認
- 1つの入力に含まれる複数依頼の順次実行
- 直近の会話履歴を踏まえた応答
- ツールを使わない一般的な学習相談

## 仕組み

```text
ユーザー入力
    ↓
Ollama / qwen2.5:3b がJSON形式でツールを選択
    ↓
入力・ツール名を検証
    ↓
登録済みPython関数だけを実行
    ↓
定型フォーマットで結果を表示し、CSV／JSONへ保存
```

Ollamaは `http://localhost:11434/api/chat` で動く `qwen2.5:3b` を使用します。LLMの返答をそのままコードとして実行せず、`tool_registry.py` に登録済みの関数だけを呼び出します。記録を伴う依頼かどうかや返答JSONの型も検証し、ツール実行結果はLLMへ再送せず決定的な書式で表示します。

## 技術構成

- Python 3.13
- Ollama / `qwen2.5:3b`
- Requests
- CSV / JSONによるローカル保存
- `unittest` / `unittest.mock`
- GitHub Actions

## セットアップ

Windows PowerShellでの例です。

```powershell
git clone <repository-url>
cd ai-learning
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ollama pull qwen2.5:3b
```

Ollamaが常駐していない環境では、別のターミナルで起動します。

```powershell
ollama serve
```

## 使い方

正式なCLI入口は `chat_agent.py` です。

```powershell
python -B chat_agent.py
```

入力例：

```text
あなた：今日はRAGを30分勉強した
AI：RAGの学習時間30分を記録しました。

あなた：トピック別の学習時間を教えて
AI：RAG：30分

あなた：RAGを120分勉強する目標にしたい
AI：RAGの目標学習時間を120分に設定しました。
```

`終了` と入力するとCLIを終了します。表示文はデータやバージョンにより異なる場合があります。

## 保存データとプライバシー

通常は次の実行データをリポジトリ直下に作成します。これらは個人ログのためGit管理しません。

| ファイル | 内容 | Gitでの扱い |
|---|---|---|
| `study_records.csv` | 学習時間 | 管理しない |
| `study_topics.csv` | 学習トピック | 管理しない |
| `study_goals.csv` | トピック別目標 | 管理しない |
| `detailed_study_records.csv` | トピックと時間の詳細記録 | 管理しない |
| `conversation_history.json` | CLIの会話履歴 | 管理しない |
| `chat_history.json` | 旧スクリプトの会話履歴 | 管理しない |

`.env`、会話履歴、個人の学習ログは `.gitignore` の対象です。秘密情報や実際の個人データをREADME、Issue、公開リポジトリへ掲載しないでください。

一方、追跡済みの `study_data.csv` は初期学習用スクリプトで使う小さなサンプル／初期データとして残しています。個人ログの保存先には使用しません。

環境変数 `AI_LEARNING_DATA_DIR` に既存フォルダの絶対パスを指定すると、実行データをリポジトリ外へ分離できます。

```powershell
New-Item -ItemType Directory -Force C:\path\to\ai-learning-data
$env:AI_LEARNING_DATA_DIR = "C:\path\to\ai-learning-data"
python -B chat_agent.py
```

未指定時はリポジトリ直下を使用します。空文字、相対パス、存在しないパス、ファイルのパスは安全のため拒否します。

## テストと安全設計

CIと同じ、外部サービス不要のテストは次のコマンドで実行できます。

```powershell
python -B -m unittest -v test_storage_isolation.py test_generate_final_answer_fallback.py test_response_formatter.py test_topic_list_routing.py
```

このテスト群は以下を確認します。

- 一時ディレクトリによる個人データとの分離
- 保存先設定の検証
- Ollama通信失敗時のフォールバック
- 不正なJSONや型の拒否
- 表示形式、ツール選択補正、意図しない書込みの防止

GitHub Actionsでも同じ49件を実行し、Ollamaへの実通信は行いません。リポジトリには学習過程で作成した `*_test.py` や `*_preview.py` もありますが、一部はスクリプト形式で、外部通信や実データへの書込みを伴う可能性があります。そのため `unittest discover` ではなく、上記の検証済みファイルを明示しています。

Ollamaとの実通信はローカルでのみ確認します。`ollama list` で `qwen2.5:3b` と起動状態を確認してからCLIを実行し、一般会話や記録入力を試してください。個人ログを守るには `AI_LEARNING_DATA_DIR` を検証用フォルダへ設定してください。

## 主要ファイル

| ファイル | 役割 |
|---|---|
| `chat_agent.py` | 正式なCLI入口。会話、ツール実行、履歴保存を統括 |
| `tool_selector.py` | Ollamaへの問い合わせ、自然言語からのツール選択、入力検証 |
| `tool_registry.py` | LLMから呼出し可能なPython関数の許可リスト |
| `study_tools.py` | 学習時間の記録、累計、時間換算 |
| `study_topic_tools.py` | 学習トピックの記録と一覧取得 |
| `study_goal_tools.py` | 目標設定と進捗計算 |
| `detailed_study_tools.py` | 詳細記録、トピック別集計、分析用データ生成 |
| `response_formatter.py` | ツール結果を安定した表示文へ変換 |
| `storage_paths.py` | 保存先の解決と安全性検証 |
| `memory_manager.py` | 会話履歴の保存、分割、要約 |
| `weekly_study.py` | 固定データを扱う初期学習用の補助スクリプト |
| `test_storage_isolation.py` | 保存先分離とデータ保護のテスト |
| `test_generate_final_answer_fallback.py` | 通信失敗時のフォールバックテスト |
| `test_response_formatter.py` | 応答形式と異常系のテスト |
| `test_topic_list_routing.py` | ツール選択・補正ロジックのテスト |

## 現在のスコープ

学習用のローカルCLIとして、記録・集計・目標管理とLLM連携に焦点を当てています。GUI、記録の編集／削除、クラウド同期、外部APIや有料サービスとの連携は対象外です。
