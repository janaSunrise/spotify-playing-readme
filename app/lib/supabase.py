import asyncio

from supabase import Client, create_client

from app.config import settings
from app.models.user import User


class SupabaseClient:
    def __init__(self, url: str, key: str) -> None:
        self.client: Client = create_client(url, key)

    async def get_user(self, user_id: str) -> User | None:
        result = await asyncio.to_thread(
            lambda: self.client.table("users").select("*").eq("id", user_id).execute(),
        )

        if not result.data:
            return None

        return User(**result.data[0])

    async def upsert_user(self, user: User) -> User:
        user_data = user.model_dump()
        result = await asyncio.to_thread(
            lambda: self.client.table("users").upsert(user_data).execute(),
        )
        return User(**result.data[0])

    async def update_token(self, user_id: str, access_token: str, expired_time: int) -> None:
        update_data = {
            "access_token": access_token,
            "expired_time": expired_time,
        }
        await asyncio.to_thread(
            lambda: self.client.table("users").update(update_data).eq("id", user_id).execute(),
        )


# Global client instance
supabase_client = SupabaseClient(
    url=settings.supabase_url,
    key=settings.supabase_key,
)
