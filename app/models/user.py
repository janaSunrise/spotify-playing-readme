from time import time

from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    scope: str | None = None
    expired_time: int | None = None


class User(BaseModel):
    id: str
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None
    scope: str | None = None
    expired_time: int | None = None

    def is_token_expired(self) -> bool:
        if self.expired_time is None:
            return True
        return int(time()) >= self.expired_time
