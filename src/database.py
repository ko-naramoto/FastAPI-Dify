import os
from typing import Type, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import HTTPException, Depends

# データベース接続設定
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./default.db")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ジェネリクス型定義
T = TypeVar("T")

Base = declarative_base()

# DBセッション取得（共通依存関係）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 汎用的なモデル取得
def get_object_or_404(model: Type[T]):
    def _dependency(id: int, db: Session = Depends(get_db)) -> T:
        db_obj = db.get(model, id)
        if not db_obj:
            raise HTTPException(
                status_code=404, 
                detail=f"{model.__name__} not found"
            )
        return db_obj
    return _dependency