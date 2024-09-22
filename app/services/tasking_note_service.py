# libralies
from typing import Optional
from asyncio import create_task, gather, sleep
# dto
from app.schemas.service_dto.tasking_note_dto import (
    CreateNoteInputDto,
    CreateNoteOuputDto,
    UpdateNoteInputDto,
    UpdateNoteOutputDto,
    DeleteNoteInputDto,
    WritePageInputDto,
    WritePageOutputDto,
    WriteTextInputDto,
    WriteTextOutputDto,
    GetTextInputDto,
    GetTextOuputDto,
)
# 기타 사용자 모듈
from app.configs.config import settings
from app.services.abs_service import AbsService
from app.deps import get_user_coll, get_taskingnote_coll, get_user_space_coll
from app.utils.db_handlers.mongodb_handler import MongoDBHandler

# 이거 레디스 캐시 적용은 시간 나면 할 것
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
                          taskingnote_coll: MongoDBHandler = get_taskingnote_coll()) -> CreateNoteOuputDto:
        # tasking note(책) 생성
        note_dict = {
            "note_title": input.note_title,
            "note_description": input.note_description,
        }
        note_id = await taskingnote_coll.insert(note_dict)

        # user space에 넣기
        new_book = {"note_id": note_id, "note_title": input.note_title}
        await user_space_coll.update(
            {"_id": input.user_id},
            {
                "$set": {
                    "book_list": {
                        "$cond": {
                            "if": {"$gt": [{"$size": "$book_list"}, 0]},  # book_list가 비어있지 않으면
                            "then": {"$concatArrays": ["$book_list", new_book]},  # 기존 리스트에 추가
                            "else": new_book  # 리스트가 없으면 새 리스트를 생성
                        }
                    }
                }
            }
        )

        return CreateNoteOuputDto(
            note_id=note_id,
            note_title=input.note_title
        )

    @staticmethod
    async def update_note(input: UpdateNoteInputDto,
                          user_space_coll: MongoDBHandler = get_user_space_coll(),
                          taskingnote_coll: MongoDBHandler = get_taskingnote_coll()) -> UpdateNoteOutputDto:        
        # task 생성(user_space_coll, taskingnote_coll 모두)
        user_space_update_task = create_task(user_space_coll.update(
            {"_id": input.user_id},
            {
                "$set": {
                    "book_list.$[elem].title": input.note_title           
                }
            }
        ))
        taskingnote_update_task = create_task(taskingnote_coll.update(
            {"_id": input.user_id},
            {
                "$set" : {
                    "note_title": input.note_title,
                    "note_description": input.note_description
                }
            }
        ))

        await gather(user_space_update_task, taskingnote_update_task)

        return UpdateNoteOutputDto(
            note_id=input.note_id,
            note_title=input.note_title,
            note_description=input.note_description
        )

    @staticmethod
    async def delete_note(input: DeleteNoteInputDto,
                          user_space_coll: MongoDBHandler = get_user_space_coll(),
                          taskingnote_coll: MongoDBHandler = get_taskingnote_coll()) -> None:
        # 테스크 생성
        user_space_delete_task = create_task(user_space_coll.delete({"_id": input.user_id}))
        taskingnote_delete_task = create_task(taskingnote_coll.delete({"_id": input.note_id}))
        # 테스크 완료
        await gather(user_space_delete_task, taskingnote_delete_task)

        return 

    @staticmethod
    async def write_page(input: WritePageInputDto,
                         taskingnote_coll: MongoDBHandler = get_taskingnote_coll()) -> WritePageOutputDto:
        # 테스크 생성
        text_update_task = taskingnote_coll.update({"_id": input.note_id}, {
                "$set": {f"text.{input.note_page}": input.note_text}
            })
        image_update_task = sleep(0) # 없는 경우 대비
        file_update_task = sleep(0) # 없는 경우 대비

        if(input.note_image is None): 
            image_update_task = taskingnote_coll.update({"_id": input.note_id}, {
                "$set": {f"image.{input.note_page}": input.note_image}
            })
        if(input.note_file is None):
            file_update_task = taskingnote_coll.update({"_id": input.note_id}, {
                "$set": {f"file.{input.note_page}": input.note_file}
            })

        await gather(text_update_task, image_update_task, file_update_task)

        return WritePageOutputDto(
            note_id=input.note_id,
            note_page=input.note_page,
            note_text=input.note_text,
            note_image=input.note_image,
            note_file=input.note_file
        )
    
    @staticmethod
    async def write_text(input: WriteTextInputDto,
                         taskingnote_coll: MongoDBHandler = get_taskingnote_coll()) -> WriteTextOutputDto:
        await taskingnote_coll.update({"_id": input.note_id}, {
                "$set": {f"text.{input.note_page}": input.note_text}
            })
        
        return WriteTextOutputDto(
            note_id=input.note_id,
            note_page=input.note_page,
            note_text=input.note_page,
        )


# 정의 
# 가능하면 캐시 중간에 두기
# 파일은 -> {{file:책page수/몇 번째 파일인지}} = 해당 책의 몇 번째 파일인가(위에서 아래로 순서)
    # ex) {{file: 2/3}} => 해당 책의 2page의 3번째 파일
# 이미지는 -> {{image: 책page수/몇 번째 이미지인지}}
#  0. 책 전체 생성, 수정, 삭제
#  1. 페이지 전체 생성

#  2. 텍스트만 작성(수정과 동일), 조회, 보내기 -> 이거 분리하자
# 
# 
# 

    