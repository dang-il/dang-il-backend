from pydantic import BaseModel
from typing import Union, Tuple, List, Optional, Dict

class GetUserSpaceInput(BaseModel):
    id: str
    is_unknown: bool

class GetUserSpaceOutput(BaseModel):
    accessibility: bool = True
    user_space_data: Optional[Union[dict, bool]] = None
    user_tasking_time_data: Optional[Union[dict, bool]] = None

#
class FurnitureArrange(BaseModel):
    decor_id: str
    location: Tuple[float, float, float]    

class SaveInteriorDataInput(BaseModel):
    id: str
    updated_location_data: List[FurnitureArrange]

class SaveInteriorDataOutput(BaseModel):
    user_space_data: dict

class DeleteInteriorDataInput(BaseModel):
    id: str

class GetTodoInput(BaseModel):
    id: str

class GetTodoOutput(BaseModel):
    todo_list: List[str]

class SaveTodoInput(BaseModel):
    id: str
    todo_list: List[str]

class SaveTodoOutput(BaseModel):
    todo_list: List[str]

class DeleteTodoInput(BaseModel):
    id: str

class GetBoardInput(BaseModel):
    id: str

class GetBoardOutput(BaseModel):
    board_data: list

class PostBoardInput(BaseModel):
    sender_id: str
    sender_name: str
    receiver_id: str
    memo: str

class Memo(BaseModel):
    sender_id: str
    sender_name: str
    content: str

class PostBoardOutput(BaseModel):
    memo_data: List[Memo]

class DeleteBoardInput(BaseModel):
    receiver_id: str

class DeleteBoardOutput(BaseModel):
    pass