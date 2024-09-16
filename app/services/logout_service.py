from fastapi import Depends, Response, HTTPException, status, Request
from app.utils.db_handlers.redis_handler import RedisHandler
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.deps import get_current_user
import requests


class LogoutService:
    def __init__(self, redis_handler: RedisHandler, mongodb_handler: MongoDBHandler):
        self.redis_handler = redis_handler
        self.mongodb_handler = mongodb_handler

    async def logout(self, request: Request, response: Response, user: dict = Depends(get_current_user)):
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # 구글(카카오) 로그아웃 처리
        if user.get("auth_provider") == "google":
            self.logout_google(user)
        elif user.get("auth_provider") == "kakao":
            self.logout_kakao(user)

        # redis session 삭제
        session_id = user.get("session_id")
        if session_id:
            await self.redis_handler.delete(session_id)

        # mongodb session 삭제
        user_id = user.get("user_id")
        if user_id:
            self.mongodb_handler.delete_user_session(user_id)

        # cookie session_id 삭제
        response.delete_cookie(key="session_id")

        return {"message": "로그아웃"}

    def logout_google(self, user):
        # 구글 로그아웃 API 호출
        token = user.get("access_token")
        if token:
            requests.get(f"https://accounts.google.com/o/oauth2/revoke?token={token}")

    def logout_kakao(self, user):
        # 카카오 로그아웃 API 호출
        token = user.get("access_token")
        if token:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            requests.post("https://kapi.kakao.com/v1/user/logout", headers=headers)