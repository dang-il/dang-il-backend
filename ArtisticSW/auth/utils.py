from fastapi import Request, HTTPException
from auth.schemas import User


def create_session(request: Request, user: User):
    request.session['user'] = user.dict()


def get_current_user(request: Request) -> User:
    user_data = request.session.get('user')
    if not user_data:
        raise HTTPException(status_code=401, detail="Failed")
    return User(**user_data)
