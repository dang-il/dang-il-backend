from pydantic import BaseModel
from typing import Literal, Optional

class FriendApplyInput(BaseModel):
    sender_id: str
    receiver_id: str
    sender_friend_list: Optional[list]
    
class FriendApplyOutput(BaseModel):
    status: Literal["success", "already_friend", "already_send"]
    
class FriendApplyResInput(BaseModel):
    consent_status: bool
    sender_id: str
    receiver_id: str

class FriendApplyResOutput(FriendApplyResInput):
    pass

class FriendSearchInput(BaseModel):
    search_word: str
    

class FriendSearchOutput(BaseModel):
    exist_status: bool
    id: Optional[str] = None
    name: Optional[str] = None
    tag: Optional[str] = None
    