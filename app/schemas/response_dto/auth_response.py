from pydantic import BaseModel
from typing import Optional

class AuthGoogleCallbackResponse(BaseModel):
    message: str
    action_type: str