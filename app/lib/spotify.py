import base64

from httpx import AsyncClient, HTTPError, HTTPStatusError, RequestError, Timeout

from app.config import settings
from app.exceptions import SpotifyAPIError, TokenRefreshError
from app.models.spotify_api import (
    SpotifyCurrentlyPlayingResponse,
    SpotifyRecentlyPlayedResponse,
    SpotifyTokenResponse,
    SpotifyUserInfoResponse,
)

DEFAULT_TIMEOUT = Timeout(10.0, connect=5.0)


class SpotifyClient:
    BASE_URL: str = "https://api.spotify.com/v1/me"
    AUTH_BASE: str = "https://accounts.spotify.com"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._client: AsyncClient | None = None

    def initialize(self) -> None:
        if self._client is None or self._client.is_closed:
            self._client = AsyncClient(timeout=DEFAULT_TIMEOUT)

    @property
    def client(self) -> AsyncClient:
        if self._client is None or self._client.is_closed:
            raise RuntimeError(
                "AsyncClient not initialized. Call initialize() to initialize.",
            )

        return self._client

    async def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    def _generate_base64_auth(self) -> str:
        auth_str = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(auth_str.encode()).decode("utf-8")

    def generate_auth_url(self, scopes: list[str]) -> str:
        scope_str = " ".join(scopes)
        return (
            f"{self.AUTH_BASE}/authorize?"
            f"client_id={self.client_id}&"
            f"response_type=code&"
            f"scope={scope_str}&"
            f"redirect_uri={self.redirect_uri}"
        )

    async def generate_token(self, authorization_code: str) -> SpotifyTokenResponse:
        headers = {"Authorization": f"Basic {self._generate_base64_auth()}"}
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
        }

        try:
            response = await self.client.post(
                f"{self.AUTH_BASE}/api/token",
                data=payload,
                headers=headers,
            )
            response.raise_for_status()

            return SpotifyTokenResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to generate token: {e.response.text}") from e
        except RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def refresh_token(self, refresh_token: str) -> SpotifyTokenResponse:
        headers = {"Authorization": f"Basic {self._generate_base64_auth()}"}
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        try:
            response = await self.client.post(
                f"{self.AUTH_BASE}/api/token",
                data=payload,
                headers=headers,
            )
            response.raise_for_status()

            return SpotifyTokenResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise TokenRefreshError(f"Failed to refresh token: {e.response.text}") from e
        except RequestError as e:
            raise TokenRefreshError(f"Request failed: {e!s}") from e

    async def get_now_playing(self, access_token: str) -> SpotifyCurrentlyPlayingResponse | None:
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/player/currently-playing?additional_types=track,episode",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code == 204:  # noqa: PLR2004
                return None

            response.raise_for_status()

            return SpotifyCurrentlyPlayingResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to get now playing: {e.response.text}") from e
        except RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def get_recently_played(self, access_token: str, limit: int = 20) -> SpotifyRecentlyPlayedResponse:
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/player/recently-played?limit={limit}",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code == 204:  # noqa: PLR2004
                return SpotifyRecentlyPlayedResponse(items=[])

            response.raise_for_status()

            return SpotifyRecentlyPlayedResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to get recently played: {e.response.text}") from e
        except RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def get_user_info(self, access_token: str) -> SpotifyUserInfoResponse:
        try:
            response = await self.client.get(
                self.BASE_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()

            return SpotifyUserInfoResponse.model_validate(response.json())
        except HTTPStatusError as e:
            raise SpotifyAPIError(f"Failed to get user info: {e.response.text}") from e
        except RequestError as e:
            raise SpotifyAPIError(f"Request failed: {e!s}") from e

    async def fetch_image(self, url: str | None) -> bytes:
        if not url:
            return b""

        try:
            response = await self.client.get(url)
            response.raise_for_status()
        except HTTPError:
            return b""
        else:
            return response.content


spotify_client = SpotifyClient(
    client_id=settings.spotify_client_id,
    client_secret=settings.spotify_secret_id,
    redirect_uri=settings.redirect_uri,
)
