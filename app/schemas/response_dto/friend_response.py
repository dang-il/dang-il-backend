from pydantic import BaseModel
from typing import Dict

class FriendApplyResponse(BaseModel):
    message: str
    data: Dict[str, str]

class FriendApplyResResponse(FriendApplyResponse):
    pass