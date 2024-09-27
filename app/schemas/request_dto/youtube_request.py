from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    video_id: str  
