from pydantic import BaseModel
from typing import Union, Optional, Dict, List, IO, Any
from bson.binary import Binary

class CreateBookRes(BaseModel):
    user_id: str
    note_title: str
    note_description: str

class UpdateBookRes(BaseModel):
    user_id: str
    note_title: str
    note_description: str

class OpenBookRes(BaseModel):
    user_id: str
    note_title: str
    note_description: str
    page_count: int
    page_text: str

class WritePageRes(BaseModel):
    user_id: str
    note_title: str
    note_page: int

class GetPageTextRes(BaseModel):
    note_title: str
    note_page: int
    page_text: str

class GetPageImageRes(BaseModel):
    note_title: str
    note_page: int
    page_image: Optional[Dict[str, Any]]

class GetPageFileRes(BaseModel):
    note_title: str
    note_page: int
    page_image: Optional[Dict[str, Any]]