from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.schemas.request_dto.user_updatename_request import UpdateUserNameRequest

class UserService:
    def __init__(self):
        self.mongodb_handler = MongoDBHandler()

    async def update_user_name(self, user_id: str, new_name: str) -> bool:
        try:
            # MongoDB의 유저 컬렉션 연결
            user_collection = self.mongodb_handler.get_collection_conn()
            
            # 이름 업데이트
            update_result = await user_collection.update_one(
                {"_id": user_id},
                {"$set": {"name": new_name}}
            )
            
            # 업데이트 성공여부 반환
            return update_result.modified_count > 0
        except Exception as e:
            print(f"UserService Update Error: {e}")
            return False
