from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from openai import OpenAI
from app.core.config import settings
from app.routers.properties import get_current_user
from app.models.user import User

router = APIRouter()

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
async def ask_ai(
    request: AskRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful real estate assistant."},
                {"role": "user", "content": request.question}
            ]
        )
        answer = response.choices[0].message.content
        return AskResponse(answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
