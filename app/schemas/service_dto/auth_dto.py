from pydantic import BaseModel, Field
from typing import Optional, Union

class AuthCallbackInput(BaseModel):
    code: str
    
class AuthCallbackOutput(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str
    profile_image: Optional[str] = None
    
class AuthRegisterInput(AuthCallbackOutput):
    pass

class AuthRegisterOutput(BaseModel):
    session_id: str
    expires: str
    
class AuthLoginInput(AuthCallbackOutput):
    session_id: Optional[str] = None
    
class AuthLoginOutput(AuthRegisterOutput):
    pass