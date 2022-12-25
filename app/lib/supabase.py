from __future__ import annotations

from time import time
from typing import Any

from memoization import cached

from ..app import spotify, supabase


def get_user(user_id: str) -> dict[str, Any] | None:
    users = supabase.table("user").select("*").eq("user_id", user_id).execute().data

    if len(users) == 0:
        return None

    return users[0]


def insert_user(
    user_id: str, refresh_token: str, access_token: str, expires_in: int, scope: str
) -> None:
    expired_time = int(time()) + expires_in

    supabase.table("user").insert(
        {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "scope": scope,
            "access_token": access_token,
            "expired_time": expired_time,
            "expires_in": expires_in,
        }
    ).execute()


def update_user_refresh_token(user_id: str, refresh_token: str) -> None:
    supabase.table("user").update({"refresh_token": refresh_token}).eq(
        "user_id", user_id
    ).execute()


def update_user_access_token(user_id: str, access_token: str, expires_in: int) -> None:
    expired_time = int(time()) + expires_in

    supabase.table("user").update(
        {
            "access_token": access_token,
            "expired_time": expired_time,
            "expires_in": expires_in,
        }
    ).eq("user_id", user_id).execute()


@cached(ttl=5, max_size=128)
def get_access_token(user_id: str) -> str | None:
    user = get_user(user_id)

    if not user:
        return None

    current_time = int(time())
    access_token = user["access_token"]
    expired_time = user["expired_time"]

    if current_time >= expired_time:
        refresh_token = user["refresh_token"]
        new_token = spotify.get_access_token(refresh_token)
        print(new_token)

        update_user_access_token(
            user_id, new_token["access_token"], new_token["expires_in"]
        )

        access_token = new_token["access_token"]

    return access_token
