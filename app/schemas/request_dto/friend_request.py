from pydantic import BaseModel
from typing import Dict

class FriendApplyRequest(BaseModel):
    sender_id: str
    receiver_id: str
    
class FriendApplyResRequest(BaseModel):
    consent_status: bool
    sender_id: str
    
class FriendSearchRequest(BaseModel):
    search_word: str