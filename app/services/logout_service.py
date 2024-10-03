# logout_service.py
import requests
from fastapi import Request, Response, HTTPException, status
from typing import Optional
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.utils.db_handlers.redis_handler import RedisHandler
from app.deps import get_session_coll, get_session_cache


class LogoutService:
    def __init__(self, 
                 session_coll: Optional[MongoDBHandler] = None,
                 session_cache: Optional[RedisHandler] = None):
        self.session_coll = session_coll if session_coll else get_session_coll()
        self.session_cache = session_cache if session_cache else get_session_cache()

    async def logout(self, request: Request, response: Response) -> dict:
        # 쿠키에서 세션 id를 가져옴
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No session_id in cookie")

        # redis, mongoDB에서 세션 조회
        session_data = await self.session_cache.select(session_id)
        if not session_data:
            session_data = await self.session_coll.select({"_id": session_id})
            if not session_data:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

        user_identifier = session_data.get("identifier")
        
        # redis와 mongoDB에서 세션 삭제
        await self.session_cache.delete(session_id)
        await self.session_coll.delete({"_id": session_id})

        # 구글 로그아웃 처리
        if session_data.get("provider") == "google":
            self.google_logout(request)

        # 카카오 로그아웃 처리
        elif session_data.get("provider") == "kakao":
            self.kakao_logout(request)

        # 쿠키 삭제
        response.delete_cookie(key="session_id")

        return {"message": "Logout successful"}

    # token 이 none이 나옴
    def google_logout(self, request: Request):
        token = request.cookies.get("access_token")
        if token:
            requests.get(f"https://accounts.google.com/o/oauth2/revoke?token={token}")

    def kakao_logout(self, request: Request):
        token = request.cookies.get("access_token")
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            requests.post("https://kapi.kakao.com/v1/user/logout", headers=headers)


def get_logout_service() -> LogoutService:
    return LogoutService()