# libralies
from typing import Optional
from asyncio import create_task, gather
# dto
from app.schemas.service_dto.tasking_note_dto import (
    CreateNoteInputDto,
    CreateNoteOuputDto,
    UpdateNoteInputDto,
    UpdateNoteOutputDto,
    DeleteNoteInputDto,
)
# 기타 사용자 모듈
from app.configs.config import settings
from app.services.abs_service import AbsService
from app.deps import get_user_coll, get_taskingnote_coll, get_user_space_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler


# 친구 id 파트에서 오류가 날 것 같음(확인 필요)
class TaskingNoteService(AbsService):
    instance: Optional["TaskingNoteService"] = None
    # 싱글톤 반환
    @classmethod
    def get_instance(cls) -> "TaskingNoteService":
        if(cls.instance is None):
            cls.instance = cls()
        return cls.instance

    @staticmethod
    async def create_note(input: CreateNoteInputDto,
                          user_space_coll: MongoDBHandler = get_user_space_coll(),
                          taskingnote_coll: MongoDBHandler = get_taskingnote_coll()):
        pass


    # @staticmethod
    # async def write_text()
    
# 정의 
# 가능하면 캐시 중간에 두기
# 파일은 -> {file:책page수/몇 번째 파일인지} = 해당 책의 몇 번째 파일인가(위에서 아래로 순서)
    # ex) {file: 2/3} => 해당 책의 2page의 3번째 파일
# 이미지는 -> {image: 책page수/몇 번째 이미지인지}
#  0. 책 전체 생성, 수정, 삭제
#  1. 글 작성 ->
#  2. 글 수정(작성과 동일)
#  3. 글 조회
#  4. 글 삭제
#  5. 글 전체 불러오기
#  6. 책 통째로 삭제
# 파일, 이미지 crud 및 json으로 보내기 -> 이거 분리하자
# 
# 
# 

    