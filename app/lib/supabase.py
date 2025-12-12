from supabase import AsyncClient, acreate_client

from app.config import settings
from app.exceptions import UserNotFoundError
from app.models.user import User


class SupabaseClient:
    def __init__(self, url: str, key: str) -> None:
        self.url = url
        self.key = key
        self._client: AsyncClient | None = None

    @property
    def client(self) -> AsyncClient:
        if self._client is None:
            raise RuntimeError("Supabase client not initialized. Call initialize() first.")
        return self._client

    async def initialize(self) -> None:
        """Initialize the async Supabase client."""
        self._client = await acreate_client(self.url, self.key)

    async def get_user(self, user_id: str) -> User:
        result = await self.client.table("users").select("*").eq("id", user_id).execute()
        if not result.data:
            raise UserNotFoundError(f"User {user_id} not found")
        return User.model_validate(result.data[0])

    async def upsert_user(self, user: User) -> User:
        result = await self.client.table("users").upsert(user.model_dump()).execute()
        return User.model_validate(result.data[0])

    async def update_token(self, user_id: str, access_token: str, expired_time: int) -> None:
        await self.client.table("users").update({
            "access_token": access_token,
            "expired_time": expired_time,
        }).eq("id", user_id).execute()


supabase_client = SupabaseClient(
    url=settings.supabase_url,
    key=settings.supabase_key,
)
