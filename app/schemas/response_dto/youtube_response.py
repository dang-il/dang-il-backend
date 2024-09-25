from pydantic import BaseModel

class YouTubeResponse(BaseModel):
    message: str  
    video_id: str
