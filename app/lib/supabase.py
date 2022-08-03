from __future__ import annotations

from time import time

from memoization import cached

from ..core.app import supabase


def insert_user(
    user_id: str, refresh_token: str, access_token: str, expires_in: int, scope: str
) -> None:
    expired_time = int(time()) + expires_in

    supabase.table("Users").insert(
        {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "scope": scope,
            "access_token": access_token,
            "expired_time": expired_time,
            "expires_in": expires_in,
        }
    ).execute()


def update_user(user_id: str, access_token: str, expires_in: int) -> None:
    expired_time = int(time()) + expires_in

    supabase.table("Users").update(
        {
            "access_token": access_token,
            "expired_time": expired_time,
            "expires_in": expires_in,
        }
    ).eq("user_id", user_id).execute()


@cached(ttl=5, max_size=128)
def get_access_token(user_id: str) -> str | None:
    users = supabase.table("Users").select("*").eq("user_id", user_id).execute().data

    if len(users) == 0:
        return None

    # Get the values from the user
    token_info = users[0]

    current_time = int(time())
    access_token = token_info["access_token"]
    expired_time = token_info["expired_time"]

    if current_time >= expired_time:
        refresh_token = token_info["refresh_token"]

        new_token = {
            "refresh_token": refresh_token
        }  # TODO: Replace with the new refresh token
        expired_time = int(time()) + new_token["expires_in"]

        update_user(user_id, new_token["expires_in"], expired_time)

        access_token = new_token["access_token"]

    return access_token
