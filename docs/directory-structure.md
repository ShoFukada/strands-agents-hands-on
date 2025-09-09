# コード構成方針（ディレクトリ設計）

本ドキュメントは、以下のセクション群を「ソースコード中心」で育てていくためのディレクトリ構成と運用方針をまとめたものです。

- strands agentsとは？
- エージェントを動かしてみる
- セッション管理（ローカル、S3）
- プロンプト
- hooks
- tools（python, mcp）
- model provider
- streaming
- エージェントをツールとして使用

## 結論（推奨）
「共有ライブラリ + セクション別の最小実行例（examples）」のハイブリッド構成を採用します。

- 共有ライブラリ（`src/`）に共通ロジック（エージェント初期化、セッション実装、ツール定義、hooks、provider 設定、ストリーミング補助）を集約。
- セクション別の実行例（`examples/NN_*`）は、最小限の `main.py` で「1トピック=1動作」を再現し、章ごとの再現性と独立性を担保。
- 番号付きディレクトリで学習順序と差分を明確化。共有ライブラリの進化で壊れないように、例側は薄く保ちます。

## ディレクトリツリー（初期案）
```
strands-agents-hands-on/
├─ src/
│  └─ strands_hands_on/
│     ├─ agents/            # エージェントの組み立て・実行制御
│     │  ├─ core.py
│     │  └─ registry.py
│     ├─ prompts/           # システム/テンプレート/プロンプト構築
│     │  ├─ base.py
│     │  └─ templates/
│     ├─ tools/             # ツール定義（Python/MCP）
│     │  ├─ python/
│     │  │  └─ arithmetic.py
│     │  └─ mcp/
│     │     ├─ client.py
│     │     └─ schemas.py
│     ├─ hooks/             # before/after などのフック群
│     │  └─ logging.py
│     ├─ providers/         # モデルプロバイダの切替層
│     │  ├─ base.py
│     │  ├─ openai.py
│     │  └─ anthropic.py
│     ├─ sessions/          # セッションの保存先
│     │  ├─ local_store.py
│     │  └─ s3_store.py
│     ├─ streaming/         # ストリーミング補助（分割/表示/整形）
│     │  └─ stream_utils.py
│     ├─ cli/               # エージェントをツールとして使う CLI
│     │  └─ __main__.py
│     └─ __init__.py
│
├─ examples/                # 各章の最小実行例（1ファイル完結を基本）
│  ├─ 01_run_agent/
│  │  └─ main.py
│  ├─ 02_session_local/
│  │  └─ main.py
│  ├─ 02_session_s3/
│  │  └─ main.py
│  ├─ 03_prompt/
│  │  └─ main.py
│  ├─ 04_hooks/
│  │  └─ main.py
│  ├─ 05_tools_python/
│  │  └─ main.py
│  ├─ 06_tools_mcp/
│  │  └─ main.py
│  ├─ 07_model_provider/
│  │  └─ main.py
│  ├─ 08_streaming/
│  │  └─ main.py
│  └─ 09_agent_as_tool/
│     └─ main.py
│
├─ configs/
│  ├─ .env.example          # APIキー/設定の雛形
│  ├─ provider.toml         # モデルや温度/トークン設定など
│  └─ mcp.json              # MCP サーバ設定の例
│
├─ tests/                   # 単体テスト（必要最小限）
│  ├─ test_agents.py
│  ├─ test_tools_python.py
│  └─ test_sessions.py
│
├─ scripts/                 # セットアップ/ユーティリティ
│  └─ bootstrap.sh
│
├─ docs/
│  └─ directory-structure.md  # 本ファイル
│
├─ pyproject.toml
└─ README.md
```

## 各ディレクトリの役割
- `src/strands_hands_on/agents/`: エージェントの生成・実行（ストリーミングやツール連携のハブ）。
- `prompts/`: システム/テンプレート/変数埋め込み。例では最小の関数かクラスを想定。
- `tools/python/`: 小粒な純粋関数を型付きで公開（例: `arithmetic.add`）。
- `tools/mcp/`: MCP クライアント、スキーマ、呼び出しラッパ。
- `hooks/`: ロギング/サニタイズ/ポリシー適用などの差し込みポイント。
- `providers/`: モデル/ベンダーの差し替え層（OpenAI/Anthropicなど）。
- `sessions/`: ローカル/S3 の保存実装とインターフェース。
- `streaming/`: チャンク表示/途中キャンセル/イベント変換など。
- `cli/`: `python -m strands_hands_on.cli --prompt "..."` のように使うための入口。
- `examples/`: 各章ごとに完結した `main.py`。共通ロジックは `src/` を使う。

## セクション → コード対応
- エージェントを動かしてみる → `examples/01_run_agent/main.py`
- セッション管理（ローカル） → `examples/02_session_local/main.py` + `src/.../sessions/local_store.py`
- セッション管理（S3） → `examples/02_session_s3/main.py` + `src/.../sessions/s3_store.py`
- プロンプト → `examples/03_prompt/main.py` + `src/.../prompts/*`
- hooks → `examples/04_hooks/main.py` + `src/.../hooks/*`
- tools（python） → `examples/05_tools_python/main.py` + `src/.../tools/python/*`
- tools（mcp） → `examples/06_tools_mcp/main.py` + `src/.../tools/mcp/*`
- model provider → `examples/07_model_provider/main.py` + `src/.../providers/*`
- streaming → `examples/08_streaming/main.py` + `src/.../streaming/*`
- エージェントをツールとして使用 → `examples/09_agent_as_tool/main.py` + `src/.../cli/__main__.py`

## 運用方針：番号で分けるか、どんどん更新か
- 単一を更新し続ける方式
  - 長所: ファイルが少なく見通しが良い
  - 短所: 章ごとの差分が消え、再現性・回帰検証が難しい
- 番号で分ける方式（推奨）
  - 長所: 再現性が高い、章ごとの目的が明確、レビュー/比較が容易
  - 短所: 重複の温床になりがち → 共有ライブラリに吸い上げて回避
- ハイブリッドの指針
  - 共通化できるものは `src/` に集約し、`examples/` はなるべく薄く保つ
  - 破壊的変更が必要な場合は `examples/03_prompt_v2` のように派生を作る

## 命名・進化ルール
- 例のディレクトリは `NN_topic` で揃える（例: `05_tools_python`）。
- 小改修なら同ディレクトリ内で完結。大きく概念が変わる場合のみ `v2` ディレクトリを新設。
- 共有ライブラリは後方互換を優先。互換を壊す場合は `experimental/`（またはブランチ）で先行検証。

## 実行と設定の目安
- セットアップ（例）
  - `pip install -e .` でローカルパッケージとして `src/` を参照
  - `cp configs/.env.example .env` で環境変数を用意
- 例の実行（例）
  - `python examples/01_run_agent/main.py`
  - `python -m strands_hands_on.cli --prompt "hello"`

## 次のアクション
1. `examples/01_run_agent/main.py` と `src/strands_hands_on/agents/core.py` の最小雛形を作成
2. `configs/.env.example` にモデル/キー項目を定義
3. セッション（ローカル）→ プロンプト → hooks → tools（python）…の順に段階的に追加

> この構成であれば、章ごとの再現性とコードの重複最小化の両立ができます。必要に応じて調整しましょう。
