from fastapi import APIRouter, HTTPException, Depends
from app.services.youtube_service import YouTubeService, get_youtube_service
from app.schemas.request_dto.youtube_request import YouTubeRequest, UpdateYouTubeRequest
from app.schemas.response_dto.youtube_response import YouTubeResponse, UpdateYouTubeResponse
from app.schemas.service_dto.youtube_dto import SaveVideoInput, DeleteVideoInput, UpdateVideoInput

router = APIRouter()

@router.post("/video/save", response_model=YouTubeResponse)
async def save_video_id(request: YouTubeRequest, service: YouTubeService = Depends(get_youtube_service)):
    try:
        save_input = SaveVideoInput(video_id=request.video_id)
        result = await service.save_video_id(save_input)
        return YouTubeResponse(message=result.message, video_id=result.video_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/video/delete/{video_id}", response_model=YouTubeResponse)
async def delete_video_id(video_id: str, service: YouTubeService = Depends(get_youtube_service)):
    try:
        delete_input = DeleteVideoInput(video_id=video_id)
        result = await service.delete_video_id(delete_input)
        return YouTubeResponse(message=result.message, video_id=result.video_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/video/update", response_model=UpdateYouTubeResponse)
async def update_video_id(request: UpdateYouTubeRequest, service: YouTubeService = Depends(get_youtube_service)):
    try:
        update_input = UpdateVideoInput(old_video_id=request.old_video_id, new_video_id=request.new_video_id)
        result = await service.update_video_id(update_input)
        return UpdateYouTubeResponse(
            message=result.message,
            old_video_id=request.old_video_id,
            new_video_id=request.new_video_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
