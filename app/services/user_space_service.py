# libralies
from typing import Optional
from asyncio import create_task, gather
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone, timedelta
# dto
from app.schemas.service_dto.user_space_dto import (
    GetUserSpaceInput, 
    GetUserSpaceOutput,
)
# 기타 사용자 모듈
from app.services.abs_service import AbsService
from app.deps import get_user_space_coll, get_user_tasking_time_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler

class UserSpaceService(AbsService):
    instance: Optional["UserSpaceService"] = None
    # 싱글톤 반환
    @classmethod
    def get_instance(cls) -> "UserSpaceService":
        if(cls.instance is None):
            cls.instance = cls()
        return cls.instance
    
    @staticmethod
    async def get_user_space_data(input: GetUserSpaceInput,
                                user_space_coll: MongoDBHandler = get_user_space_coll(),
                                user_tasking_time_coll: MongoDBHandler = get_user_tasking_time_coll())->GetUserSpaceOutput:
        user_id = input.id
        
        # 태스트 생성
        user_space_task = create_task(user_space_coll.select({"_id": user_id}))
        user_tasking_time_task = create_task(user_tasking_time_coll.select({"_id": user_id}))
        
        return GetUserSpaceOutput(
            user_space_data=await user_space_task,
            user_tasking_time_data=await user_tasking_time_task
        )
        
    @staticmethod
    async def save_interior_data(input,
                                 user_space_coll: MongoDBHandler = get_user_space_coll()):
        pass
