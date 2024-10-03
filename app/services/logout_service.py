from fastapi import Depends, HTTPException, status, Request, Response
from app.deps import get_user_coll, get_session_cache, get_session_coll
from app.utils.db_handlers.redis_handler import RedisHandler
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.schemas.response_dto.auth_response import AuthLogoutResponse
import requests

class LogoutService:
    def __init__(self, 
                 user_coll: MongoDBHandler = Depends(get_user_coll), 
                 session_cache: RedisHandler = Depends(get_session_cache),
                 session_coll: MongoDBHandler = Depends(get_session_coll)):
        self.user_coll = user_coll
        self.session_cache = session_cache
        self.session_coll = session_coll

    async def logout(self, request: Request, response: Response) -> AuthLogoutResponse:
        # 쿠키에서 세션 ID를 가져옴
        print(f"session_cache 타입: {type(self.session_cache)}")
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session ID not found")

        # Redis에서 세션 정보 삭제
        redis_result = await self.session_cache.delete_session(session_id)
        if not redis_result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete Redis session")

        # MongoDB에서 세션 정보 삭제
        mongodb_result = await self.session_coll.delete({"_id": session_id})
        if not mongodb_result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete MongoDB session")

        # 구글/카카오 세션 로그아웃 처리
        self.revoke_social_session(request)

        # 쿠키 삭제
        response.delete_cookie(key="session_id")

        return AuthLogoutResponse(message="Successfully logged out")

    def revoke_social_session(self, request: Request):
        # 구글 로그아웃 처리
        self.google_logout(request)
        
        # 카카오 로그아웃 처리
        self.kakao_logout(request)

    def google_logout(self, request: Request):
        # 구글 액세스 토큰 무효화
        token = request.cookies.get("access_token")
        if token:
            requests.get(f"https://accounts.google.com/o/oauth2/revoke?token={token}")

    def kakao_logout(self, request: Request):
        # 카카오 액세스 토큰 무효화
        token = request.cookies.get("access_token")
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            requests.post("https://kapi.kakao.com/v1/user/logout", headers=headers)

# 의존성 주입 함수
def get_logout_service() -> LogoutService:
    return LogoutService()
