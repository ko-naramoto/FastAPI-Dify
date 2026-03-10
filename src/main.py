from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers import categories, documents, search_logs, users, dify
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search_logs.router, prefix="/search_logs", tags=["search_logs"])
app.include_router(dify.router, prefix="/dify", tags=["dify"])
