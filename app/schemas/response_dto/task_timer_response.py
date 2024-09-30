from pydantic import BaseModel

class TaskTimerResponse(BaseModel):
    message: str
    total_time: int
    task_specific_time: dict
