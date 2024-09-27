from app.deps import get_video_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler

class YouTubeService:
    # DB에서 id 삭제
    @staticmethod
    async def save_video_id(video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        document = {"_id": video_id}
        return await video_coll.insert(document) is not False

    # DB에서 id 삭제
    @staticmethod
    async def delete_video_id(video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        return await video_coll.delete({"_id": video_id}) is not False

    '''
    # 기존 id 삭제하고 새 id 저장
    @staticmethod
    async def replace_video_id(video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        await video_coll.delete({})  # 기존 id 삭제
        document = {"_id": video_id}
        return await video_coll.insert(document) is not False
    '''
    
    # MongoDB에 id가 존재유무 확인
    @staticmethod
    async def is_video_id_exist(video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        result = await video_coll.select({"_id": video_id})
        return result is not False
