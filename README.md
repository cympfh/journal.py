# journal.py - journal server

A Simple Server as a Logging Service

This journal server is a simple logging server that stores arbitrary values (in JSON format) associated with section and key pairs, along with timestamps.

journal server は `section`, `key` に紐づく自由な値（JSON形式）をタイムスタンプ付きで保存するだけのシンプルなロギングサーバです。

## Working on

http://s.cympfh.cc/journal

## Launch

```bash
uv sync  # Install dependencies
fastapi run --host 0.0.0.0 --port 8000 --reload journal.py
```

## APIs

You can see detailed API documentation at: http://s.cympfh.cc/journal/docs

### Post Logging

```bash
POST /journal/{section}/{key} --data '{ free-JSON data }'

Optional query parameters:

- `timestamp`: timestamp of the log entry
    - format: YYYY-MM-DD HH:MM:SS
    - if not provided, the current timestamp will be used

Examples:

POST http://s.cympfh.cc/journal/cympfh/diary --data '{"title": "My first log", "content": "This is the content of my first log."}'
POST http://s.cympfh.cc/journal/tokyo/temperature --data '{"temperature": 32, "humidity": 63}'
POST http://s.cympfh.cc/journal/tokyo/temperature?timestamp=2023-10-01 12:00:00 --data '{"temperature": 24, "humidity": 60}'
```

### Get Loggings

```bash
GET /journal/{section}/{key}

Optional query parameters:

- `tail`: number of entries to return (default: 10)
- `from`: timestamp to start from
    - format: YYYY-MM-DD HH:MM:SS

Examples:

GET http://s.cympfh.cc/journal/cympfh/diary?tail=5
GET http://s.cympfh.cc/journal/tokyo/temperature?from=2023-10-01
```

## Database

SQLite database is used to store the data.

```sql
CREATE TABLE IF NOT EXISTS journal (
    section TEXT NOT NULL,
    key TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    data TEXT NOT NULL,
    PRIMARY KEY (section, key, timestamp)
);
```

## Note

All stored data is open, and anyone can read it.
This product does not support authentication.
Don't store any secret data.
If you want, I recommend you to encrypt your data before sending it to the server.

データはすべて平文で保存されており, 誰でもデータにアクセスできる可能性があります.
もし必要なら自分で暗号化したデータを入れることを検討してください.
何にせよ秘匿データを入れないで下さい.
