from fastapi import APIRouter, Depends, Request
from app.schemas.request_dto.task_timer_request import TaskTimerStartRequest
from app.schemas.response_dto.task_timer_response import TaskTimerResponse
from app.services.task_timer_service import TaskTimerService, get_task_timer_service
from app.middleware.session.session_middleware import SessionMiddleware

router = APIRouter()

# 시간측정 시작 엔드포인트
@router.post("/task-timer/start", response_model=TaskTimerResponse)
async def start_timer(
    request: Request,
    task_timer_input: TaskTimerStartRequest,
    task_timer_service: TaskTimerService = Depends(get_task_timer_service),
):
    user_data = await SessionMiddleware.session_check(request)
    result = await task_timer_service.start_task_timer(user_data, task_timer_input.task_name)
    return result

# 시간측정 멈춤 엔드포인트
@router.post("/task-timer/pause", response_model=TaskTimerResponse)
async def pause_timer(
    request: Request,
    task_timer_service: TaskTimerService = Depends(get_task_timer_service),
):
    user_data = await SessionMiddleware.session_check(request)
    result = await task_timer_service.pause_task_timer(user_data)
    return result

# 00시 초기화
@router.post("/task-timer/reset", response_model=TaskTimerResponse)
async def reset_timer(
    request: Request,
    task_timer_service: TaskTimerService = Depends(get_task_timer_service),
):
    user_data = await SessionMiddleware.session_check(request)
    result = await task_timer_service.reset_task_timer(user_data)
    return result
