import re
from app.deps import get_video_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler

class YouTubeService:
    @staticmethod
    def extract_video_id(url: str) -> str:
        # 유튜브 링크에서 영상 ID 추출
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
        if not video_id_match:
            raise ValueError("Invalid YouTube URL")
        return video_id_match.group(1)

    @staticmethod
    async def save_video_id(video_id: str) -> bool:
        # ID MongoDB에 저장
        video_coll: MongoDBHandler = get_video_coll()
        document = {"_id": video_id}
        return await video_coll.insert(document) is not False

    @staticmethod
    async def is_video_id_exist(video_id: str) -> bool:
        # MongoDB안에서 ID가 존재하는지 확인
        video_coll: MongoDBHandler = get_video_coll()
        result = await video_coll.select({"_id": video_id})
        return result is not False

    @staticmethod
    async def delete_video_id(video_id: str) -> bool:
        # MongoDB안에서 ID 삭제
        video_coll: MongoDBHandler = get_video_coll()
        return await video_coll.delete({"_id": video_id}) is not False
