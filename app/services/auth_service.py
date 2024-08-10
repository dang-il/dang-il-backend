# libraries
import datetime
from httpx import AsyncClient
from fastapi.exceptions import HTTPException
from secrets import token_hex
from asyncio import create_task, gather
from typing import Optional

# DTO import
from app.schemas.service_dto.auth_dto import (
    AuthCallbackInput,
    AuthCallbackOutput,
    AuthLoginInput,
    AuthLoginOutput,
    AuthRegisterInput,
    AuthRegisterOutput,
)
from app.schemas.database_dto.db_schemas import UserColl, SessionColl
# 기타 사용자 모듈
from app.configs.config import settings
from app.services.abs_service import AbsService
from app.deps import get_user_coll, get_session_coll, get_session_cache
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.utils.db_handlers.redis_handler import RedisHandler

class AuthService(AbsService):
    instance: Optional["AuthService"] = None
    # 싱글톤 반환
    @classmethod
    def get_instance(cls) -> "AuthService":
        if(cls.instance is None):
            cls.instance = cls()
        return cls.instance
        
    # 구글 로그인 처리(callback)
    @staticmethod
    async def google_callback(input: AuthCallbackInput)->AuthCallbackOutput:
        async with AsyncClient() as client:
            print("auth code: ", input.code)
            
            post_data = {
                    "grant_type": "authorization_code",
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "code": input.code,
                }
            
            print("post_data: ",post_data)
            
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data = post_data,
            )
            
            print("acc_token_res: " ,token_response)
            print("acc_token: ", token_response.json())
            # 엑세스 토큰 
            token_data = token_response.json()
        
            # 엑세스 토큰이 안올때 400이 맞나, 애매한데 
            if "error" in token_data:
                    raise HTTPException(status_code=400, detail=token_data["error_description"])
            
            # 엑세스 토큰 기반으로 구글에 사용자 정보 받기
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
        
        # 받아온 유저 정보
        user_data = user_response.json()
        user_data["_id"] = user_data.pop("id")
        
        return AuthCallbackOutput(**user_data)
    
    # 카카오 로그인 처리(callback)
    @staticmethod
    async def kakao_callback(input: AuthCallbackInput)->AuthCallbackOutput:
        async with AsyncClient() as client:
            print("auth code: ", input.code)
            
            post_data = {
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": input.code,
                }
            
            print("post_data: ",post_data)
            
            token_response = await client.post(
                "https://kauth.kakao.com/oauth/token",
                data = post_data,
            )
            
            print("acc_token_res: " ,token_response)
            print("acc_token: ", token_response.json())
            # 엑세스 토큰 
            token_response.raise_for_status()
            token_data = token_response.json()
        
            # 엑세스 토큰이 안올때 400이 맞나, 애매한데 
            if "error" in token_data:
                    raise HTTPException(status_code=400, detail=token_data["error_description"])
            
            # 엑세스 토큰 기반으로 구글에 사용자 정보 받기
            user_response = await client.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
        
        # 받아온 유저 정보
        user_response.raise_for_status()
        user_data = user_response.json()
        user_data["_id"] = user_data.pop("id")
        
        return AuthCallbackOutput(**user_data)
    
    @staticmethod
    async def register(input: AuthRegisterInput,
                           user_coll: MongoDBHandler=get_user_coll(),
                           session_coll: MongoDBHandler=get_session_coll(),
                           session_cache: RedisHandler=get_session_cache())->AuthRegisterOutput:
        # 사용자 태그 선택
        user_coll_conn = user_coll.get_collection_conn()
        user_tag = (str(await user_coll_conn.count_documents({})).zfill(5))[::-1]
        
        # user_coll, session_coll, session_cache에 insert
        user_document = UserColl(
            _id = input.id,
            name = input.name,
            email = input.email,
            tag = user_tag
        )
        session_document = SessionColl(
            _id = token_hex(16),
            identifier = input.id,
            created_at = datetime.datetime.now(datetime.timezone.utc)
        )
        session_cache_document = SessionColl(
            _id = session_document.id,
            identifier = input.id,
            created_at = str(session_document.created_at)
        )
        
        user_document_dict = user_document.model_dump(by_alias=True, exclude_none=True)
        session_document_dict = session_document.model_dump(by_alias=True, exclude_none=True)
        session_cache_document_dict = session_cache_document.model_dump(by_alias=True, exclude_none=True)
        # 이거 비동기+멀티스레드 조합, 나중에 단위테스트로 성능 비교
        user_coll_task = create_task(user_coll.insert(user_document_dict))
        session_coll_task = create_task(session_coll.insert(session_document_dict))
        session_cache_task = create_task(session_cache.insert(session_cache_document_dict))
        await gather(user_coll_task, session_coll_task, session_cache_task)
        
        # 레디스 ttl 만료 설정
        session_cache_id = session_document.id
        ttl = int(datetime.timedelta(days=3).total_seconds())
        session_cache_conn = await session_cache.get_redis_conn()
        await session_cache_conn.expire(session_cache_id, ttl)
        
        return AuthRegisterOutput(
            session_id = session_document.id,
            expires = (session_document.created_at + datetime.timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        )
        
    @staticmethod
    async def login(input: AuthLoginInput,
                           session_coll: MongoDBHandler=get_session_coll(),
                           session_cache: RedisHandler=get_session_cache())->AuthLoginOutput:
        # 세션 id 존재하는 경우 삭제, 또는 존재하는 identifier인 경우 삭제
        # 만료시간 연장도 되지만 로직이 복잡해짐 그냥 삭제 후 다시 만들기로
        if(input.session_id is not None):
            session_delete_task = create_task(session_coll.delete({"_id": input.session_id}))
            session_cache_delete_task = create_task(session_cache.delete(input.session_id))
            
            await gather(session_delete_task, session_cache_delete_task)
        session_exist_check = create_task(session_coll.select({"identifier": input.id}))
        session_cache_exist_check = create_task(session_cache.select({"identifer": input.id}))
        if(await session_exist_check != False or await session_cache_exist_check != False):
            session_delete_task = create_task(session_coll.delete({"_id": input.session_id}))
            session_cache_delete_task = create_task(session_cache.delete(input.session_id))
            
            await gather(session_delete_task, session_cache_delete_task)
            
        # 세션 생성
        session_document = SessionColl(
            _id = token_hex(16),
            identifier = input.id,
            created_at = datetime.datetime.now(datetime.timezone.utc)
        )
        session_cache_document = SessionColl(
            _id = session_document.id,
            identifier = input.id,
            created_at = str(session_document.created_at)
        )
        
        session_document_dict = session_document.model_dump(by_alias=True)
        session_cache_document_dict = session_cache_document.model_dump(by_alias=True)
        # 이거 비동기+멀티스레드 조합, 나중에 단위테스트로 성능 비교
        session_coll_task = create_task(session_coll.insert(session_document_dict))
        session_cache_task = create_task(session_cache.insert(session_cache_document_dict))
        await gather(session_coll_task, session_cache_task)
        
        # 레디스 ttl 만료 설정
        session_cache_id = session_document.id
        ttl = int(datetime.timedelta(days=3).total_seconds())
        session_cache_conn = await session_cache.get_redis_conn()
        await session_cache_conn.expire(session_cache_id, ttl)
        
        return AuthLoginOutput(
            session_id = session_document.id,
            expires = (session_document.created_at + datetime.timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        )        
        
# 의존성 반환
def get_auth_service()->AuthService:
    return AuthService.get_instance()
