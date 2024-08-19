# libralies
from typing import Optional
from asyncio import create_task, gather
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone, timedelta
# dto
from app.schemas.service_dto.user_space_dto import (
    GetUserSpaceInput, 
    GetUserSpaceOutput,
    SaveInteriorDataInput,
    SaveInteriorDataOutput,
    DeleteInteriorDataInput,
    GetTodoInput,
    GetTodoOutput,
    SaveTodoInput,
    SaveTodoOutput,
    DeleteTodoInput,
)
# 기타 사용자 모듈
from app.services.abs_service import AbsService
from app.deps import get_user_space_coll, get_user_tasking_time_coll, get_user_coll
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
                                  user_coll: MongoDBHandler = get_user_coll(),
                                  user_space_coll: MongoDBHandler = get_user_space_coll(),
                                  user_tasking_time_coll: MongoDBHandler = get_user_tasking_time_coll())->GetUserSpaceOutput:
        user_id = input.id
        is_unknown= input.is_unknown
        
        # 본인+친구
        if(not is_unknown):
            user_space_task = create_task(user_space_coll.select({"_id": user_id}))
            user_tasking_time_task = create_task(user_tasking_time_coll.select({"_id": user_id}))
        else: # 모르는 사람 or 존재 X
            user_accessibility_data = await user_coll.select({"_id": user_id}, {"_id": 1, "accessibility": 1})
            if(not user_accessibility_data): # 존재하지 않는 유저
                raise HTTPException(404, "User does not exist")
            elif(not user_accessibility_data.get("accessibility")): # 공개 여부 false
                return GetUserSpaceOutput(accessibility=False)
            else: # 존재+공개 True
                user_space_task = create_task(user_space_coll.select({"_id": user_id}))
                user_tasking_time_task = create_task(user_tasking_time_coll.select({"_id": user_id}))
            
        return GetUserSpaceOutput(
            user_space_data=await user_space_task,
            user_tasking_time_data=await user_tasking_time_task
        )
        
    @staticmethod
    async def save_interior_data(input: SaveInteriorDataInput,
                                 user_space_coll: MongoDBHandler = get_user_space_coll()) -> SaveInteriorDataOutput:
        user_id = input.id
        updated_data = input.updated_location_data

        update_result = await user_space_coll.update({"_id": user_id}, {'$set': updated_data})
        
        if(update_result == False):
            raise HTTPException(status_code=400)
        
        return SaveInteriorDataOutput(
            user_space_data=updated_data
        )
    
    @staticmethod
    async def delete_interior_data(input: DeleteInteriorDataInput,
                                   user_space_coll: MongoDBHandler = get_user_space_coll())->None:
        user_id = input.id

        delete_result = await user_space_coll.delete({"_id": user_id})

        if(delete_result == False):
            raise HTTPException(status_code=400)
    
    @staticmethod
    async def get_todo(input: GetTodoInput,
                       user_space_coll: MongoDBHandler = get_user_space_coll()) -> GetTodoOutput:
        user_id = input.id
        
        user_todo_data = await user_space_coll.select({"_id": user_id}, {"todo_list": 1})

        if(user_todo_data == False or user_todo_data == []):
            return GetTodoOutput(todo_list=[])
        else:
            return GetTodoOutput(todo_list=user_todo_data)

    @staticmethod
    async def save_todo(input: SaveTodoInput,
                        user_space_coll: MongoDBHandler = get_user_space_coll()) -> SaveTodoOutput:
        user_id = input.id
        todo_list = input.todo_list

        update_result = await user_space_coll.update(filter={"_id": user_id}, update={"$set": {"todo_list": todo_list}})

        if(update_result == False):
            HTTPException(status_code=400)
        else:
            return SaveTodoOutput(todo_list)
        



    @staticmethod
    async def delete_todo(input: DeleteTodoInput,
                          user_space_coll: MongoDBHandler = get_user_space_coll()) -> None:
        user_id = input.id
        delete_result = await user_space_coll.delete({"_id": user_id})

        if(delete_result == False):
            raise HTTPException(status_code=400)

def get_user_space_service():
    return UserSpaceService.get_instance()