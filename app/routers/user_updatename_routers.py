# app/routers/user_router.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.user_updatename_service import UserService
from app.schemas.request_dto.user_updatename_request import UpdateUserNameRequest
from app.schemas.response_dto.user_updatename_response import UpdateUserNameResponse

router = APIRouter()

@router.put("/user/name/update", response_model=UpdateUserNameResponse)
async def update_user_name(request: UpdateUserNameRequest, service: UserService = Depends()):
    user_id = request.user_id
    new_name = request.new_name
    
    # 이름 업데이트 실행
    success = await service.update_user_name(user_id, new_name)
    if not success:
        raise HTTPException(status_code=500, detail="Updating user name failed")
    
    return UpdateUserNameResponse(message="User name updated successfully", user_id=user_id, new_name=new_name)
