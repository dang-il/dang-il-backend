from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from auth.schemas import User
from auth.utils import create_session, get_current_user
from core.config import settings

router = APIRouter()


@router.get("/login")
def login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)


@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "code": code,
            },
        )
        token_data = token_response.json()

        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error_description"])

        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_data = user_response.json()

        user = User(
            id=user_data["id"],
            email=user_data["email"],
            name=user_data["name"],
        )

        create_session(request, user)

    return JSONResponse(content={"message": "Login Success"})


@router.get("/me", response_model=User)
def me(user: User = Depends(get_current_user)):
    return user
