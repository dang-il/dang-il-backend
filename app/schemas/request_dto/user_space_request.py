from pydantic import BaseModel
from typing import Tuple, List, Optional

class FurnitureArrange(BaseModel):
    decor_id: str
    location: Tuple[float, float, float]

class SpaceSaveRequest(BaseModel):
    interior_data: List[Optional[FurnitureArrange]]

class PostTodoRequest(BaseModel):
    todo_data: List[str]