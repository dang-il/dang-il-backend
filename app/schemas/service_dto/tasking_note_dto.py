from pydantic import BaseModel
from typing import Optional, Dict, IO
from bson.binary import Binary

class CreateNoteInputDto(BaseModel):
    user_id: str
    note_title: str
    note_description: Optional[str]

class CreateNoteOuputDto(BaseModel):
    note_id: str
    note_title: str

class UpdateNoteInputDto(BaseModel):
    user_id: str
    note_id: str
    note_title: str
    note_description: str

class UpdateNoteOutputDto(BaseModel):
    note_id: str
    note_title: str
    note_description: str

class DeleteNoteInputDto(BaseModel):
    user_id: str
    note_id: str

class WritePageInputDto(BaseModel):
    note_id: str
    note_page: str
    note_text: str
    note_image: Optional[Dict[str, Binary]] # 이미지 id : 이미지
    note_file: Optional[Dict[str, IO]] # 파일id : 파일

class WritePageOutputDto(WritePageInputDto):
    pass

class WriteTextInputDto(BaseModel):
    note_id: str
    note_page: str
    note_text: str

class WriteTextOutputDto(WriteTextInputDto):
    note_image: Optional[Dict[str, Binary]] = None # 이미지 id : 이미지
    note_file: Optional[Dict[str, IO]] = None # 파일id : 파일

class GetTextInputDto(BaseModel):
    note_id: str

class GetTextOuputDto(BaseModel):
    note_id: str
    note_text: str

