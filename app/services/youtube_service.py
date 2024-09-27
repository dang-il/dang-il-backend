from app.deps import get_video_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.schemas.service_dto.youtube_dto import SaveVideoInput, DeleteVideoInput, UpdateVideoInput, VideoOutput

class YouTubeService:
    # DB에서 video_id 저장
    @staticmethod
    async def save_video_id(input: SaveVideoInput) -> VideoOutput:
        video_coll: MongoDBHandler = get_video_coll()
        document = {"_id": input.video_id}
        result = await video_coll.insert(document)
        if result:
            return VideoOutput(message="video_id saved successfully", video_id=input.video_id)
        else:
            raise ValueError("Failed to save video_id")

    # DB에서 video_id 삭제
    @staticmethod
    async def delete_video_id(input: DeleteVideoInput) -> VideoOutput:
        video_coll: MongoDBHandler = get_video_coll()
        result = await video_coll.delete({"_id": input.video_id})
        if result:
            return VideoOutput(message="video_id deleted successfully", video_id=input.video_id)
        else:
            raise ValueError("Failed to delete video_id")

    # DB에서 video_id 변경
    @staticmethod
    async def update_video_id(input: UpdateVideoInput) -> VideoOutput:
        video_coll: MongoDBHandler = get_video_coll()
        # 기존 video_id 삭제
        delete_result = await video_coll.delete({"_id": input.old_video_id})
        # 새로운 video_id 저장
        document = {"_id": input.new_video_id}
        insert_result = await video_coll.insert(document)
        if delete_result and insert_result:
            return VideoOutput(message="video_id updated successfully", video_id=input.new_video_id)
        else:
            raise ValueError("Failed to update video_id")

    # DB에서 video_id 존재 유무 확인
    @staticmethod
    async def is_video_id_exist(video_id: str) -> bool:
        video_coll: MongoDBHandler = get_video_coll()
        result = await video_coll.select({"_id": video_id})
        return result is not False

# 의존성 주입 함수
def get_youtube_service() -> YouTubeService:
    return YouTubeService()
