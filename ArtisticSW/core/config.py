from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAKAO_CLIENT_ID: str
    KAKAO_CLIENT_SECRET: str
    KAKAO_REDIRECT_URI: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
