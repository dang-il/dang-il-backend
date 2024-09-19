from pydantic import BaseModel
from typing import Optional

class CreateNoteInputDto(BaseModel):
    user_id: str
    note_title: str
    note_description: Optional[str]

class CreateNoteOuputDto(BaseModel):
    note_id: str
    note_title: str

class UpdateNoteInputDto(BaseModel):
    pass

class UpdateNoteOutputDto(BaseModel):
    pass

class DeleteNoteInputDto(BaseModel):
    pass

# class WriteTextInputDto(BaseModel):
#     user_id: str

    