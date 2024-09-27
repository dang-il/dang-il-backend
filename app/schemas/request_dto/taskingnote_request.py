from pydantic import BaseModel
from typing import Union, Optional, List, Dict, IO, Any
from bson.binary import Binary

class CreateBookReq(BaseModel):
    note_title: str
    note_description: str

class UpdateBookReq(BaseModel):
    note_title: str
    new_note_title: str
    new_note_description: Optional[str] = None

class DeleteBookReq(BaseModel):
    note_title: str

class WritePageReq(BaseModel):
    note_title: str
    note_page: int
    note_text: str
    note_image: Optional[Dict[str, Any]] # 이미지 번호 : 이미지
    note_file: Optional[Dict[str, Any]] # 파일 번호 : 파일

