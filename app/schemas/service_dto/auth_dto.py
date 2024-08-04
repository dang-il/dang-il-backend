from pydantic import BaseModel, Field
from typing import Optional, Union

class AuthGoogleCallbackInput(BaseModel):
    code: str
    
class AuthGoogleCallbackOutput(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str
    
class AuthGoogleRegisterInput(AuthGoogleCallbackOutput):
    pass

class AuthGoogleRegisterOutput(BaseModel):
    session_id: str
    expires: str
    
class AuthGoogleLoginInput(AuthGoogleCallbackOutput):
    session_id: Optional[str] = None
    
class AuthGoogleLoginOutput(AuthGoogleRegisterOutput):
    pass