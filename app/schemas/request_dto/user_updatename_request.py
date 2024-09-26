from pydantic import BaseModel

class UpdateUserNameRequest(BaseModel):
    user_id: str
    new_name: str
