# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

journal.pyは、JSON形式でログエントリを保存・取得できるシンプルなジャーナルサーバーです。FastAPIを使用してHTTP APIを提供し、SQLiteデータベースでデータを永続化します。

## 開発環境のセットアップとコマンド

このプロジェクトはuvを使用して依存関係を管理しています：

```bash
# 依存関係のインストール
uv sync

# 開発環境でサーバーを起動
fastapi dev --host 0.0.0.0 --port 8000 --reload journal.py

# コードフォーマット
uv run black journal.py
uv run isort journal.py

# Lint実行
uv run ruff check journal.py
```

## アーキテクチャ

- **journal.py**: FastAPIアプリケーションのエントリーポイント
- **データベース**: SQLite（現在は未実装、実装が必要）
- **API設計**: RESTful APIでセクションとキーによる構造化されたジャーナルエントリ

### データベーススキーマ
```sql
CREATE TABLE IF NOT EXISTS journal (
    section TEXT NOT NULL,
    key TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    data TEXT NOT NULL,
    PRIMARY KEY (section, key, timestamp)
);
```

### API エンドポイント
- `POST /journal/{section}/{key}` - ログエントリの作成
- `GET /journal/{section}/{key}` - ログエントリの取得

## 現在の実装状況

journal.pyは基本的なFastAPIアプリケーション構造のみが定義されており、実際のデータベース操作やAPIロジックは未実装です。完全な実装にはSQLite接続とCRUD操作の追加が必要です。

## セキュリティ注意事項

このアプリケーションは認証機能を持たず、すべてのデータが公開されることを前提としています。機密データには適しません。
