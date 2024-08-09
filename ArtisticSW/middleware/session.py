from starlette.middleware.sessions import SessionMiddleware as BaseSessionMiddleware


class SessionMiddleware(BaseSessionMiddleware):
    def __init__(self, app, secret_key: str):
        super().__init__(app, secret_key=secret_key, same_site="lax")
