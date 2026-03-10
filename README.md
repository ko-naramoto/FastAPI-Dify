
FastAPI-Dify
============

概要
----
このワークスペースは、FastAPI + SQLAlchemy で構成された簡易ナレッジ管理APIです。ユーザー管理、カテゴリ、ドキュメント、検索ログのCRUDに加え、Dify API への問い合わせを中継するエンドポイントを提供します。

主な構成
--------
- `src/main.py`: FastAPI アプリのエントリ。各ルーターを登録。
- `src/database.py`: DB接続（SQLAlchemy）と `get_db` 依存性、`get_object_or_404` ヘルパ。
- `src/models.py`: User / Category / Document / SearchLog のORM定義。
- `src/schemas.py`: Pydantic スキーマ（入出力の型）。
- `src/auth.py`: パスワードハッシュ、JWT発行/検証、認証依存性。
- `src/routers/`: APIルーター群（users, categories, documents, search_logs, dify）。
- `src/seed.py`: 初期データ投入スクリプト。

データモデル概要
---------------
- User: `username`, `password(ハッシュ)`
- Category: `name`, `created_at`（1対多でDocumentと関連）
- Document: `category_id`, `title`, `content`, `created_at`
- SearchLog: `query`, `answer`, `result`, `category_id(任意)`, `created_at`

認証
----
- OAuth2 Password Flow（`/users/login`）でJWTを発行。
- `Authorization: Bearer <token>` で保護されたAPIにアクセス。
- 現状、`documents` と `dify` は認証必須。
  - `categories` と `search_logs` は認証がコメントアウトされており、未保護。

APIエンドポイント（主要）
------------------------
- Users: `POST /users/`, `POST /users/login`, `GET /users/me`
- Categories: `POST /categories/`, `GET /categories/`, `GET /categories/{id}`,
  `GET /categories/{id}/documents`, `PUT /categories/{id}`, `DELETE /categories/{id}`
- Documents: `POST /documents/`, `GET /documents/`, `GET /documents/{id}`,
  `PUT /documents/{id}`, `DELETE /documents/{id}`
- SearchLogs: `POST /search_logs/`, `GET /search_logs/`
- Dify: `POST /dify/invoke`

環境変数
--------
- `SQLALCHEMY_DATABASE_URL`: DB接続文字列（未設定時は `sqlite:///./default.db`）
- `JWT_SECRET_KEY`: JWT署名用シークレット
- `ALGORITHM`: JWTアルゴリズム（例: `HS256`）
- `ACCESS_TOKEN_EXPIRE_MINUTES`: アクセストークン有効期限（分）
- `DIFY_API_URL`: Dify APIのエンドポイント
- `DIFY_API_KEY`: Dify APIキー

補足
----
- `src/seed.py` は初期ユーザー・カテゴリ・ドキュメントを投入するユーティリティです。
- `src/app.db` が同梱されていますが、実際に使用されるDBは `SQLALCHEMY_DATABASE_URL` の設定に依存します。
