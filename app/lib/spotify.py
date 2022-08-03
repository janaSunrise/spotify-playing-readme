from __future__ import annotations

import base64
import json
import sys
import time
from typing import Any, Literal, cast

import requests

from ..config import Config

PYTHON_VERSION = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)


class Spotify:
    RETRY_ATTEMPTS = 3
    USER_AGENT = f"Spotify Twitter Banner ({Config.GITHUB_URL}) Python/{PYTHON_VERSION} Requests/{requests.__version__}"

    BASE_URL = "https://api.spotify.com/v1/me"
    BASE_AUTH_URL = "https://accounts.spotify.com"

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    # Utility methods
    def generate_base64_token(self) -> str:
        return base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode("utf-8")

    @staticmethod
    def _form_url(url: str, data: dict[str, Any]) -> str:
        url += "?" + "&".join(
            [f"{dict_key}={dict_value}" for dict_key, dict_value in data.items()]
        )

        return url

    # Authentication endpoints
    def get_refresh_token(self, refresh_token: str) -> dict[str, Any]:
        token = self.generate_base64_token()

        headers = {"Authorization": f"Basic {token}"}
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        response = requests.post(
            f"{self.BASE_AUTH_URL}/api/token", headers=headers, data=data
        )

        return response.json()

    def generate_token(self, auth_code: str) -> dict[str, Any]:
        token = self.generate_base64_token()

        headers = {"Authorization": f"Basic {token}"}
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": Config.REDIRECT_URI,
        }

        response = requests.post(
            f"{self.BASE_AUTH_URL}/api/token", headers=headers, data=data
        )

        return response.json()

    # Function to fetch the endpoints
    def fetch(
        self,
        url: str,
        access_token: str,
        *,
        headers: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> dict[str, Any] | None:
        if not headers:
            headers = {
                "Authorization": f"Bearer {access_token}",
            }

        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            **headers,
        }

        # Perform request with retries.
        for _ in range(self.RETRY_ATTEMPTS):
            response = requests.get(f"{self.BASE_URL}{url}", headers=headers, json=data)

            # Check if the request was successful.
            if response.status_code == 200:
                return response.json()

            try:
                data = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                data = None

            if 200 <= response.status_code < 300:
                return data

            # Handle ratelimited requests
            if response.status_code == 429:
                retry_after = int(response.headers["Retry-After"])

                time.sleep(retry_after)

                continue

            # Ignore anything 5xx
            if response.status_code >= 500:
                continue

            # Route not found error - This won't happen most of the times
            if response.status_code == 404:
                return None

            # If it's an internal route for the app
            if response.status_code == 403:
                return None

    # API endpoints
    def currently_playing(self, access_token: str) -> dict[str, Any] | None:
        """Get the currently playing song/podcast."""
        return self.fetch(
            self._form_url(
                "/me/player/currently-playing", {"additional_types": "track,episode"}
            ),
            access_token,
        )

    def is_playing(self, access_token: str) -> bool:
        """Check if the user is currently listening to music."""
        currently_playing = self.currently_playing(access_token)

        if currently_playing:
            return currently_playing["is_playing"]

        return False

    def recently_played(
        self,
        access_token: str,
        limit: int = 20,
        before: str | None = None,
        after: str | None = None,
    ) -> dict[str, Any]:
        """Get recently played tracks."""
        data: dict[str, Any] = {"limit": limit}

        if before:
            data["before"] = before

        if after:
            data["after"] = after

        return cast(
            dict,
            self.fetch(
                self._form_url("/me/player/recently-played", data), access_token
            ),
        )

    def top_tracks(
        self,
        access_token: str,
        limit: int = 20,
        offset: int = 0,
        time_range: Literal["short_term", "medium_term", "long_term"] | None = None,
    ) -> dict[str, Any]:
        """Get top tracks of the user."""
        data: dict[str, Any] = {"limit": limit, "offset": offset}

        if time_range:
            data["time_range"] = time_range

        return cast(
            dict, self.fetch(self._form_url("/me/top/tracks", data), access_token)
        )
