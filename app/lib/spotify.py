import base64
from typing import Any

import httpx

from app.config import settings
from app.exceptions import SpotifyAPIError, TokenRefreshError


class SpotifyClient:
    BASE_URL: str = "https://api.spotify.com/v1/me"
    AUTH_BASE: str = "https://accounts.spotify.com"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def _generate_base64_auth(self) -> str:
        auth_str = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(auth_str.encode()).decode("utf-8")

    def generate_auth_url(self, scopes: list[str]) -> str:
        scope_str = ",".join(scopes)
        return (
            f"{self.AUTH_BASE}/authorize?"
            f"client_id={self.client_id}&"
            f"response_type=code&"
            f"scope={scope_str}&"
            f"redirect_uri={self.redirect_uri}"
        )

    async def generate_token(self, authorization_code: str) -> dict[str, Any]:
        headers = {"Authorization": f"Basic {self._generate_base64_auth()}"}
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.AUTH_BASE}/api/token", data=payload, headers=headers)
                response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to generate token: {e.response.text}") from e
        except httpx.RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def refresh_token(self, refresh_token: str) -> dict[str, Any]:
        headers = {"Authorization": f"Basic {self._generate_base64_auth()}"}
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.AUTH_BASE}/api/token", data=payload, headers=headers)
                response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise TokenRefreshError(f"Failed to refresh token: {e.response.text}") from e
        except httpx.RequestError as e:
            raise TokenRefreshError(f"Request failed: {e!s}") from e

    async def get_now_playing(self, access_token: str) -> dict[str, Any] | None:
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/player/currently-playing?additional_types=track,episode",
                    headers=headers,
                )

                if response.status_code == 204:  # noqa: PLR2004
                    return None

                response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to get now playing: {e.response.text}") from e
        except httpx.RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def get_recently_played(self, access_token: str, limit: int = 20) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/player/recently-played?limit={limit}",
                    headers=headers,
                )

                if response.status_code == 204:  # noqa: PLR2004
                    return {"items": []}

                response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to get recently played: {e.response.text}") from e
        except httpx.RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def get_user_info(self, access_token: str) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL, headers=headers)
                response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to get user info: {e.response.text}") from e
        except httpx.RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e


# Global client instance
spotify_client = SpotifyClient(
    client_id=settings.spotify_client_id,
    client_secret=settings.spotify_secret_id,
    redirect_uri=settings.redirect_uri,
)
