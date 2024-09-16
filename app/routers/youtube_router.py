from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.youtube_service import YouTubeService

router = APIRouter()

class YouTubeLink(BaseModel):
    url: HttpUrl

@router.post("/save")
async def save_youtube_link(link: YouTubeLink):
    # 링크에서 영상 ID 추출
    try:
        video_id = YouTubeService.extract_video_id(link.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 영상 ID 저장
    result = await YouTubeService.save_video_id(video_id)
    if not result:
        raise HTTPException(status_code=500, detail="saving ID failed")
    
    return {"message": "ID saved successfully", "video_id": video_id}

@router.get("/play/{video_id}")
async def play_youtube_video(video_id: str):
    # 유효한 ID인지 확인
    if not await YouTubeService.is_video_id_exist(video_id):
        raise HTTPException(status_code=404, detail="ID not found")
    
    return {"message": "Playing video", "youtube_url": f"https://www.youtube.com/watch?v={video_id}"}

@router.delete("/delete/{video_id}")
async def delete_youtube_video(video_id: str):
    # ID 삭제
    result = await YouTubeService.delete_video_id(video_id)
    if not result:
        raise HTTPException(status_code=404, detail="Video ID not found or failed to delete")
    
    return {"message": "Video ID deleted successfully"}
