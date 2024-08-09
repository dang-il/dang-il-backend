from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from auth.schemas import User
from auth.utils import create_session, get_current_user
from core.config import settings

router = APIRouter()

@router.get("/login")
def login():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URI}&response_type=code"
    )
    return RedirectResponse(kakao_auth_url)

@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
            )
            token_response.raise_for_status()
            token_data = token_response.json()

            if "error" in token_data:
                raise HTTPException(status_code=400, detail=token_data["error_description"])

            user_response = await client.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            user_response.raise_for_status()
            user_data = user_response.json()

            user = User(
                id=str(user_data["id"]),  # id를 문자열로 변환
                email=user_data["kakao_account"]["email"],
                name=user_data["properties"]["nickname"],
            )

            create_session(request, user)
            return JSONResponse(content={"message": "Login Success"})

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me", response_model=User)
def me(user: User = Depends(get_current_user)):
    return user
