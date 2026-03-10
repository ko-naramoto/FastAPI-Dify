import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx

import auth
import models
import schemas
from database import get_db

# 環境変数からDifyの設定を読み込む
DIFY_API_URL = os.getenv("DIFY_API_URL")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

router = APIRouter(
    dependencies=[Depends(auth.get_current_user)]
)


@router.post("/invoke", response_model=schemas.DifyInvokeResponse)
async def invoke_dify_app(
    request: schemas.DifyInvokeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Difyのチャットアプリケーションを呼び出し、応答を取得します。
    """
    if not DIFY_API_URL or not DIFY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dify API URL or Key is not configured in the environment.",
        )

    # Difyに渡す前に、指定されたカテゴリIDがDBに存在するかチェックします。
    category = db.get(models.Category, request.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {request.category_id} not found",
        )

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": {
            "category_id": str(request.category_id) # Difyのプロンプト変数は通常文字列として扱われるため、str()で変換します。
        },
        "query": request.query,
        "user": current_user.username,
        "conversion_id": None, #request.conversation_id or None,
        "response_mode": "blocking",  # ストリーミングの場合は "streaming"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(DIFY_API_URL, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status() # 2xx以外のステータスコードで例外を発生させる
            print(response.text)
            dify_response = response.json()

            # Difyのレスポンス形式に合わせて調整します
            return schemas.DifyInvokeResponse(
                answer=dify_response.get("answer", ""),
                conversation_id=dify_response.get("conversation_id", "")
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Dify API: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to Dify API: {e}",
            )