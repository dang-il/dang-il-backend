#libraries
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
# 미들웨어
from app.middleware.session.session_middleware import SessionMiddleware
# 의존성 
from app.services.user_space_service import UserSpaceService, get_user_space_service
# DTO 
from app.schemas.service_dto.user_space_dto import (
    GetUserSpaceInput,
    GetUserSpaceOutput,
    SaveInteriorDataInput,
    SaveInteriorDataOutput,
    DeleteInteriorDataInput,
    GetTodoInput,
    GetTodoOutput,
    SaveTodoInput,
    SaveTodoOutput,
    DeleteTodoInput,
    GetBoardInput,
    GetBoardOutput,
    PostBoardInput,
    PostBoardOutput,
    DeleteBoardInput,
    DeleteBoardOutput
)
from app.schemas.request_dto.user_space_request import (
    SpaceSaveRequest,
    PostTodoRequest,
    PostBoardRequest,
)
from app.schemas.response_dto.user_space_response import (
    GetSpaceResponse,
    SaveSpaceResponse,
    GetTodoResponse,
    PostTodoResponse,
    DeleteSpaceResponse,
    GetBoardResponse,
    PostBoardResponse,
    DeleteBoardResponse,
)
# 기타 사용자 모듈
from app.api_spec.user_space_spec import UserSpaceSpec

router = APIRouter()

# 유저 공간 정보 불러오기 + 이때 할일 적은 것+게시판도 같은 컬렉션에 넣기/ 메인페이지에는 안 가도록 함
@router.get("/{path_user_id}", response_model=GetSpaceResponse, **(UserSpaceSpec.space()))
async def get_space(request: Request,
                    path_user_id: str,
                    user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")
    user_friend_list = user_data.get("friend_list")

    # 본인인 경우 or 친구인 경우
    if(path_user_id == user_id or path_user_id in user_friend_list):
        # 정보 받아오기
        get_user_space_input = GetUserSpaceInput(id=path_user_id, is_unknown=False)
    # 모르는 사람인 경우 or 없는 유저인 경우
    else:
        # 존재 여부 + accessibility 확인
        get_user_space_input = GetUserSpaceInput(id=path_user_id, is_unknown=True)

    user_space_data: GetUserSpaceOutput = await user_space_service.get_user_space_data(get_user_space_input)

    if(user_space_data.accessibility): # 접근 가능한 유저
        return GetSpaceResponse(
            message="data successfully transferred",
            data=user_space_data.model_dump()
        )
    else:
        return JSONResponse(status_code=204)

# 유저 공간 정보 저장하기
@router.post("/save", response_model=SaveSpaceResponse, **(UserSpaceSpec.space_save()))
async def post_space_save(request: Request,
                          post_input: SpaceSaveRequest,
                          user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")
    save_input = SaveInteriorDataInput(id = user_id, updated_location_data = post_input.interior_data)
    user_space_data: SaveInteriorDataOutput = await user_space_service.save_interior_data(save_input)

    return SaveSpaceResponse(
        message="space data successfully updated",
        updated_data=user_space_data
    )

# 유저 공간 정보 초기화
@router.delete("/delete", response_model=DeleteSpaceResponse, **(UserSpaceSpec.space_delete()))
async def delete_space(request:Request,
                       user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")

    delete_interior_input = DeleteInteriorDataInput(id=user_id)
    await user_space_service.delete_interior_data(delete_interior_input)
    return DeleteSpaceResponse(
        message="space data successfully deleted"
    )

# 할일 불러오기
@router.get("/todo", response_model=GetTodoResponse, **(UserSpaceSpec.space_get_todo()))
async def get_space_todo(request:Request,
                         user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")

    get_todo_input = GetTodoInput(id=user_id)
    todo_data: GetTodoOutput = await user_space_service.get_todo(get_todo_input)
    
    return GetTodoResponse(
        message="todo data successfully transmitted",
        todo=todo_data
    )

# 할일 저장하기 -> 초기 저장 이후 불러와야 하므로 저장되는 양식과 동일하게 적기
@router.post("/todo", response_model=PostTodoResponse, **(UserSpaceSpec.space_post_todo()))
async def post_space_todo(request:Request,
                          post_input: PostTodoRequest,
                          user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")

    save_todo_input = SaveTodoInput(id=user_id, todo_list=post_input.todo_data)
    save_todo_result: SaveTodoOutput = await user_space_service.save_todo(save_todo_input)

    return PostTodoResponse(
        message="todo data successfully saved",
        todo=save_todo_result.todo_list
    )

# 할일 통째로 지우기
@router.delete("/todo", response_model=DeleteSpaceResponse, **(UserSpaceSpec.space_delete_todo()))
async def delete_space_todo(request: Request,
                            user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")

    delete_todo_input = DeleteTodoInput(id=user_id)
    await user_space_service.delete_todo(delete_todo_input)

    return DeleteSpaceResponse(
        message="todo data successfully deleted"
    )

# 게시판 확인하기 -> 세션 미들웨어 필요하지 X
@router.get("/board/{path_user_id}", **(UserSpaceSpec.space_board()))
async def get_space_board(path_user_id,
                          user_space_service: UserSpaceService = Depends(get_user_space_service)):
    get_board_input = GetBoardInput(path_user_id)
    board_data: GetBoardOutput = await user_space_service.get_board(get_board_input)

    return GetBoardResponse(
        board_data=board_data
    )

# 친구, 모르는 유저 공간 게시판에 메모 남기기 -> 세션 필요, path_user_id는 게시판 주인 유저
@router.post("/board/{path_user_id}", **(UserSpaceSpec.space_board_write()))
async def post_space_board(request: Request,
                           path_user_id,
                           post_input: PostBoardRequest,
                           user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    user_id = user_data.get("_id")
    user_name = user_data.get("name")
    post_board_input = PostBoardInput(
                                        sender_id=user_id,
                                        sender_name=user_name,
                                        receiver_id=path_user_id,
                                        memo=post_input.memo
                                    )
    post_board_output: PostBoardOutput = await user_space_service.post_board(post_board_input)

    return PostBoardResponse(post_board_output.memo_data)

@router.delete("/board", **(UserSpaceSpec.space_board_delete()))
async def delete_space_board(request: Request,
                             user_space_service: UserSpaceService = Depends(get_user_space_service)):
    user_data = await SessionMiddleware.session_check(request)
    delete_board_input: DeleteBoardInput = {"receiver_id":user_data.get("_id")}
    await user_space_service.delete_board(delete_board_input)

    return DeleteBoardResponse(message="board has been cleared")