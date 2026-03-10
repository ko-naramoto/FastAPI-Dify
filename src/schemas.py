from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# --- Schemas for Document ---
class DocumentBase(BaseModel):
    title: str = Field(max_length=255)
    content: str


class DocumentCreate(DocumentBase):
    category_id: int


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    category_id: Optional[int] = None


class Document(DocumentBase):
    id: int
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Schemas for Category ---
class CategoryBase(BaseModel):
    name: str = Field(max_length=255)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)


class Category(CategoryBase):
    id: int
    created_at: datetime
    documents: List[Document] = []

    class Config:
        from_attributes = True


# --- Schemas for SearchLog ---
class SearchLogBase(BaseModel):
    query: str
    answer: str
    result: int
    category_id: Optional[int] = None


class SearchLogCreate(SearchLogBase):
    pass


class SearchLog(SearchLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schemas for Dify ---
class DifyInvokeRequest(BaseModel):
    query: str
    category_id: int
    # user: str  # Dify側でユーザーを識別するためのID
    # conversation_id: Optional[str] = None # 既存の会話ID

class DifyInvokeResponse(BaseModel):
    answer: str
    conversation_id: str
