from pydantic import BaseModel
from typing import List

class GetSpaceResponse(BaseModel):
    message: str
    data: dict # 나중에 구체화하기

class SaveSpaceResponse(BaseModel):
    message: str
    updated_data: dict

class DeleteSpaceResponse(BaseModel):
    message: str

class GetTodoResponse(BaseModel):
    message: str
    todo: List[str]

class PostTodoResponse(GetTodoResponse):
    pass

class DeleteTodoResponse(BaseModel):
    message: str