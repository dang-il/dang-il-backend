from pydantic import BaseModel
from typing import Optional, Dict, IO, Any
from bson.binary import Binary

class CreateNoteInputDto(BaseModel):
    user_id: str
    note_title: str
    note_description: Optional[str]

class CreateNoteOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_description: Optional[str]

class UpdateNoteInputDto(BaseModel):
    user_id: str
    note_title: str
    new_note_title: str
    note_description: str

class UpdateNoteOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_description: str

class DeleteNoteInputDto(BaseModel):
    user_id: str
    note_title: str

class WritePageInputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int
    note_text: str
    note_image: Optional[Dict[str, Any]] # 이미지 번호 : 이미지
    note_file: Optional[Dict[str, Any]] # 파일 번호 : 파일

class WritePageOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int

class OpenBookInputDto(BaseModel):
    user_id: str
    note_title: str

class OpenBookOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_description: str
    page_count: int
    page_text: str

class GetTextInputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int

class GetTextOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int
    page_text: str

class GetImageInputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int

class GetImageOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int
    page_image: Optional[Dict[str, Any]]

class GetFileInputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int

class GetFileOutputDto(BaseModel):
    user_id: str
    note_title: str
    note_page: int
    page_file: Optional[Dict[str, Any]]

class DeletePageInput(BaseModel):
    user_id: str
    note_title: str
    note_page: int
