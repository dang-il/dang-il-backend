#libraries
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

# 의존성 
from app.deps import get_user_coll
from app.services.auth_service import get_auth_service, AuthService
# DTO 
from app.schemas.service_dto.auth_dto import (
    AuthGoogleCallbackInput as GoogleCallbackInput, 
    AuthGoogleCallbackOutput as GoogleCallbackOutput,
    AuthGoogleRegisterInput as GoogleRegisterInput,   
    AuthGoogleRegisterOutput as GoogleRegisterOutput,
    AuthGoogleLoginInput as GoogleLoginInput,
    AuthGoogleLoginOutput as GoogleLoginOutput,
)
from app.schemas.request_dto.auth_request import (
    AuthCallbackRequest 
)
from app.schemas.response_dto.auth_response import (
    AuthGoogleCallbackResponse as GoogleCallbackResponse,
)
# 기타 사용자 모듈
from app.configs.config import settings
from app.utils.db_handlers.mongodb_handler import MongoDBHandler

router = APIRouter()

@router.get("/google/login")
async def auth_google_login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid%20email%20profile"
    )
    return RedirectResponse(google_auth_url)

@router.post("/google/callback", response_model=GoogleCallbackResponse)
async def auth_google_callback(post_input: AuthCallbackRequest,
                               request: Request,
                               response: Response,
                               auth_service: AuthService = Depends(get_auth_service),
                               user_coll: MongoDBHandler = Depends(get_user_coll)):
    # 쿼리 파라미터에서 인증코드 받기, 없으면 400에러
    code = post_input.code
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")
    
    # 인증 코드 기반으로 google에 엑세스 토큰 요청해 사용자 정보 받기
    google_callback_input = GoogleCallbackInput(
        code = code
    )
    user_data: GoogleCallbackOutput = await auth_service.google_callback(google_callback_input)
    
    # 기존에 존재하는 유저이면 로그인, 아니면 회원가입
    if(await user_coll.select({"_id": user_data.id}) == False):
        register_login_result: GoogleRegisterOutput = await auth_service.google_register(user_data)
        response_message = "register process is complete"
        response_action_type = "register"
    else:
        login_input = GoogleLoginInput(
            _id = user_data.id,
            name = user_data.name,
            email = user_data.email,
            session_id = request.cookies.get("session_id")
        )
        register_login_result: GoogleLoginOutput = await auth_service.google_login(login_input)
        response_message = "login process is complete"
        response_action_type = "login"
        
    # 반환된 정보로 세션id 쿠키 삽입, 응답 생성
    session_cookie = {
        "key":"session_id",
        "value":register_login_result.session_id,
        "expires": register_login_result.expires,
        "httponly":True,
        "secure":True,
        "samesite":'Lax'
    }
    response.set_cookie(**session_cookie)
    
    return GoogleCallbackResponse(
        message=response_message,
        action_type=response_action_type
    )
    