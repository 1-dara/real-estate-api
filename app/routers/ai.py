from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from google import genai
from app.core.config import settings
from app.routers.properties import get_current_user
from app.models.user import User

router = APIRouter()

client = genai.Client(api_key=settings.GEMINI_API_KEY)


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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"You are a helpful real estate assistant. Answer concisely.\n\nQuestion: {request.question}",
        )
        return AskResponse(answer=response.text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
