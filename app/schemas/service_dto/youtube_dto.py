from pydantic import BaseModel

class SaveVideoInput(BaseModel):
  video_id: str

class DeleteVideoInput(BaseModel):
  video_id: str

class UpdateVideoInput(BaseModel):
  old_video_id: str
  new_video_id: str

class VideoOutput(BaseModel):
  message: str
  video_id: str