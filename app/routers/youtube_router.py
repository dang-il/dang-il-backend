from fastapi import APIRouter, HTTPException, Depends
from app.services.youtube_service import YouTubeService
from app.schemas.request_dto.youtube_request import YouTubeRequest
from app.schemas.response_dto.youtube_response import YouTubeResponse

router = APIRouter()

@router.post("/video/save", response_model=YouTubeResponse)
async def save_video_id(request: YouTubeRequest, service: YouTubeService = Depends()):
    # 기존 video_id 삭제
    service.delete_video_id(video_id)
    # 새로운 video_id 저장
    video_id = request.video_id
    if not video_id:
        raise HTTPException(status_code=400, detail="video_id required")
    success = await service.save_video_id(video_id)
    if not success:
        raise HTTPException(status_code=500, detail="saving video_id failed")
    return YouTubeResponse(message="video_id saved sucessfully", video_id=video_id)

@router.delete("/video/delete/{video_id}", response_model=YouTubeResponse)
async def delete_video_id(video_id: str, service: YouTubeService = Depends()):
    success = await service.delete_video_id(video_id)
    if not success:
        raise HTTPException(status_code=404, detail="video_id doesn't exist")
    return YouTubeResponse(message="video_id deleted sucessfully", video_id=video_id)
