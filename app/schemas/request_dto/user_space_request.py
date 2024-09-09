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
class PostBoardRequest(BaseModel):
    memo: dict = Field(...,
        description="메모 데이터 딕셔너리로 보내기",
        example={
            "sender_id": "test1",
            "sender_name": "test1",
            "content": "게시판에 작성할 글입니다."
        }
    )