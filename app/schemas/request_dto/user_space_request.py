from pydantic import BaseModel, Field
from typing import Tuple, List, Optional

class FurnitureArrange(BaseModel):
    decor_id: str
    location: Tuple[float, float, float]

class SpaceSaveRequest(BaseModel):
    interior_data: List[Optional[FurnitureArrange]] = Field(
        ..., 
        description="인테리어 데이터 리스트로 보내기", 
        example=
                {
                "decor_id": "desk1",
                "location": [
                        1,
                        2,
                        3
                    ]
                }
    )

class PostTodoRequest(BaseModel):
    todo_data: List[str] = Field(..., 
        description="Todo 데이터 리스트로 보내기",
        example=[
                "국어", "수학"
            ]
        )