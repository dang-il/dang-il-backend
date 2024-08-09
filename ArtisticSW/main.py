import uvicorn
from fastapi import FastAPI
from auth.kakao import router as kakao_router
from auth.google import router as google_router
from middleware.session import SessionMiddleware
from core.config import settings

app = FastAPI()

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# 라우터 등록
app.include_router(kakao_router, prefix="/auth/kakao", tags=["kakao"])
app.include_router(google_router, prefix="/auth/google", tags=["google"])


@app.get("/")
def index():
    return {"message": "Login Page"}


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
