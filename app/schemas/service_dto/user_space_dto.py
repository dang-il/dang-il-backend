from pydantic import BaseModel
from typing import Union, Tuple, List

class GetUserSpaceInput(BaseModel):
    id: str

class GetUserSpaceOutput(BaseModel):
    user_space_data: Union[dict, bool]
    user_tasking_time_data: Union[dict, bool]

#
class FurnitureArrange(BaseModel):
    decor_id: str
    location: Tuple[float, float, float]    

class SaveInteriorDataInput(BaseModel):
    id: str
    updated_location_data: List[FurnitureArrange]

class SaveInteriorDataOutput(BaseModel):
    pass
    