from app.deps import get_video_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler

class YouTubeService:
    @staticmethod
    async def save_video_id(user_id: str, video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        document = {"user_id": user_id, "_id": video_id}
        return await video_coll.insert(document) is not False

    @staticmethod
    async def delete_video_id(user_id: str, video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        return await video_coll.delete({"_id": video_id, "user_id": user_id}) is not False

    @staticmethod
    async def update_video_id(user_id: str, old_video_id: str, new_video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        update_result = await video_coll.update(
            filter={"_id": old_video_id, "user_id": user_id},
            update={"$set": {"_id": new_video_id}}
        )
        return update_result is not False

def get_youtube_service() -> YouTubeService:
    return YouTubeService()
