from pydantic import BaseModel

class AuthCallbackRequest(BaseModel):
    code:str